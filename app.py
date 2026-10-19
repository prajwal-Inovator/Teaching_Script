"""
TeachingScript — Streamlit IDE-style workspace.

Launch:
    streamlit run app.py

Execution uses ANTLR lex/parse plus the real ``Interpreter`` visitor on the
live ML backend (same pipeline as ``main.py``).
"""
from __future__ import annotations

import os
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from interpreter.visitor import Session
from ui.execution import RunOutcome, Stage, execute_source
from ui.theme import APP_VERSION, header_block, inject_theme

ROOT = os.path.dirname(os.path.abspath(__file__))
VALID_DIR = os.path.join(ROOT, "examples", "valid")
INVALID_DIR = os.path.join(ROOT, "examples", "invalid")

DEFAULT_SCRIPT = """lesson "iris_workflow" {
    dataset "data/iris.csv"

    test

    checkpoint "baseline"

    add_examples {
        [5.1, 3.5, 1.4, 0.2] -> "setosa"
        [6.0, 2.9, 4.5, 1.5] -> "versicolor"
    }

    test

    rollback "baseline"

    test
}
"""

_KIND_LABEL = {
    "lesson": "Lesson",
    "dataset": "Dataset",
    "test": "Test",
    "checkpoint": "Checkpoint",
    "rollback": "Rollback",
    "add_examples": "Add examples",
}


def _list_scripts(directory: str) -> List[str]:
    if not os.path.isdir(directory):
        return []
    return sorted(
        f for f in os.listdir(directory) if f.endswith((".ts", ".tscript"))
    )


def _read_script(directory: str, name: str) -> str:
    with open(os.path.join(directory, name), "r", encoding="utf-8") as f:
        return f.read()


def _render_stages(stages: List[Stage]) -> None:
    lines = []
    for s in stages:
        cls = s.status if s.status in ("done", "fail", "pending") else "pending"
        detail = f" — {s.detail}" if s.detail else ""
        lines.append(
            f'<div class="ts-stage {cls}">'
            f'<span class="ts-dot"></span><span>{s.name}{detail}</span></div>'
        )
    st.markdown(
        f'<div class="ts-panel"><div class="ts-panel-title">Execution pipeline</div>'
        + "".join(lines)
        + "</div>",
        unsafe_allow_html=True,
    )


def _plot_confusion(confusion: List[List[int]], class_names: List[str]) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    fig.patch.set_facecolor("#161b22")
    ax.set_facecolor("#161b22")
    data = np.array(confusion, dtype=int)
    im = ax.imshow(data, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names, color="#e6edf3", fontsize=9)
    ax.set_yticklabels(class_names, color="#e6edf3", fontsize=9)
    ax.set_xlabel("Predicted", color="#8b949e", fontsize=10)
    ax.set_ylabel("True", color="#8b949e", fontsize=10)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(
                j,
                i,
                str(int(data[i, j])),
                ha="center",
                va="center",
                color="#e6edf3" if data[i, j] > data.max() / 2 else "#0d1117",
                fontsize=11,
                fontweight="600",
            )
    ax.tick_params(colors="#8b949e")
    for spine in ax.spines.values():
        spine.set_color("#30363d")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _checkpoints_from_session(session: Session) -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    saved: set[str] = set()
    for ev in session.log:
        if ev.kind == "checkpoint":
            name = ev.data.get("name") or ev.message
            saved.add(str(name))
            rows.append((str(name), "Saved"))
        elif ev.kind == "rollback":
            name = ev.data.get("name") or ev.message
            rows.append((str(name), "Restored"))
    for name in saved:
        if not any(r[0] == name and r[1] == "Restored" for r in rows):
            pass
    return rows


def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("script", DEFAULT_SCRIPT)
    ss.setdefault("last_outcome", None)
    ss.setdefault("run_count", 0)
    ss.setdefault("loaded_example", "(default)")
    ss.setdefault("nav", "Workspace")


def page_workspace() -> None:
    ss = st.session_state
    status = "Running…" if ss.get("_running") else "Ready"
    header_block(status=status)

    col_editor, col_side = st.columns([1.55, 1], gap="large")

    with col_editor:
        st.markdown("##### Script editor")
        script_text = st.text_area(
            "TeachingScript source",
            value=ss.script,
            height=380,
            label_visibility="collapsed",
            key="editor_area",
        )

        btn_run, btn_reset, btn_clear = st.columns([1.2, 1, 1])
        with btn_run:
            run_clicked = st.button("Run program", type="primary", use_container_width=True)
        with btn_reset:
            reset_clicked = st.button("Reset editor", use_container_width=True)
        with btn_clear:
            clear_clicked = st.button("Clear output", use_container_width=True)

    with col_side:
        st.markdown("##### Run options")
        persist = st.checkbox(
            "Persist checkpoints to ./checkpoints_ui",
            value=False,
            help="When enabled, checkpoint blobs are written under the project checkpoints_ui folder.",
        )
        st.caption(f"Session runs: **{ss.run_count}**")

        examples = _list_scripts(VALID_DIR)
        pick = st.selectbox(
            "Load example",
            ["(default)"] + examples,
            index=(
                (["(default)"] + examples).index(ss.loaded_example)
                if ss.loaded_example in (["(default)"] + examples)
                else 0
            ),
        )
        if st.button("Load into editor", use_container_width=True):
            ss.script = (
                DEFAULT_SCRIPT if pick == "(default)" else _read_script(VALID_DIR, pick)
            )
            ss.loaded_example = pick
            ss.last_outcome = None
            st.rerun()

    if reset_clicked:
        ss.script = DEFAULT_SCRIPT
        ss.loaded_example = "(default)"
        ss.last_outcome = None
        st.rerun()

    if clear_clicked:
        ss.last_outcome = None
        st.rerun()

    if run_clicked:
        ss.script = script_text
        ckpt_dir = None
        if persist:
            ckpt_dir = os.path.join(ROOT, "checkpoints_ui")
            os.makedirs(ckpt_dir, exist_ok=True)
        ss.last_outcome = execute_source(script_text, checkpoint_dir=ckpt_dir)
        ss.run_count += 1

    ss.script = script_text

    st.markdown("---")
    outcome: Optional[RunOutcome] = ss.last_outcome

    if outcome is None:
        st.info(
            "Write a **lesson** program using the six TeachingScript commands, then click "
            "**Run program**. Output reflects a real ANTLR lex → parse → visitor pass."
        )
        return

    _render_stages(outcome.stages)

    if outcome.syntax_errors:
        st.error("Syntax error — the parser rejected this program.")
        st.dataframe(
            pd.DataFrame(outcome.syntax_errors),
            hide_index=True,
            use_container_width=True,
        )
        return

    if outcome.runtime_error:
        st.error(f"Runtime error: {outcome.runtime_error}")
        return

    session = outcome.session
    if session is None:
        return

    st.success("Program completed successfully.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Parser", "OK")
    c2.metric("Lesson", session.lesson_name or "—")
    tests = session.all_tests
    if tests:
        c3.metric("Tests run", len(tests))
        c4.metric(
            "Latest accuracy",
            f"{tests[-1].data['accuracy'] * 100:.2f}%",
        )
    else:
        c3.metric("Tests run", 0)
        c4.metric("Latest accuracy", "—")

    if len(tests) >= 2:
        if tests[0].data["accuracy"] == tests[-1].data["accuracy"]:
            st.caption(
                "Rollback check: final test accuracy matches the first test "
                "(restored model state)."
            )

    tab_eval, tab_ckpt, tab_log = st.tabs(
        ["Evaluation", "Checkpoints", "Execution log"]
    )

    with tab_eval:
        if not tests:
            st.warning("No `test` command ran in this program.")
        else:
            cols = st.columns(min(len(tests), 4))
            for i, ev in enumerate(tests[:4]):
                with cols[i]:
                    st.metric(
                        f"Test #{i + 1}",
                        f"{ev.data['accuracy'] * 100:.2f}%",
                        help=f"{ev.data['n_correct']}/{ev.data['n_samples']} correct",
                    )
            last = tests[-1]
            st.markdown("**Confusion matrix** (last test)")
            _plot_confusion(last.data["confusion"], last.data["class_names"])
            ds_ev = next((e for e in session.log if e.kind == "dataset"), None)
            if ds_ev:
                st.caption(
                    f"Dataset: `{ds_ev.data.get('path', '—')}` · "
                    f"{ds_ev.data.get('n_train', '?')} train / "
                    f"{ds_ev.data.get('n_test', '?')} test · "
                    f"Model: DecisionTreeClassifier (scikit-learn)"
                )

    with tab_ckpt:
        ck_rows = _checkpoints_from_session(session)
        if not ck_rows:
            st.info("No checkpoint or rollback commands in this run.")
        else:
            st.dataframe(
                pd.DataFrame(ck_rows, columns=["Checkpoint", "Status"]),
                hide_index=True,
                use_container_width=True,
            )
        if session.checkpoint_dir:
            st.caption(f"Disk persistence: `{session.checkpoint_dir}`")

    with tab_log:
        for ev in session.log:
            label = _KIND_LABEL.get(ev.kind, ev.kind)
            st.markdown(f"**{label}** — {ev.message}")


def page_examples() -> None:
    header_block(status="Examples")
    st.markdown(
        "Load valid programs into the workspace, or inspect invalid samples "
        "to see how syntax errors are reported."
    )

    valid = _list_scripts(VALID_DIR)
    invalid = _list_scripts(INVALID_DIR)

    vcol, icol = st.columns(2)
    with vcol:
        st.markdown("##### Valid programs")
        if not valid:
            st.caption("No examples found.")
        else:
            choice = st.selectbox("Valid sample", valid, key="ex_valid")
            st.code(_read_script(VALID_DIR, choice), language="text")
            if st.button("Open in workspace", key="load_valid"):
                st.session_state.script = _read_script(VALID_DIR, choice)
                st.session_state.loaded_example = choice
                st.session_state.last_outcome = None
                st.session_state.nav = "Workspace"
                st.rerun()

    with icol:
        st.markdown("##### Invalid programs (syntax)")
        if not invalid:
            st.caption("No invalid samples found.")
        else:
            ichoice = st.selectbox("Invalid sample", invalid, key="ex_invalid")
            st.code(_read_script(INVALID_DIR, ichoice), language="text")
            if st.button("Try in workspace", key="load_invalid"):
                st.session_state.script = _read_script(INVALID_DIR, ichoice)
                st.session_state.loaded_example = ichoice
                st.session_state.last_outcome = None
                st.session_state.nav = "Workspace"
                st.rerun()


def page_reference() -> None:
    header_block(status="Reference")
    st.markdown(
        """
        TeachingScript programs contain exactly one **lesson** block. Inside the
        block, statements run in order. Paths in `dataset` are relative to the
        project root when you launch Streamlit from there.
        """
    )
    st.markdown(
        """
| Command | Syntax | Purpose |
|---------|--------|---------|
| `lesson` | `lesson "name" { ... }` | Defines a named workflow |
| `dataset` | `dataset "path/to.csv"` | Load CSV, split train/test once, train model |
| `test` | `test` | Evaluate on the fixed held-out test set |
| `checkpoint` | `checkpoint "name"` | Save current model + training state |
| `add_examples` | `add_examples { [f1, f2, ...] -> "label" }` | Append labelled rows and retrain |
| `rollback` | `rollback "name"` | Restore a saved checkpoint |
        """
    )
    st.markdown(
        f"""
        **Comments:** lines starting with `#` are ignored (lexer rule `LINE_COMMENT`).

        **CLI:** `python main.py examples/valid/01_iris_full.ts`

        **Docs:** see [README.md](README.md) and [docs/TOKENS.md](docs/TOKENS.md).

        **Version:** {APP_VERSION}
        """
    )


def main() -> None:
    st.set_page_config(
        page_title="TeachingScript",
        page_icon="TS",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()
    _init_state()

    with st.sidebar:
        st.markdown("### Navigation")
        nav = st.radio(
            "Section",
            ["Workspace", "Examples", "Reference"],
            index=["Workspace", "Examples", "Reference"].index(st.session_state.nav),
            label_visibility="collapsed",
        )
        st.session_state.nav = nav
        st.divider()
        st.caption(
            "Run executes ANTLR lex/parse and the Python visitor — "
            "not a simulated result."
        )

    if nav == "Workspace":
        page_workspace()
    elif nav == "Examples":
        page_examples()
    else:
        page_reference()


if __name__ == "__main__":
    main()

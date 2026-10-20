"""
ANTLR visitor that executes a TeachingScript program.

The visitor orchestrates the ML backend (Dataset / Model / evaluate) and
records a structured execution log. State is held in a Session object so
that repeated runs never leak into one another.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from checkpoint.store import CheckpointNotFound, CheckpointStore
from interpreter.parser_utils import (
    TeachingScriptParserVisitor,
    parse,
)
from ml import Dataset, Model, evaluate, load_dataset


# --------------------------------------------------------------------------- #
# Errors
# --------------------------------------------------------------------------- #
class ParseError(Exception):
    """Raised when the source has syntax errors. Carries per-line details."""

    def __init__(self, errors: List[Dict[str, Any]]) -> None:
        self.errors = errors
        super().__init__(self._format())

    def _format(self) -> str:
        parts = []
        for e in self.errors:
            parts.append(f"line {e['line']}:{e['column']} {e['message']}")
        return "; ".join(parts) if parts else "syntax error"


class InterpreterError(Exception):
    """Raised for semantic / runtime errors during execution."""


# --------------------------------------------------------------------------- #
# Session / log
# --------------------------------------------------------------------------- #
@dataclass
class LogEvent:
    kind: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    lesson_name: str = ""
    dataset: Optional[Dataset] = None
    model: Optional[Model] = None
    checkpoints: Dict[str, bytes] = field(default_factory=dict)
    checkpoint_dir: Optional[str] = None
    log: List[LogEvent] = field(default_factory=list)

    def log_event(self, kind: str, message: str, **data: Any) -> None:
        self.log.append(LogEvent(kind=kind, message=message, data=data))

    # Convenience views used by the UI ------------------------------------- #
    @property
    def last_test(self) -> Optional[LogEvent]:
        for ev in reversed(self.log):
            if ev.kind == "test":
                return ev
        return None

    @property
    def all_tests(self) -> List[LogEvent]:
        return [ev for ev in self.log if ev.kind == "test"]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _unquote(token_text: str) -> str:
    """Strip the surrounding quotes from a STRING token and unescape."""
    s = token_text
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    # Basic escapes that the lexer allows.
    out_chars: List[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "n":
                out_chars.append("\n")
            elif nxt == "t":
                out_chars.append("\t")
            elif nxt == '"':
                out_chars.append('"')
            elif nxt == "\\":
                out_chars.append("\\")
            else:
                out_chars.append(nxt)
            i += 2
        else:
            out_chars.append(c)
            i += 1
    return "".join(out_chars)


# --------------------------------------------------------------------------- #
# Visitor
# --------------------------------------------------------------------------- #
class Interpreter(TeachingScriptParserVisitor):
    """
    Executes a parsed TeachingScript program.

    Usage:
        tree, errors = parse(source)
        if errors: raise ParseError(errors)
        session = Interpreter(Session(checkpoint_dir=...)).visitProgram(tree)
    """

    def __init__(self, session: Optional[Session] = None) -> None:
        super().__init__()
        self.session: Session = session if session is not None else Session()

    # ------------------------------------------------------------------ #
    # Top-level
    # ------------------------------------------------------------------ #
    def visitProgram(self, ctx) -> Session:  # type: ignore[override]
        self.visit(ctx.lesson())
        return self.session

    def visitLesson(self, ctx) -> Session:  # type: ignore[override]
        name = _unquote(ctx.STRING().getText())
        self.session.lesson_name = name
        self.session.log_event("lesson", f"lesson {name!r}")
        for stmt in ctx.statement():
            self.visit(stmt)
        return self.session

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #
    def visitDatasetStmt(self, ctx) -> None:  # type: ignore[override]
        if self.session.dataset is not None:
            raise InterpreterError(
                "'dataset' can only be given once per lesson "
                "(the held-out test split must stay fixed)."
            )
        path = _unquote(ctx.STRING().getText())
        try:
            ds = load_dataset(path)
        except Exception as exc:  # noqa: BLE001
            raise InterpreterError(f"dataset: {exc}") from exc

        model = Model(ds)
        model.train()

        self.session.dataset = ds
        self.session.model = model
        self.session.log_event(
            "dataset",
            f"loaded {path!r} "
            f"({ds.n_train} train / {ds.n_test} test / {len(ds.class_names)} classes)",
            path=path,
            n_train=ds.n_train,
            n_test=ds.n_test,
            class_names=list(ds.class_names),
        )
        return None

    def visitTestStmt(self, ctx) -> None:  # type: ignore[override]
        self._require_model("test")
        res = evaluate(self.session.model, self.session.dataset)  # type: ignore[arg-type]
        n_correct = int(res.confusion.trace())
        self.session.log_event(
            "test",
            f"accuracy = {res.accuracy:.4f} ({n_correct}/{res.n_samples} correct)",
            accuracy=res.accuracy,
            confusion=res.confusion.tolist(),
            class_names=list(res.class_names),
            n_samples=res.n_samples,
            n_correct=n_correct,
        )
        return None

    def visitCheckpointStmt(self, ctx) -> None:  # type: ignore[override]
        self._require_model("checkpoint")
        name = _unquote(ctx.STRING().getText())
        blob = self.session.model.snapshot()  # type: ignore[union-attr]
        self.session.checkpoints[name] = blob
        if self.session.checkpoint_dir:
            CheckpointStore(self.session.checkpoint_dir).save(name, blob)
        self.session.log_event("checkpoint", f"saved checkpoint {name!r}", name=name)
        return None

    def visitRollbackStmt(self, ctx) -> None:  # type: ignore[override]
        self._require_model("rollback")
        name = _unquote(ctx.STRING().getText())
        blob = self.session.checkpoints.get(name)
        if blob is None and self.session.checkpoint_dir:
            try:
                blob = CheckpointStore(self.session.checkpoint_dir).load(name)
                self.session.checkpoints[name] = blob
            except CheckpointNotFound:
                blob = None
        if blob is None:
            raise InterpreterError(f"rollback: checkpoint {name!r} not found.")

        try:
            restored = Model.from_snapshot(blob, self.session.dataset)  # type: ignore[arg-type]
        except Exception as exc:  # noqa: BLE001
            raise InterpreterError(f"rollback: could not restore {name!r}: {exc}") from exc

        self.session.model = restored
        self.session.log_event("rollback", f"restored checkpoint {name!r}", name=name)
        return None

    def visitAddExamplesStmt(self, ctx) -> None:  # type: ignore[override]
        self._require_model("add_examples")
        examples: List[Tuple[List[float], str]] = [
            self.visit(e) for e in ctx.example()
        ]
        try:
            n = self.session.model.add_examples(examples)  # type: ignore[union-attr]
        except Exception as exc:  # noqa: BLE001
            raise InterpreterError(f"add_examples: {exc}") from exc
        self.session.log_event(
            "add_examples",
            f"added {n} example(s) and retrained",
            n_added=n,
        )
        return None

    # ------------------------------------------------------------------ #
    # Leaves
    # ------------------------------------------------------------------ #
    def visitExample(self, ctx) -> Tuple[List[float], str]:  # type: ignore[override]
        feats = self.visit(ctx.featureVector())
        label = _unquote(ctx.STRING().getText())
        return (feats, label)

    def visitFeatureVector(self, ctx) -> List[float]:  # type: ignore[override]
        return [float(t.getText()) for t in ctx.NUMBER()]

    # ------------------------------------------------------------------ #
    def _require_model(self, command: str) -> None:
        if self.session.dataset is None or self.session.model is None:
            raise InterpreterError(
                f"'{command}' requires a dataset. "
                f"Run 'dataset \"<path>\"' first."
            )


# --------------------------------------------------------------------------- #
# Convenience entry points
# --------------------------------------------------------------------------- #
def run_source(
    source: str,
    *,
    checkpoint_dir: Optional[str] = None,
) -> Session:
    """
    Parse + execute a TeachingScript program.

    Raises ParseError for syntax errors, InterpreterError for runtime errors.
    """
    tree, errors = parse(source)
    if errors:
        raise ParseError(errors)

    session = Session(checkpoint_dir=checkpoint_dir)
    Interpreter(session).visitProgram(tree)
    return session


def run_file(path: str, *, checkpoint_dir: Optional[str] = None) -> Session:
    """Execute a .ts file."""
    with open(path, "r", encoding="utf-8") as f:
        return run_source(f.read(), checkpoint_dir=checkpoint_dir)


__all__ = [
    "Interpreter",
    "InterpreterError",
    "ParseError",
    "Session",
    "LogEvent",
    "run_source",
    "run_file",
]
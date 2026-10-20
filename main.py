"""
TeachingScript CLI.

Usage:
    python main.py examples/valid/01_iris_full.ts
    python main.py examples/valid/01_iris_full.ts --checkpoint-dir ./checkpoints
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import List

from interpreter.visitor import (
    InterpreterError,
    LogEvent,
    ParseError,
    Session,
    run_file,
)


# --------------------------------------------------------------------------- #
# Pretty printing
# --------------------------------------------------------------------------- #
_KIND_LABEL = {
    "lesson": "LESSON",
    "dataset": "DATASET",
    "test": "TEST",
    "checkpoint": "CHECKPOINT",
    "rollback": "ROLLBACK",
    "add_examples": "ADD_EXAMPLES",
}


def _format_confusion(confusion: List[List[int]], class_names: List[str]) -> str:
    col_w = max(len(n) for n in class_names) + 2
    corner = "true \\ pred"
    row_w = max(max(len(n) for n in class_names), len(corner)) + 2

    lines: List[str] = []
    header = f"{corner:>{row_w}}" + "".join(f"{n:>{col_w}}" for n in class_names)
    lines.append(header)

    for i, name in enumerate(class_names):
        row = f"{name:>{row_w}}" + "".join(
            f"{int(v):>{col_w}}" for v in confusion[i]
        )
        lines.append(row)

    return "\n".join(lines)


def print_event(ev: LogEvent) -> None:
    label = _KIND_LABEL.get(ev.kind, ev.kind.upper())
    print(f"[{label:<12}] {ev.message}")
    if ev.kind == "test":
        confusion = ev.data.get("confusion")
        class_names = ev.data.get("class_names")
        if confusion and class_names:
            block = _format_confusion(confusion, class_names)
            for line in block.splitlines():
                print(f"{'':<14}{line}")


# --------------------------------------------------------------------------- #
def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Run a TeachingScript program through the ANTLR interpreter.",
    )
    parser.add_argument("script", help="Path to a .ts TeachingScript file.")
    parser.add_argument(
        "--checkpoint-dir",
        default=None,
        help="Directory for persistent checkpoints (optional; in-memory if omitted).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the final summary line.",
    )
    args = parser.parse_args(argv)

    if not os.path.isfile(args.script):
        print(f"error: file not found: {args.script}", file=sys.stderr)
        return 2

    print(f"Running: {args.script}")
    print("=" * 68)

    try:
        session: Session = run_file(
            args.script, checkpoint_dir=args.checkpoint_dir
        )
    except ParseError as exc:
        print("SYNTAX ERROR", file=sys.stderr)
        for e in exc.errors:
            print(
                f"  line {e['line']}, column {e['column']}: {e['message']}",
                file=sys.stderr,
            )
        return 1
    except InterpreterError as exc:
        print(f"RUNTIME ERROR: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        for ev in session.log:
            print_event(ev)
    print("=" * 68)

    tests = session.all_tests
    if tests:
        print(
            f"Executed {len(tests)} test command(s). "
            f"Final accuracy: {tests[-1].data['accuracy']:.4f}"
        )
    print("Completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
Run TeachingScript through the real ANTLR pipeline with structured stage info.

Uses the same parse + visitor path as ``interpreter.visitor.run_source`` but
returns execution stages for the UI without parsing twice.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from interpreter.parser_utils import lex, parse
from interpreter.visitor import (
    Interpreter,
    InterpreterError,
    ParseError,
    Session,
)

StageStatus = Literal["pending", "done", "fail", "skip"]


@dataclass
class Stage:
    name: str
    status: StageStatus
    detail: str = ""


@dataclass
class RunOutcome:
    session: Optional[Session] = None
    stages: List[Stage] = field(default_factory=list)
    syntax_errors: Optional[List[Dict[str, Any]]] = None
    runtime_error: Optional[str] = None


def execute_source(
    source: str,
    *,
    checkpoint_dir: Optional[str] = None,
) -> RunOutcome:
    """
    Lex, parse, and interpret ``source``.

    Raises are not used; errors are returned on ``RunOutcome``.
    """
    stages: List[Stage] = [
        Stage("Source received", "done", f"{len(source.splitlines())} line(s)"),
    ]

    _, lex_errors = lex(source)
    if lex_errors:
        stages.append(
            Stage("Lexing", "fail", lex_errors[0].get("message", "lexical error"))
        )
        stages.append(Stage("Parsing", "skip"))
        stages.append(Stage("Interpreter", "skip"))
        return RunOutcome(stages=stages, syntax_errors=lex_errors)

    stages.append(Stage("Lexing", "done", "tokens recognised"))

    tree, parse_errors = parse(source)
    if parse_errors:
        stages.append(
            Stage("Parsing", "fail", parse_errors[0].get("message", "syntax error"))
        )
        stages.append(Stage("Interpreter", "skip"))
        return RunOutcome(stages=stages, syntax_errors=parse_errors)

    stages.append(Stage("Parsing", "done", "parse tree built"))

    session = Session(checkpoint_dir=checkpoint_dir)
    try:
        Interpreter(session).visitProgram(tree)
    except InterpreterError as exc:
        stages.append(Stage("Interpreter", "fail", str(exc)))
        return RunOutcome(stages=stages, runtime_error=str(exc))

    stages.append(Stage("Interpreter", "done", "commands executed"))

    for ev in session.log:
        if ev.kind == "dataset":
            stages.append(
                Stage("Dataset / model", "done", ev.message)
            )
        elif ev.kind == "test":
            acc = ev.data.get("accuracy")
            detail = ev.message
            if acc is not None:
                detail = f"accuracy {acc * 100:.2f}%"
            stages.append(Stage("Evaluation", "done", detail))
        elif ev.kind == "checkpoint":
            stages.append(Stage("Checkpoint", "done", ev.message))
        elif ev.kind == "rollback":
            stages.append(Stage("Rollback", "done", ev.message))
        elif ev.kind == "add_examples":
            stages.append(Stage("Training update", "done", ev.message))

    stages.append(Stage("Complete", "done", "workflow finished"))
    return RunOutcome(session=session, stages=stages)


def outcome_to_parse_error(outcome: RunOutcome) -> Optional[ParseError]:
    if outcome.syntax_errors:
        return ParseError(outcome.syntax_errors)
    return None

"""
Utilities for tokenising and parsing TeachingScript programs with ANTLR4.

This is the ONLY module in the project that imports the ANTLR-generated
Python files. It ensures ``generated/`` is on ``sys.path`` before importing
them, so the rest of the codebase stays independent of that detail.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Make the generated ANTLR Python modules importable
# --------------------------------------------------------------------------- #
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_GEN = os.path.join(_ROOT, "generated")
if _GEN not in sys.path:
    sys.path.insert(0, _GEN)

# Safe to import now (generated modules use flat imports).
from antlr4 import CommonTokenStream, InputStream  # noqa: E402
from antlr4.error.ErrorListener import ErrorListener  # noqa: E402
from TeachingScriptLexer import TeachingScriptLexer  # noqa: E402
from TeachingScriptParser import TeachingScriptParser  # noqa: E402
from TeachingScriptParserVisitor import TeachingScriptParserVisitor  # noqa: E402


class CollectingErrorListener(ErrorListener):
    """Collects ANTLR syntax errors instead of printing them to stderr."""

    def __init__(self) -> None:
        super().__init__()
        self.errors: List[Dict[str, Any]] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # noqa: N802
        self.errors.append(
            {
                "line": line,
                "column": column,
                "message": msg,
                "text": str(offendingSymbol) if offendingSymbol is not None else None,
            }
        )


def lex(source: str) -> Tuple[List[Any], List[Dict[str, Any]]]:
    """Return (tokens, errors) for the given source string."""
    lexer = TeachingScriptLexer(InputStream(source))
    lexer.removeErrorListeners()
    listener = CollectingErrorListener()
    lexer.addErrorListener(listener)
    tokens = list(lexer.getAllTokens())
    return tokens, listener.errors


def parse(source: str) -> Tuple[Any, List[Dict[str, Any]]]:
    """
    Parse ``source`` and return ``(parse_tree, errors)``.

    ``errors`` is a list of dicts with keys ``line``, ``column``, ``message``,
    ``text``. The tree is the ``ProgramContext`` produced by ``program()``.
    """
    lexer = TeachingScriptLexer(InputStream(source))
    lexer.removeErrorListeners()
    lex_listener = CollectingErrorListener()
    lexer.addErrorListener(lex_listener)

    token_stream = CommonTokenStream(lexer)
    parser = TeachingScriptParser(token_stream)
    parser.removeErrorListeners()
    parse_listener = CollectingErrorListener()
    parser.addErrorListener(parse_listener)

    tree = parser.program()
    return tree, lex_listener.errors + parse_listener.errors


def parse_file(path: str) -> Tuple[Any, List[Dict[str, Any]]]:
    """Parse a TeachingScript file. Returns ``(tree, errors)``."""
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read())


__all__ = [
    "CollectingErrorListener",
    "TeachingScriptLexer",
    "TeachingScriptParser",
    "TeachingScriptParserVisitor",
    "lex",
    "parse",
    "parse_file",
]
"""Smoke tests for the ANTLR grammar (Milestone 1 / 2)."""
from __future__ import annotations

import os

from interpreter.parser_utils import lex, parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VALID = os.path.join(ROOT, "examples", "valid")
INVALID = os.path.join(ROOT, "examples", "invalid")


SIMPLE_PROGRAM = '''
lesson "demo" {
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
'''


def test_tokens_recognised():
    tokens, errors = lex(SIMPLE_PROGRAM)
    assert not errors, errors
    assert len(tokens) >= 30


def test_simple_program_parses():
    tree, errors = parse(SIMPLE_PROGRAM)
    assert not errors, errors
    assert tree is not None


def test_all_valid_examples_parse():
    for name in sorted(os.listdir(VALID)):
        if not name.endswith(".ts"):
            continue
        path = os.path.join(VALID, name)
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        _, errors = parse(src)
        assert not errors, f"{name} failed to parse: {errors}"


def test_all_invalid_examples_fail():
    for name in sorted(os.listdir(INVALID)):
        if not name.endswith(".ts"):
            continue
        path = os.path.join(INVALID, name)
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        _, errors = parse(src)
        assert errors, f"{name} unexpectedly parsed cleanly"


def test_missing_closing_brace_reports_line():
    src = 'lesson "broken" {\n    dataset "x.csv"\n'
    _, errors = parse(src)
    assert errors
    assert any(e["line"] >= 1 for e in errors)
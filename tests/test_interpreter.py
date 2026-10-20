"""End-to-end interpreter tests."""
from __future__ import annotations

import os

import numpy as np
import pytest

from interpreter.visitor import (
    InterpreterError,
    ParseError,
    run_file,
    run_source,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IRIS = os.path.join(ROOT, "data", "iris.csv")
EXAMPLES_VALID = os.path.join(ROOT, "examples", "valid")
EXAMPLES_INVALID = os.path.join(ROOT, "examples", "invalid")


# --------------------------------------------------------------------------- #
# Happy paths
# --------------------------------------------------------------------------- #
def test_full_workflow_from_example_file(tmp_path):
    path = os.path.join(EXAMPLES_VALID, "01_iris_full.ts")
    session = run_file(path, checkpoint_dir=str(tmp_path))

    kinds = [ev.kind for ev in session.log]
    assert kinds[0] == "lesson"
    assert "dataset" in kinds
    assert kinds.count("test") == 3
    assert "checkpoint" in kinds
    assert "add_examples" in kinds
    assert "rollback" in kinds

    # First and last test must agree (baseline restored).
    tests = session.all_tests
    assert tests[0].data["accuracy"] == tests[-1].data["accuracy"]


def test_dataset_split_is_fixed(tmp_path):
    src = f'''
    lesson "fixed" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        test
        add_examples {{
            [5.0, 3.4, 1.5, 0.2] -> "setosa"
        }}
        test
    }}
    '''
    session = run_source(src, checkpoint_dir=str(tmp_path))
    tests = session.all_tests
    assert tests[0].data["n_samples"] == tests[1].data["n_samples"] == 30


def test_all_valid_examples_execute(tmp_path):
    for name in sorted(os.listdir(EXAMPLES_VALID)):
        if not name.endswith(".ts"):
            continue
        path = os.path.join(EXAMPLES_VALID, name)
        # Each example gets its own checkpoint dir so they cannot interfere.
        dir_for_run = tmp_path / name.replace(".ts", "")
        dir_for_run.mkdir()
        session = run_file(path, checkpoint_dir=str(dir_for_run))
        assert session.log, f"{name} produced an empty log"


# --------------------------------------------------------------------------- #
# Error paths
# --------------------------------------------------------------------------- #
def test_syntax_error_raises_parse_error():
    bad = 'lesson "x" {\n    dataset "data/iris.csv"\n'
    with pytest.raises(ParseError) as ei:
        run_source(bad)
    assert ei.value.errors
    assert ei.value.errors[0]["line"] >= 1


def test_test_before_dataset_raises():
    src = 'lesson "x" {\n    test\n}'
    with pytest.raises(InterpreterError, match="requires a dataset"):
        run_source(src)


def test_checkpoint_before_dataset_raises():
    src = 'lesson "x" {\n    checkpoint "b"\n}'
    with pytest.raises(InterpreterError, match="requires a dataset"):
        run_source(src)


def test_dataset_twice_raises():
    src = f'''
    lesson "x" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        dataset "{IRIS.replace(chr(92), '/')}"
    }}
    '''
    with pytest.raises(InterpreterError, match="only be given once"):
        run_source(src)


def test_missing_dataset_file_raises():
    src = 'lesson "x" {\n    dataset "no/such/file.csv"\n    test\n}'
    with pytest.raises(InterpreterError, match="not found"):
        run_source(src)


def test_wrong_feature_count_in_add_examples():
    src = f'''
    lesson "x" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        add_examples {{
            [1.0, 2.0] -> "setosa"
        }}
    }}
    '''
    with pytest.raises(InterpreterError, match="expected 4 features"):
        run_source(src)


def test_unknown_label_in_add_examples():
    src = f'''
    lesson "x" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        add_examples {{
            [5.1, 3.5, 1.4, 0.2] -> "banana"
        }}
    }}
    '''
    with pytest.raises(InterpreterError, match="unknown label"):
        run_source(src)


def test_all_invalid_examples_raise(tmp_path):
    for name in sorted(os.listdir(EXAMPLES_INVALID)):
        if not name.endswith(".ts"):
            continue
        path = os.path.join(EXAMPLES_INVALID, name)
        with pytest.raises(ParseError):
            run_file(path, checkpoint_dir=str(tmp_path))
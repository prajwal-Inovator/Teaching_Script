"""Tests for the on-disk checkpoint store and interpreter rollback."""
from __future__ import annotations

import os

import numpy as np
import pytest

from checkpoint import CheckpointNotFound, CheckpointStore
from interpreter.visitor import InterpreterError, run_source
from ml import Model, evaluate, load_dataset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IRIS = os.path.join(ROOT, "data", "iris.csv")


# --------------------------------------------------------------------------- #
# Store-level
# --------------------------------------------------------------------------- #
def test_store_round_trip(tmp_path):
    store = CheckpointStore(str(tmp_path))
    store.save("alpha", b"payload-1")
    store.save("beta", b"payload-2")
    assert store.exists("alpha")
    assert store.exists("beta")
    assert store.load("alpha") == b"payload-1"
    assert store.load("beta") == b"payload-2"
    assert store.list_names() == ["alpha", "beta"]


def test_store_missing_raises(tmp_path):
    store = CheckpointStore(str(tmp_path))
    with pytest.raises(CheckpointNotFound):
        store.load("nope")


def test_store_sanitises_names(tmp_path):
    store = CheckpointStore(str(tmp_path))
    store.save("../../evil", b"x")
    # Nothing escapes tmp_path
    files = os.listdir(str(tmp_path))
    assert any(f.endswith(".pkl") for f in files)


# --------------------------------------------------------------------------- #
# Interpreter + persistence round trip
# --------------------------------------------------------------------------- #
BASELINE_PROGRAM = '''
lesson "checkpoint_demo" {
    dataset "data/iris.csv"
    checkpoint "baseline"
    test
    add_examples {
        [6.7, 3.1, 5.6, 2.4] -> "virginica"
    }
    test
    rollback "baseline"
    test
}
'''


def test_rollback_in_memory_matches_baseline(tmp_path):
    src = BASELINE_PROGRAM.replace('data/iris.csv', IRIS.replace('\\', '/'))
    session = run_source(src, checkpoint_dir=str(tmp_path))

    tests = [ev for ev in session.log if ev.kind == "test"]
    assert len(tests) == 3
    baseline, after_add, after_rollback = tests
    # The rollback result must match the baseline (restored state).
    assert after_rollback.data["accuracy"] == baseline.data["accuracy"]
    assert np.array_equal(
        np.array(after_rollback.data["confusion"]),
        np.array(baseline.data["confusion"]),
    )


def test_rollback_persisted_survives_new_session(tmp_path):
    src = BASELINE_PROGRAM.replace('data/iris.csv', IRIS.replace('\\', '/'))
    run_source(src, checkpoint_dir=str(tmp_path))

    # A new session with the same dir must be able to restore by name.
    src2 = f'''
    lesson "resume" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        rollback "baseline"
        test
    }}
    '''
    session = run_source(src2, checkpoint_dir=str(tmp_path))
    assert session.model is not None
    # Baseline accuracy from the first run in a fresh process.
    ds = load_dataset(IRIS)
    m = Model(ds); m.train()
    expected = evaluate(m, ds)
    got = [ev for ev in session.log if ev.kind == "test"][-1]
    assert abs(got.data["accuracy"] - expected.accuracy) < 1e-12


def test_unknown_checkpoint_raises(tmp_path):
    src = f'''
    lesson "bad" {{
        dataset "{IRIS.replace(chr(92), '/')}"
        rollback "ghost"
    }}
    '''
    with pytest.raises(InterpreterError, match="ghost"):
        run_source(src, checkpoint_dir=str(tmp_path))
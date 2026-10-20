"""Unit tests for the ML backend (Batch 2)."""
from __future__ import annotations

import os

import numpy as np
import pytest

from ml import DatasetError, Model, ModelError, evaluate, load_dataset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IRIS = os.path.join(ROOT, "data", "iris.csv")


@pytest.fixture(scope="module")
def dataset():
    return load_dataset(IRIS)


# --------------------------------------------------------------------------- #
# Dataset
# --------------------------------------------------------------------------- #

def test_iris_shape_and_split(dataset):
    assert dataset.n_features == 4
    assert dataset.n_train == 120
    assert dataset.n_test == 30
    assert dataset.n_train + dataset.n_test == 150
    assert len(dataset.class_names) == 3
    assert dataset.class_names == sorted(dataset.class_names)


def test_missing_file_raises(tmp_path):
    with pytest.raises(DatasetError):
        load_dataset(str(tmp_path / "nope.csv"))


def test_non_numeric_feature_raises(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("a,b,label\n1,x,cat\n2,3,dog\n4,5,cat\n6,7,dog\n", encoding="utf-8")
    with pytest.raises(DatasetError):
        load_dataset(str(p))


def test_single_class_raises(tmp_path):
    p = tmp_path / "one.csv"
    p.write_text("a,label\n1,x\n2,x\n3,x\n4,x\n", encoding="utf-8")
    with pytest.raises(DatasetError):
        load_dataset(str(p))


# --------------------------------------------------------------------------- #
# Model
# --------------------------------------------------------------------------- #

def test_train_and_evaluate(dataset):
    m = Model(dataset)
    m.train()
    res = evaluate(m, dataset)
    assert 0.0 <= res.accuracy <= 1.0
    assert res.accuracy >= 0.8  # iris with seed 42 is well above this
    assert res.confusion.shape == (3, 3)
    assert int(res.confusion.sum()) == dataset.n_test


def test_deterministic_baseline(dataset):
    a = Model(dataset); a.train(); ra = evaluate(a, dataset)
    b = Model(dataset); b.train(); rb = evaluate(b, dataset)
    assert ra.accuracy == rb.accuracy
    assert np.array_equal(ra.confusion, rb.confusion)


def test_add_examples_retrains_without_touching_test(dataset):
    m = Model(dataset)
    m.train()
    n0 = m.X_train.shape[0]
    added = m.add_examples([
        ([5.1, 3.5, 1.4, 0.2], "setosa"),
        ([6.0, 2.9, 4.5, 1.5], "versicolor"),
    ])
    assert added == 2
    assert m.X_train.shape[0] == n0 + 2
    assert dataset.n_test == 30  # fixed


def test_add_example_wrong_feature_count(dataset):
    m = Model(dataset); m.train()
    with pytest.raises(ModelError):
        m.add_examples([([1.0, 2.0], "setosa")])


def test_add_example_unknown_label(dataset):
    m = Model(dataset); m.train()
    with pytest.raises(ModelError):
        m.add_examples([([5.1, 3.5, 1.4, 0.2], "banana")])


def test_snapshot_restore_preserves_evaluation(dataset):
    m = Model(dataset); m.train()
    before = evaluate(m, dataset)
    blob = m.snapshot()

    # Mutate
    m.add_examples([([6.7, 3.1, 5.6, 2.4], "virginica")])

    # Restore and re-evaluate
    restored = Model.from_snapshot(blob, dataset)
    after = evaluate(restored, dataset)
    assert after.accuracy == before.accuracy
    assert np.array_equal(after.confusion, before.confusion)


def test_confusion_matrix_is_readable(dataset):
    m = Model(dataset); m.train()
    text = evaluate(m, dataset).format_confusion()
    for name in dataset.class_names:
        assert name in text
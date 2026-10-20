"""
Reproducible DecisionTreeClassifier wrapper that also owns the mutable
training set, so add_examples() / snapshot() / restore() operate on a
single, self-contained state object.
"""
from __future__ import annotations

import io
import pickle
from typing import List, Sequence, Tuple

import numpy as np
from sklearn.tree import DecisionTreeClassifier

from ml.dataset import Dataset


class ModelError(Exception):
    """Raised for invalid operations on a TeachingScript ML model."""


Example = Tuple[Sequence[float], str]


class Model:
    """Trainable model + its current training state."""

    def __init__(self, dataset: Dataset, *, random_state: int = 42) -> None:
        self.dataset = dataset
        self.random_state = random_state
        self.class_names: List[str] = list(dataset.class_names)
        self.n_features: int = dataset.n_features
        self.X_train: np.ndarray = dataset.X_train.copy()
        self.y_train: np.ndarray = dataset.y_train.copy()
        self.clf: DecisionTreeClassifier | None = None

    # ------------------------------------------------------------------ #
    def train(self) -> None:
        """Fit the classifier on the current training set."""
        clf = DecisionTreeClassifier(random_state=self.random_state)
        clf.fit(self.X_train, self.y_train)
        # sklearn sorts classes alphabetically. We already sorted class_names
        # at dataset load time, so this is a no-op safeguard.
        self.class_names = list(clf.classes_)
        self.clf = clf

    # ------------------------------------------------------------------ #
    def add_examples(self, examples: Sequence[Example]) -> int:
        """
        Append labelled examples to the training set and retrain.
        Does NOT touch the test set. Returns the number of examples added.
        """
        if not examples:
            return 0

        rows: List[List[float]] = []
        labels: List[str] = []

        for i, (feat, label) in enumerate(examples, start=1):
            if len(feat) != self.n_features:
                raise ModelError(
                    f"Example #{i}: expected {self.n_features} features, "
                    f"got {len(feat)}."
                )
            for v in feat:
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    raise ModelError(
                        f"Example #{i}: non-numeric feature {v!r}."
                    )
            if label not in self.class_names:
                raise ModelError(
                    f"Example #{i}: unknown label {label!r}. "
                    f"Known labels: {self.class_names}"
                )
            rows.append([float(v) for v in feat])
            labels.append(label)

        new_X = np.asarray(rows, dtype=float)
        new_y = np.asarray(labels, dtype=object)

        self.X_train = np.vstack([self.X_train, new_X])
        self.y_train = np.concatenate([self.y_train, new_y])
        self.train()
        return len(examples)

    # ------------------------------------------------------------------ #
    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.clf is None:
            raise ModelError("Model has not been trained yet.")
        return self.clf.predict(X)

    # ------------------------------------------------------------------ #
    def snapshot(self) -> bytes:
        """
        Serialize model + training state to a bytes blob.

        The test set is intentionally excluded: it lives on the Dataset and
        is never mutated.
        """
        payload = {
            "class_names": self.class_names,
            "n_features": self.n_features,
            "X_train": self.X_train,
            "y_train": self.y_train,
            "clf": self.clf,
            "random_state": self.random_state,
        }
        buf = io.BytesIO()
        pickle.dump(payload, buf, protocol=pickle.HIGHEST_PROTOCOL)
        return buf.getvalue()

    @classmethod
    def from_snapshot(cls, blob: bytes, dataset: Dataset) -> "Model":
        """Reconstruct a Model from a snapshot. Only for trusted local blobs."""
        try:
            payload = pickle.loads(blob)
        except Exception as exc:  # noqa: BLE001
            raise ModelError(f"Corrupt model snapshot: {exc}") from exc

        required = {"class_names", "n_features", "X_train", "y_train", "clf", "random_state"}
        missing = required - payload.keys()
        if missing:
            raise ModelError(f"Snapshot is missing fields: {sorted(missing)}")

        m = cls.__new__(cls)
        m.dataset = dataset
        m.class_names = list(payload["class_names"])
        m.n_features = int(payload["n_features"])
        m.X_train = payload["X_train"]
        m.y_train = payload["y_train"]
        m.clf = payload["clf"]
        m.random_state = int(payload["random_state"])
        return m
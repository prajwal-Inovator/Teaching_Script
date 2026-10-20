"""
Evaluation against the fixed held-out test set.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix

from ml.dataset import Dataset
from ml.model import Model


@dataclass
class EvalResult:
    accuracy: float
    confusion: np.ndarray
    class_names: List[str]
    n_samples: int

    def format_confusion(self) -> str:
        """Human-readable text confusion matrix."""
        names = list(self.class_names)
        width = max([len(n) for n in names] + [len("pred ->")]) + 2
        header = " " * width + "".join(f"{n:>{width}}" for n in names)
        lines = ["pred ->".rjust(width) + "".join(f"{n:>{width}}" for n in names)]
        for i, name in enumerate(names):
            row = f"{name:>{width}}" + "".join(
                f"{int(v):>{width}}" for v in self.confusion[i]
            )
            lines.append(row)
        # keep header text clean
        lines[0] = header.replace("pred ->", " " * len("pred ->"), 1) if False else lines[0]
        return "\n".join(lines)


def evaluate(model: Model, dataset: Dataset) -> EvalResult:
    """
    Evaluate the model against the dataset's fixed test split.
    Never regenerates the split.
    """
    preds = model.predict(dataset.X_test)
    acc = float(accuracy_score(dataset.y_test, preds))
    cm = confusion_matrix(
        dataset.y_test, preds, labels=list(model.class_names)
    )
    return EvalResult(
        accuracy=acc,
        confusion=cm,
        class_names=list(model.class_names),
        n_samples=int(len(dataset.y_test)),
    )
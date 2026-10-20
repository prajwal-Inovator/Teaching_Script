"""
Generates data/iris.csv from sklearn's built-in iris dataset.

Run once from the project root:
    python scripts/make_iris.py

The CSV has 150 rows, 5 columns:
    sepal_length, sepal_width, petal_length, petal_width, label

This avoids any runtime or build-time internet dependency.
"""
from __future__ import annotations

import os

import pandas as pd
from sklearn.datasets import load_iris


FEATURE_COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root, "data")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "iris.csv")

    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=FEATURE_COLUMNS)
    df["label"] = [iris.target_names[t] for t in iris.target]
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df)} rows, {len(df.columns)} columns)")


if __name__ == "__main__":
    main()
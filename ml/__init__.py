"""Machine-learning backend for TeachingScript."""
from ml.dataset import Dataset, DatasetError, load_dataset
from ml.evaluation import EvalResult, evaluate
from ml.model import Model, ModelError

__all__ = [
    "Dataset",
    "DatasetError",
    "load_dataset",
    "EvalResult",
    "evaluate",
    "Model",
    "ModelError",
]
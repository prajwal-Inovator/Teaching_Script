"""
On-disk checkpoint storage.

A checkpoint is a pickle blob produced by Model.snapshot(). The store keeps
each blob under <dir>/<sanitised-name>.pkl. Names are sanitised to avoid
path traversal but the original name is stored inside the file so it can be
verified on load.
"""
from __future__ import annotations

import os
import pickle
from typing import Any, Dict


class CheckpointNotFound(KeyError):
    """Raised when a requested checkpoint does not exist on disk."""


def _sanitise(name: str) -> str:
    safe = "".join(c if (c.isalnum() or c in "-_.") else "_" for c in name).strip("._")
    if not safe:
        raise ValueError(f"Invalid checkpoint name: {name!r}")
    return safe


class CheckpointStore:
    """File-backed checkpoint storage."""

    def __init__(self, directory: str) -> None:
        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)

    # ------------------------------------------------------------------ #
    def _path(self, name: str) -> str:
        return os.path.join(self.directory, f"{_sanitise(name)}.pkl")

    # ------------------------------------------------------------------ #
    def save(self, name: str, blob: bytes) -> str:
        """Persist ``blob`` under ``name``. Returns the file path written."""
        path = self._path(name)
        payload: Dict[str, Any] = {"name": name, "blob": blob}
        with open(path, "wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
        return path

    # ------------------------------------------------------------------ #
    def load(self, name: str) -> bytes:
        """Load a checkpoint blob. Raises CheckpointNotFound if absent."""
        path = self._path(name)
        if not os.path.isfile(path):
            raise CheckpointNotFound(name)
        with open(path, "rb") as f:
            payload = pickle.load(f)
        if not isinstance(payload, dict) or "blob" not in payload:
            raise ValueError(f"Checkpoint file is corrupt: {path}")
        return payload["blob"]

    # ------------------------------------------------------------------ #
    def exists(self, name: str) -> bool:
        return os.path.isfile(self._path(name))

    # ------------------------------------------------------------------ #
    def list_names(self) -> list[str]:
        names = []
        for fname in os.listdir(self.directory):
            if fname.endswith(".pkl"):
                names.append(fname[:-4])
        return sorted(names)

    # ------------------------------------------------------------------ #
    def delete(self, name: str) -> None:
        path = self._path(name)
        if os.path.isfile(path):
            os.remove(path)
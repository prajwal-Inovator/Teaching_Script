"""
Smoke tests for app.py.

Streamlit scripts run top-to-bottom and cannot be safely imported under
pytest, so we verify (a) that the file exists, (b) that it compiles, and
(c) that it uses the real backend entry point rather than a simulation.
"""
from __future__ import annotations

import os
import py_compile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.path.join(ROOT, "app.py")


def test_app_file_exists():
    assert os.path.isfile(APP), f"app.py not found at {APP}"


def test_app_compiles():
    py_compile.compile(APP, doraise=True)


def test_app_calls_real_backend():
    with open(APP, "r", encoding="utf-8") as f:
        src = f.read()
    assert "Interpreter" in src or "execute_source" in src
    assert "st.text_area" in src
    # We must never fabricate a result — sanity-check that the file
    # does not define any hardcoded accuracy value.
    lowered = src.lower()
    assert "hardcoded" not in lowered
    assert "fake_accuracy" not in lowered
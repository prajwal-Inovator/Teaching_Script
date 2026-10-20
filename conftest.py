"""
Pytest bootstrap: make sure the project root is importable so tests can do
``from interpreter.parser_utils import …``.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
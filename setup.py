"""Compatibility shim for editable installs.

All metadata lives in ``pyproject.toml``. This file exists only because pip
< 21.3 refuses a pyproject-only editable install ("editable mode currently
requires a setuptools-based build"); with it present, the same
``pip install -e .`` works on both the old legacy path and the modern PEP 660
path. It declares nothing: everything is read from ``pyproject.toml``.
"""

from setuptools import setup

setup()

#!/usr/bin/env python3
"""Bootstraps the EVMBench Harbor verifier inside a Harbor task container."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

extra_path = os.environ.get("EVMBENCH_HARBOR_PYTHONPATH", "/tests/evmbench-src")
if extra_path and Path(extra_path).exists():
    sys.path.insert(0, extra_path)

runpy.run_module("evmbench.harbor_adapter.verifier", run_name="__main__")

#!/usr/bin/env python3
"""Repository convenience entrypoint for the installed skill's context gate."""

from __future__ import annotations

import runpy
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "hls-factory-orchestrate"
    / "scripts"
    / "context_baseline.py"
)

runpy.run_path(str(SOURCE), run_name="__main__")

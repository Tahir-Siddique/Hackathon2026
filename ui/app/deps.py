"""Paths and imports shared with parent pipeline project."""

from __future__ import annotations

import sys
from pathlib import Path

UI_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = UI_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = UI_DIR / "output"
TEMPLATES_DIR = UI_DIR / "templates"
STATIC_DIR = UI_DIR / "static"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

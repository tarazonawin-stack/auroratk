"""Shared test helpers: import the CI scripts and run code inside a temporary folder."""

import contextlib
import os
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CI_DIR = ROOT / "perfiles" / "ci"
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))


@contextlib.contextmanager
def in_temp_dir() -> Iterator[Path]:
    """Run the block inside a fresh empty folder, then go back."""
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as folder:
        os.chdir(folder)
        try:
            yield Path(folder)
        finally:
            os.chdir(previous)

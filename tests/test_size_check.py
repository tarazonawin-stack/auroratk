"""Tests for perfiles/ci/size_check.py (R02)."""

import contextlib
import io
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from helpers import in_temp_dir

import size_check


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True)


def write_lines(path: str, count: int) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("x = 1\n" * count, encoding="utf-8")


def start_repo() -> None:
    """Create a repo with one base commit on branch 'base'."""
    git("init", "-q", "-b", "base")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    write_lines("README.py", 1)
    git("add", ".")
    git("commit", "-q", "-m", "base")
    git("checkout", "-q", "-b", "work")


def commit_all() -> None:
    git("add", ".")
    git("commit", "-q", "-m", "change")


def run_main() -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), mock.patch("sys.argv", ["size_check.py", "base"]):
        code = size_check.main()
    return code, out.getvalue()


class ExclusionTests(unittest.TestCase):
    def test_lock_translation_and_vendored_files_are_excluded(self) -> None:
        for name in ["uv.lock", "locale/es/LC_MESSAGES/django.po", "app.mo",
                     "third_party/fonts/a.css", "LICENSES/OFL-1.1.txt",
                     "tickets/migrations/0001_initial.py"]:
            self.assertTrue(size_check.is_excluded(Path(name)), name)

    def test_own_code_is_not_excluded(self) -> None:
        for name in ["tickets/models.py", "core/static/app.css", "templates/base.html"]:
            self.assertFalse(size_check.is_excluded(Path(name)), name)


class ChangeSizeTests(unittest.TestCase):
    def test_counts_added_and_deleted_lines_but_not_excluded_files(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 30)
            write_lines("uv.lock", 900)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), 30)

    def test_deleted_lines_count_too(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 50)
            commit_all()
            git("branch", "-f", "base")
            write_lines("app/a.py", 10)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), 40)

    def test_binary_files_are_skipped(self) -> None:
        with in_temp_dir():
            start_repo()
            Path("logo.png").write_bytes(bytes(range(256)) * 4)
            write_lines("app/a.py", 5)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), 5)

    def test_change_over_cap_fails(self) -> None:
        with in_temp_dir():
            start_repo()
            for i in range(2):
                write_lines(f"app/m{i}.py", 201)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 1)
            self.assertIn("Changed lines: 402", out)

    def test_change_between_target_and_cap_warns_but_passes(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 250)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 0)
            self.assertIn("::warning::Change is above the 200-line target", out)


class FileSizeTests(unittest.TestCase):
    def test_file_over_cap_fails_and_over_warning_warns(self) -> None:
        with in_temp_dir():
            start_repo()
            for name, count in [("big.py", 401), ("medium.py", 301), ("small.py", 300)]:
                write_lines(name, count)
            commit_all()
            warnings, failures = size_check.oversized_files()
            self.assertEqual(failures, ["big.py: 401 lines (cap 400)"])
            self.assertEqual(warnings, ["medium.py: 301 lines (split it before 400)"])

    def test_non_code_files_are_ignored(self) -> None:
        with in_temp_dir():
            start_repo()
            Path("notes.md").write_text("line\n" * 900, encoding="utf-8")
            commit_all()
            self.assertEqual(size_check.oversized_files(), ([], []))


if __name__ == "__main__":
    unittest.main()

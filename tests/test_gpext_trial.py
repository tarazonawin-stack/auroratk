"""Failing cases found while adopting v4.0.0-rc.1 in GPEXT (2026-11-26), for the 4.0.1 patch.

All tests fail on v4.0.0-rc.1 on purpose (DEC-001: a patch needs a test that fails before the fix).
"""

import contextlib
import io
import subprocess
import tomllib
import unittest
from pathlib import Path

from helpers import CI_DIR, ROOT, in_temp_dir

import kernel_sync
import risk
import size_check


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True)


class GpextTrialTests(unittest.TestCase):
    def test_adopting_the_kernel_alone_passes_r02(self) -> None:
        """R02 must not count the kernel's own copy: `check` already proves it is byte-identical.

        On rc.1, `sync` alone adds ~1000 lines of code (scripts/, pr-description.yml) and the size
        check fails, so no adoption PR (guias/adoptar.md, step 6) can ever pass the kernel's CI.
        """
        with in_temp_dir():
            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.com")
            git("config", "user.name", "t")
            Path("README.md").write_text("x\n", encoding="utf-8")
            git("add", "-A")
            git("commit", "-q", "-m", "base")
            git("checkout", "-q", "-b", "adopt")
            with contextlib.redirect_stdout(io.StringIO()):
                kernel_sync.main(["sync", "--from", str(ROOT), "--ci", "python-django"])
            Path("AGENTS.md").unlink()  # the project's own template, not the kernel's copy
            git("add", "-A")
            git("commit", "-q", "-m", "adopt")
            code, docs = size_check.changed_lines("main")
            self.assertLessEqual(code, size_check.CODE_CAP, f"kernel copy counted as code: {code}")
            self.assertLessEqual(docs, size_check.DOC_CAP, f"kernel copy counted as docs: {docs}")

    def test_kernel_scripts_fit_the_profiles_own_line_length(self) -> None:
        """The scripts copied to scripts/ must pass the lint the profile asks for (R04).

        A project cannot edit them, so `ruff check .` with pyproject-django.toml fails (92 errors
        on rc.1: E501, C901, S603/S607, B905, I001) and the project has to exclude them. Only the
        line length is checked here, with the standard library.
        """
        config = tomllib.loads((CI_DIR / "pyproject-django.toml").read_text(encoding="utf-8"))
        limit = config["tool"]["ruff"]["line-length"]
        long_lines = [f"{path.name}:{number}"
                      for path in sorted(CI_DIR.glob("*.py"))
                      for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
                      if len(line) > limit]
        self.assertEqual(long_lines, [])

    def test_removing_asserts_from_a_test_is_risk_3(self) -> None:
        """R12: weakening a test is risk 3. GPEXT's lanes marked it red; risk.py gives 2."""
        change = risk.FileChange("tests/test_totals.py",
                                 added=["def test_total():", "    pass"],
                                 removed=["def test_total():", "    assert total == 3"])
        self.assertEqual(risk.file_risk(change, risk.CRITICAL_PATHS, risk.ALARM_WORDS)[0], 3)

    def test_a_project_can_make_removing_its_access_guard_risk_3(self) -> None:
        """A project's own access guard (GPEXT: scoped(...)) must count like login_required.

        `.github/riesgo.txt` only adds alarms on ADDED lines, so removing the guard stays risk 2.
        """
        paths, words = risk.load_project_rules("alarma scoped(\n")
        change = risk.FileChange("tickets/views.py", added=["    qs = Ticket.objects.all()"],
                                 removed=["    qs = scoped(Ticket.objects, request.user)"])
        self.assertEqual(risk.file_risk(change, risk.CRITICAL_PATHS + paths, risk.ALARM_WORDS + words)[0], 3)


if __name__ == "__main__":
    unittest.main()

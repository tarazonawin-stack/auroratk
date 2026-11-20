"""Tests for perfiles/ci/pr_meta.py and the part D rules of pr_check.py (R12)."""

import contextlib
import io
import os
import subprocess
import unittest
from pathlib import Path
from unittest import mock

import helpers
import pr_check
import pr_meta
from test_pr_check import filled

DEPENDABOT = ["-c", "user.name=dependabot[bot]",
              "-c", "user.email=49699333+dependabot[bot]@users.noreply.github.com"]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def merged_main() -> str:
    """A repo whose main has one merged PR (a merge commit). Returns that merge's SHA."""
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "Test")
    with open("app.py", "w") as f:
        f.write("x = 1\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    git("checkout", "-qb", "feature")
    with open("app.py", "a") as f:
        f.write("y = 2\n")
    git("commit", "-qam", "feature")
    git("checkout", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "Merge feature", "feature")
    return git("rev-parse", "HEAD")


class RevertTests(unittest.TestCase):
    def test_exact_revert_of_a_merge_is_recognised(self) -> None:
        with helpers.in_temp_dir():
            merge = merged_main()
            git("checkout", "-qb", "revert")
            git("revert", "--no-edit", "-m", "1", merge)
            self.assertTrue(pr_meta.is_exact_revert("main", "revert"))

    def test_revert_with_an_extra_change_is_not_exact(self) -> None:
        with helpers.in_temp_dir():
            merge = merged_main()
            git("checkout", "-qb", "revert")
            git("revert", "--no-commit", "-m", "1", merge)
            with open("app.py", "a") as f:
                f.write("z = eval(input())\n")
            git("add", "-A")
            git("commit", "-qm", f"Revert\n\nThis reverts commit {merge}.")
            self.assertFalse(pr_meta.is_exact_revert("main", "revert"))

    def test_a_message_that_only_claims_to_revert_is_not_a_revert(self) -> None:
        with helpers.in_temp_dir():
            merge = merged_main()
            git("checkout", "-qb", "fake")
            with open("app.py", "w") as f:
                f.write("x = 1\nimport os; os.system('rm -rf /')\n")
            git("commit", "-qam", f"Revert\n\nThis reverts commit {merge}.")
            self.assertFalse(pr_meta.is_exact_revert("main", "fake"))

    def test_revert_with_other_indentation_is_not_exact(self) -> None:
        """Re-adding a line with other indentation changes Python's meaning; patch-id ignores it."""
        with helpers.in_temp_dir():
            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.invalid")
            git("config", "user.name", "Test")
            Path("app.py").write_text("if admin:\n    allow()\ndone()\n")
            git("add", "-A")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "feature")
            Path("app.py").write_text("if admin:\n    pass\ndone()\n")
            git("commit", "-qam", "feature")
            git("checkout", "-q", "main")
            git("merge", "-q", "--no-ff", "-m", "Merge feature", "feature")
            merge = git("rev-parse", "HEAD")
            git("checkout", "-qb", "revert")
            Path("app.py").write_text("if admin:\n    pass\nallow()\ndone()\n".replace("    pass\n", ""))
            git("commit", "-qam", f"Revert\n\nThis reverts commit {merge}.")
            self.assertNotEqual(Path("app.py").read_text(), "if admin:\n    allow()\ndone()\n")
            self.assertFalse(pr_meta.is_exact_revert("main", "revert"))

    def test_revert_of_an_old_change_is_not_skipped(self) -> None:
        with helpers.in_temp_dir():
            merge = merged_main()
            for i in range(pr_meta.RECENT):
                git("commit", "-q", "--allow-empty", "-m", f"later {i}")
            git("checkout", "-qb", "revert")
            git("revert", "--no-edit", "-m", "1", merge)
            self.assertFalse(pr_meta.is_exact_revert("main", "revert"))

    def test_two_commits_are_not_an_exact_revert(self) -> None:
        with helpers.in_temp_dir():
            merge = merged_main()
            git("checkout", "-qb", "revert")
            git("revert", "--no-edit", "-m", "1", merge)
            git("commit", "-q", "--allow-empty", "-m", "more")
            self.assertFalse(pr_meta.is_exact_revert("main", "revert"))


class DependabotTests(unittest.TestCase):
    def test_only_dependabot_commits(self) -> None:
        with helpers.in_temp_dir():
            merged_main()
            git("checkout", "-qb", "bump")
            git(*DEPENDABOT, "commit", "-q", "--allow-empty", "-m", "Bump x")
            self.assertTrue(pr_meta.dependabot_only("main", "bump"))
            git("commit", "-q", "--allow-empty", "-m", "someone else")
            self.assertFalse(pr_meta.dependabot_only("main", "bump"))

    def test_dependabot_may_only_touch_dependency_files(self) -> None:
        with helpers.in_temp_dir():
            merged_main()
            git("checkout", "-qb", "bump")
            with open("uv.lock", "w") as f:
                f.write("x\n")
            git("add", "-A")
            git(*DEPENDABOT, "commit", "-qm", "Bump x")
            self.assertTrue(pr_meta.dependabot_only("main", "bump"))
            with open("backdoor.py", "w") as f:
                f.write("x = 1\n")
            git("add", "-A")
            git(*DEPENDABOT, "commit", "-qm", "Bump y")
            self.assertFalse(pr_meta.dependabot_only("main", "bump"))

    def test_cli_prints_only_0_or_1(self) -> None:
        with helpers.in_temp_dir() as repo:
            merged_main()
            git("checkout", "-qb", "bump")
            git(*DEPENDABOT, "commit", "-q", "--allow-empty", "-m", "Bump x")
            out = subprocess.run(["python3", str(helpers.CI_DIR / "pr_meta.py"), "main", "bump"],
                                 capture_output=True, text=True, cwd=repo,
                                 env={**os.environ, "PR_AUTHOR": "dependabot[bot]"})
        self.assertEqual(out.stdout.splitlines(), ["IS_REVERT=0", "DEPENDABOT_OK=1"])


def run(env: dict[str, str]) -> tuple[int, str]:
    out = io.StringIO()
    base = {"PR_BODY": "", "COMPUTED_RISK": "3", "KERNEL_LEVEL": "estandar", "HEAD_SHA": "",
            "IS_REVERT": "", "PR_AUTHOR": "", "DEPENDABOT_OK": "", "DEPENDABOT_EXCEPTION": ""}
    with contextlib.redirect_stdout(out), mock.patch.dict(os.environ, {**base, **env}):
        code = pr_check.main()
    return code, out.getvalue()


class PrCheckPartDTests(unittest.TestCase):
    def test_exact_revert_asks_nothing(self) -> None:
        self.assertEqual(run({"IS_REVERT": "1"})[0], 0)

    def test_dependabot_needs_a_written_exception(self) -> None:
        self.assertEqual(run({"PR_AUTHOR": "dependabot[bot]", "DEPENDABOT_OK": "1"})[0], 1)
        code, out = run({"PR_AUTHOR": "dependabot[bot]", "DEPENDABOT_OK": "1", "DEPENDABOT_EXCEPTION": "EXC-004"})
        self.assertEqual(code, 0)
        self.assertIn("EXC 004", out)

    def test_dependabot_with_someone_elses_commit_fails(self) -> None:
        code, out = run({"PR_AUTHOR": "dependabot[bot]", "DEPENDABOT_OK": "0", "DEPENDABOT_EXCEPTION": "EXC-004"})
        self.assertEqual(code, 1)
        self.assertIn("commits de otra persona", out)

    def test_review_must_be_on_the_current_head(self) -> None:
        reviewed = "abc1234def56"
        body = filled(3).replace("<cuál · which>, en el commit <SHA>", f"Sonnet 5.5, en el commit {reviewed}")
        self.assertEqual(pr_check.problems(body, 3, head_sha=reviewed + "0" * 28), [])
        found = pr_check.problems(body, 3, head_sha="def5678" + "0" * 33)
        self.assertTrue(any("cambios nuevos sin revisar" in p and "otra revisión a la IA" in p for p in found))

    def test_a_seven_character_sha_is_not_enough(self) -> None:
        body = filled(3).replace("<cuál · which>, en el commit <SHA>", "Sonnet 5.5, en el commit abc1234")
        found = pr_check.problems(body, 3, head_sha="abc1234" + "0" * 33)
        self.assertTrue(any("12 caracteres" in p for p in found))

    def test_checked_review_without_a_commit_fails(self) -> None:
        body = filled(3).replace("<cuál · which>, en el commit <SHA>", "Sonnet 5.5")
        found = pr_check.problems(body, 3, head_sha="def5678" + "0" * 33)
        self.assertTrue(any("en qué commit" in p for p in found))


if __name__ == "__main__":
    unittest.main()

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
            self.assertEqual(size_check.changed_lines("base"), (30, 0))

    def test_deleted_lines_count_too(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 50)
            commit_all()
            git("branch", "-f", "base")
            write_lines("app/a.py", 10)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), (40, 0))

    def test_binary_files_are_skipped(self) -> None:
        with in_temp_dir():
            start_repo()
            Path("logo.png").write_bytes(bytes(range(256)) * 4)
            write_lines("app/a.py", 5)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), (5, 0))

    def test_change_over_cap_fails(self) -> None:
        with in_temp_dir():
            start_repo()
            for i in range(2):
                write_lines(f"app/m{i}.py", 201)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 1)
            self.assertIn("Changed lines: code 402", out)

    def test_change_exactly_at_cap_passes(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 200)
            write_lines("app/b.py", 200)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 0)
            self.assertIn("Changed lines: code 400", out)

    def test_change_exactly_at_target_does_not_warn(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 200)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 0)
            self.assertNotIn("Code is above the 200-line target", out)

    def test_change_between_target_and_cap_warns_but_passes(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 250)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 0)
            self.assertIn("::warning::Code is above the 200-line target", out)


def write_doc(path: str, count: int) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("text\n" * count, encoding="utf-8")


class CodeAndDocsTests(unittest.TestCase):
    """R02 in 4.0.0: code and documentation are counted apart and each cap blocks."""

    def test_docs_are_counted_apart_from_code(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 30)
            write_doc("docs/a.md", 20)
            write_doc("docs/b.RST", 5)
            write_doc("docs/c.adoc", 4)
            write_doc("requirements.txt", 3)  # .txt is not documentation: it counts as code
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), (33, 29))

    def test_docs_over_cap_fail_even_with_little_code(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 10)
            write_doc("docs/a.md", 201)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 1)
            self.assertIn("docs 201 (cap 200)", out)
            self.assertIn("::error::Documentation is above the 200-line cap", out)

    def test_docs_exactly_at_cap_pass(self) -> None:
        with in_temp_dir():
            start_repo()
            write_doc("docs/a.md", 200)
            commit_all()
            self.assertEqual(run_main()[0], 0)

    def test_code_at_cap_plus_docs_at_cap_pass(self) -> None:
        """Before 4.0.0 this 600-line PR failed; now each part is within its own cap."""
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 400)
            write_doc("docs/a.md", 200)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 0)
            self.assertIn("Changed lines: code 400", out)

    def test_code_over_cap_says_so(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 401)
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 1)
            self.assertIn("::error::Code is above the 400-line cap", out)


class FileSizeTests(unittest.TestCase):
    def test_file_over_cap_fails_and_over_warning_warns(self) -> None:
        with in_temp_dir():
            start_repo()
            for name, count in [("big.py", 401), ("at_cap.py", 400), ("medium.py", 301),
                                ("small.py", 300)]:
                write_lines(name, count)
            commit_all()
            warnings, failures = size_check.oversized_files()
            self.assertEqual(failures, ["big.py: 401 lines (cap 400)"])
            self.assertEqual(sorted(warnings), ["at_cap.py: 400 lines (split it before 400)",
                                                "medium.py: 301 lines (split it before 400)"])

    def test_non_code_files_are_ignored(self) -> None:
        with in_temp_dir():
            start_repo()
            Path("notes.md").write_text("line\n" * 900, encoding="utf-8")
            commit_all()
            self.assertEqual(size_check.oversized_files(), ([], []))


class AgentsWordsTests(unittest.TestCase):
    """R13 in 4.0.0: AGENTS.md has a 450-word cap checked by CI."""

    def test_agents_over_the_cap_fails(self) -> None:
        with in_temp_dir():
            start_repo()
            Path("AGENTS.md").write_text("palabra " * 451, encoding="utf-8")
            commit_all()
            code, out = run_main()
            self.assertEqual(code, 1)
            self.assertIn("::error::AGENTS.md: 451 words (cap 450)", out)

    def test_agents_at_the_cap_or_missing_passes(self) -> None:
        with in_temp_dir():
            start_repo()
            self.assertIsNone(size_check.agents_too_long())
            Path("AGENTS.md").write_text("palabra " * 450, encoding="utf-8")
            self.assertIsNone(size_check.agents_too_long())

    def test_the_template_leaves_room_for_the_project(self) -> None:
        from helpers import ROOT
        words = len((ROOT / "plantillas/AGENTS.md").read_text(encoding="utf-8").split())
        self.assertLessEqual(words, 375, "the AGENTS template must leave the project ~75 words")

    def test_skill_templates_have_name_and_description(self) -> None:
        from helpers import ROOT
        skills = sorted((ROOT / "plantillas/skills").glob("*/SKILL.md"))
        self.assertEqual([p.parent.name for p in skills], ["cerrar-sesion", "con-tus-palabras"])
        for path in skills:
            head = path.read_text(encoding="utf-8").split("---")[1]
            self.assertIn(f"name: {path.parent.name}", head)
            self.assertIn("description: ", head)


class KernelCopyTests(unittest.TestCase):
    """4.0.0-rc.2 (SPEC-002, GPEXT trial): adopting the kernel must not break R02 by itself."""

    def test_the_kernel_copy_does_not_count(self) -> None:
        with in_temp_dir():
            start_repo()
            write_doc(".github/kernel.txt", 1)  # the project adopted the kernel (kernel_sync.py sync)
            commit_all()
            git("branch", "-f", "base")
            write_doc("docs/kernel/KERNEL.md", 300)
            write_lines("scripts/risk.py", 300)
            write_doc(".claude/skills/con-tus-palabras/SKILL.md", 50)
            write_lines(".github/workflows/pr-description.yml", 80)
            write_lines("scripts/own_tool.py", 7)  # the project's own script still counts
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), (7, 0))

    def test_the_list_matches_kernel_sync(self) -> None:
        import kernel_sync
        from helpers import ROOT
        outside_docs = {d for d in kernel_sync.fixed_files(ROOT).values() if not d.startswith("docs/kernel/")}
        self.assertEqual(size_check.KERNEL_COPY, outside_docs)
        with in_temp_dir():
            Path(".github").mkdir()
            Path(".github/kernel.txt").write_text("version v4.0.0\n", encoding="utf-8")
            for dest in kernel_sync.fixed_files(ROOT).values():
                self.assertTrue(size_check.is_kernel_copy(Path(dest)), dest)
            self.assertFalse(size_check.is_kernel_copy(Path("scripts/deploy.py")))
            self.assertFalse(size_check.is_kernel_copy(Path(".claude/skills/mia/SKILL.md")))

    def test_without_kernel_txt_nothing_is_a_kernel_copy(self) -> None:
        """In the kernel's own repo (no .github/kernel.txt) its workflow and scripts still count."""
        with in_temp_dir():
            start_repo()
            write_lines(".github/workflows/pr-description.yml", 30)
            write_lines("scripts/risk.py", 20)
            commit_all()
            self.assertEqual(size_check.changed_lines("base"), (50, 0))


if __name__ == "__main__":
    unittest.main()

"""risk.py must never LOWER a risk: one rejection test per finding of the independent review of #13."""

import subprocess
import unittest
from pathlib import Path

import helpers
import risk
from risk import FileChange


def level(*changes: FileChange) -> int:
    return risk.compute(list(changes))[0]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def repo_risk(base_files: dict[str, str], pr_edit: object) -> int:
    """Commit `base_files` on main, apply `pr_edit` on a branch, return the CLI's risk (or -exit code)."""
    with helpers.in_temp_dir() as repo:
        git("init", "-q", "-b", "main")
        git("config", "user.email", "t@example.invalid")
        git("config", "user.name", "Test")
        for name, text in base_files.items():
            (repo / name).parent.mkdir(parents=True, exist_ok=True)
            (repo / name).write_text(text)
        git("add", "-A")
        git("commit", "-qm", "main")
        git("checkout", "-qb", "pr")
        if callable(pr_edit):
            pr_edit(repo)
        git("add", "-A")
        git("commit", "-qm", "pr", "--allow-empty")
        out = subprocess.run(["python3", str(helpers.CI_DIR / "risk.py"), "main", "pr"],
                             capture_output=True, text=True)
    return int(out.stdout.split()[1]) if out.returncode == 0 else -out.returncode


PROTECTED = "@login_required\ndef v(r):\n    return r\n"


def unprotect(name: str) -> object:
    return lambda repo: (repo / name).write_text("def v(r):\n    return r\n")


class FileNameTests(unittest.TestCase):
    """Finding 1: names with spaces, accents, quotes or glob characters kept their lines hidden."""

    def test_removed_protection_is_seen_whatever_the_name(self) -> None:
        for name in ["dir con espacio/a b.py", "app/café.py", 'app/q"uote.py', "app/[x]*.py", "app/a\tb.py"]:
            self.assertEqual(repo_risk({name: PROTECTED}, unprotect(name)), 3, repr(name))

    def test_renamed_file_with_spaces_keeps_its_lines(self) -> None:
        def move(repo: Path) -> None:
            git("mv", "a b.py", "c d.py")
            (repo / "c d.py").write_text("def v(r):\n    return r\n")
        self.assertEqual(repo_risk({"a b.py": PROTECTED + "x = 1\n" * 8}, move), 3)

    def test_a_removed_line_that_starts_with_dashes_is_content(self) -> None:
        base = {"app/q.sql": "-- @login_required\nselect 1;\n", "app/v.py": "x = 1\n"}
        def edit(repo: Path) -> None:
            (repo / "app/q.sql").write_text("select 1;\n")
        self.assertEqual(repo_risk(base, edit), 3)


class WordTests(unittest.TestCase):
    """Finding 2: openings added, spaces, and missing alarm words."""

    def test_adding_an_opening_is_critical(self) -> None:
        for line in ["@csrf_exempt", "qs = M.objects.raw(sql)", "RawSQL(q, p)", "permission_classes = [AllowAny]"]:
            self.assertEqual(level(FileChange("api/views.py", added=[line])), 3, line)

    def test_switching_isauthenticated_to_allowany_is_critical(self) -> None:
        change = FileChange("api/views.py", removed=["permission_classes = [IsAuthenticated]"],
                            added=["permission_classes = [AllowAny]"])
        self.assertEqual(level(change), 3)

    def test_spaces_do_not_hide_an_alarm(self) -> None:
        for line in ["eval (x)", "exec  (code)", "run(c, shell = True)", "get(u, verify =False)", "{{ x | safe }}"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)

    def test_new_alarm_words(self) -> None:
        for line in ["@pytest.mark.skipif(True, reason='x')", "@unittest.skip('later')", "pytest.skip('x')",
                     "os.system(cmd)", "pickle.loads(blob)", "yaml.load(text)"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)

    def test_safe_lookalikes_do_not_alarm(self) -> None:
        for line in ["yaml.safe_load(text)", "skipping = True", "my_eval_(x)", "evaluate(x)"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 2, line)


class TestFileTests(unittest.TestCase):
    """Finding 3: renaming or emptying a test file disables it."""

    def test_renaming_a_test_out_of_the_test_names_is_critical(self) -> None:
        for new in ["tests/disabled.txt", "x_old.py"]:
            self.assertEqual(level(FileChange(new, "R", "tests/test_a.py")), 3, new)

    def test_renaming_a_test_to_another_test_is_normal(self) -> None:
        self.assertEqual(level(FileChange("tests/test_b.py", "R", "tests/test_a.py")), 2)

    def test_removing_test_functions_is_critical(self) -> None:
        change = FileChange("tests/test_a.py", removed=["def test_login():", "    assert ok"], added=[])
        self.assertEqual(level(change), 3)
        change = FileChange("tests/test_a.py", removed=["def test_x():"], added=["def test_x_renamed():"])
        self.assertEqual(level(change), 2)


class PathTests(unittest.TestCase):
    """Findings 4 and 7: critical files in subfolders, missing names, submodules."""

    def test_critical_files_anywhere(self) -> None:
        for path in ["services/api/package.json", "services/api/pyproject.toml", "requirements/base.txt",
                     "Makefile", ".gitmodules", ".gitattributes", "app/.gitattributes", "tests/conftest.py",
                     ".coveragerc", "CODEOWNERS", "manage.py", "setup.py", "setup.cfg", "tox.ini",
                     "Pipfile.lock", "Jenkinsfile", ".gitlab-ci.yml", "app/AGENTS.md"]:
            self.assertEqual(level(FileChange(path)), 3, path)

    def test_submodule_is_critical(self) -> None:
        self.assertEqual(level(FileChange("vendor-lib", "A", new_mode="160000")), 3)


class ExecutableAndBinaryTests(unittest.TestCase):
    """Finding 5: new executables and binaries, also inside docs/evidencia/."""

    def test_evidence_folder_accepts_only_its_formats(self) -> None:
        self.assertEqual(level(FileChange("docs/evidencia/a.sh", "A", new_mode="100755")), 3)
        self.assertEqual(level(FileChange("docs/evidencia/tool", "A", binary=True)), 3)
        self.assertEqual(level(FileChange("docs/evidencia/a.sh", "A")), 2)
        for path in ["docs/evidencia/a.md", "docs/evidencia/run.log", "docs/evidencia/2026/notes.txt"]:
            self.assertEqual(level(FileChange(path, "A")), 1, path)
        self.assertEqual(level(FileChange("docs/evidencia/shot.png", "A", binary=True)), 1)

    def test_executable_compiled_translation_is_critical(self) -> None:
        self.assertEqual(level(FileChange("locale/es/x.mo", "A", binary=True, new_mode="100755")), 3)

    def test_new_executable_without_extension_through_git(self) -> None:
        def add(repo: Path) -> None:
            (repo / "bin").mkdir()
            (repo / "bin" / "run").write_text("#!/bin/sh\necho hi\n")
            (repo / "bin" / "run").chmod(0o755)
        self.assertEqual(repo_risk({"a.txt": "a\n"}, add), 3)

    def test_script_without_extension_is_code(self) -> None:
        self.assertEqual(level(FileChange("bin/tool", added=["os.system(cmd)"])), 3)


class EmptyDiffTests(unittest.TestCase):
    """Finding 8: an empty diff must be an error, never risk 1."""

    def test_empty_diff_fails(self) -> None:
        self.assertEqual(repo_risk({"a.txt": "a\n"}, None), -1)


if __name__ == "__main__":
    unittest.main()

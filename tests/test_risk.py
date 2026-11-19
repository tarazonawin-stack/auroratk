"""Tests for perfiles/ci/risk.py (R12): the minimum risk a PR may declare."""

import subprocess
import unittest
from pathlib import Path

import helpers
import risk
from risk import FileChange


def level(*changes: FileChange, rules: str = "") -> int:
    return risk.compute(list(changes), rules)[0]


class RoutineTests(unittest.TestCase):
    def test_only_the_exact_list_is_routine(self) -> None:
        for path in ["docs/ESTADO.md", "CHANGELOG.md", "docs/evidencia/2026-11-19-restore.md"]:
            self.assertEqual(level(FileChange(path)), 1, path)

    def test_other_docs_and_unknown_paths_are_normal(self) -> None:
        for path in ["README.md", "docs/decisiones/DEC-001.md", "docs/ESTADO.md.bak", "x/y.unknown"]:
            self.assertEqual(level(FileChange(path)), 2, path)

    def test_evidence_image_is_routine_even_if_binary(self) -> None:
        self.assertEqual(level(FileChange("docs/evidencia/shot.png", "A", binary=True)), 1)

    def test_whole_change_takes_its_highest_file(self) -> None:
        self.assertEqual(level(FileChange("docs/ESTADO.md"), FileChange("app/views.py")), 2)
        self.assertEqual(level(FileChange("docs/ESTADO.md"), FileChange("AGENTS.md")), 3)


class CriticalPathTests(unittest.TestCase):
    def test_profile_critical_paths(self) -> None:
        for path in [".github/workflows/ci.yml", "scripts/check_size.py", "pyproject.toml", "uv.lock",
                     "Dockerfile", "compose.yaml", "docs/kernel/KERNEL.md", "docs/excepciones.md",
                     "AGENTS.md", "CLAUDE.md", ".claude/settings.json", "config/settings.py",
                     ".env.example", "config/wsgi.py", ".github/riesgo.txt"]:
            self.assertEqual(level(FileChange(path)), 3, path)

    def test_urls_is_not_critical_by_default(self) -> None:
        self.assertEqual(level(FileChange("config/urls.py")), 2)

    def test_project_can_add_critical_paths(self) -> None:
        rules = "# security files of the project\n3 org/roles.py\n3 org/scopes.py\n"
        self.assertEqual(level(FileChange("org/roles.py"), rules=rules), 3)
        self.assertEqual(level(FileChange("org/models.py"), rules=rules), 2)

    def test_project_cannot_lower_a_default(self) -> None:
        self.assertEqual(level(FileChange("AGENTS.md"), rules="1 AGENTS.md\n2 AGENTS.md\n"), 3)

    def test_rename_counts_old_and_new_path(self) -> None:
        self.assertEqual(level(FileChange("docs/notes.md", "R", "AGENTS.md")), 3)
        self.assertEqual(level(FileChange("AGENTS.md", "R", "docs/notes.md")), 3)
        self.assertEqual(level(FileChange("app/x.py", "R", "docs/ESTADO.md")), 2)


class FileKindTests(unittest.TestCase):
    def test_symlink_and_new_executable_are_critical(self) -> None:
        self.assertEqual(level(FileChange("link", "A", new_mode="120000")), 3)
        self.assertEqual(level(FileChange("app/x.py", "M", old_mode="100644", new_mode="100755")), 3)

    def test_new_executable_file_is_critical_too(self) -> None:
        self.assertEqual(level(FileChange("bin/run", "A", new_mode="100755")), 3)
        self.assertEqual(level(FileChange("app/x.py", "M", old_mode="100755", new_mode="100755")), 2)

    def test_binary_is_critical_except_compiled_translations(self) -> None:
        self.assertEqual(level(FileChange("app/blob.bin", "A", binary=True)), 3)
        self.assertEqual(level(FileChange("locale/es/LC_MESSAGES/django.mo", binary=True)), 2)

    def test_deleting_tests_is_critical_changing_them_is_not(self) -> None:
        self.assertEqual(level(FileChange("tests/test_login.py", "D")), 3)
        self.assertEqual(level(FileChange("shifts/tests/test_a.py", "D")), 3)
        self.assertEqual(level(FileChange("tests/test_login.py", "M")), 2)


class MigrationTests(unittest.TestCase):
    def test_adding_only_is_normal(self) -> None:
        change = FileChange("tickets/migrations/0008_x.py", "A",
                            added=["        migrations.AddField(model_name='t', name='n')"])
        self.assertEqual(level(change), 2)

    def test_removing_renaming_or_transforming_is_critical(self) -> None:
        for op in ["RemoveField", "RenameModel", "AlterField", "RunPython", "RunSQL", "DeleteModel"]:
            change = FileChange("tickets/migrations/0008_x.py", "A", added=[f"        migrations.{op}("])
            self.assertEqual(level(change), 3, op)

    def test_deleting_a_migration_is_critical(self) -> None:
        self.assertEqual(level(FileChange("tickets/migrations/0007_y.py", "D")), 3)


class PermissionTests(unittest.TestCase):
    def test_removed_or_changed_protection_is_critical(self) -> None:
        change = FileChange("tickets/views.py", removed=["@login_required"], added=["@never_cache"])
        self.assertEqual(level(change), 3)
        self.assertEqual(level(FileChange("a/views.py", removed=["class V(LoginRequiredMixin, View):"])), 3)

    def test_adding_a_protection_is_not_a_risk(self) -> None:
        self.assertEqual(level(FileChange("tickets/views.py", added=["@login_required"])), 2)

    def test_only_code_counts(self) -> None:
        self.assertEqual(level(FileChange("docs/guia.md", removed=["usa @login_required"])), 2)


class AlarmTests(unittest.TestCase):
    def test_alarm_words_in_added_code(self) -> None:
        for line in ["x = eval(data)", "subprocess.run(c, shell=True)", "requests.get(u, verify=False)",
                     "@pytest.mark.skip", "@pytest.mark.xfail", "return mark_safe(s)"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)
        self.assertEqual(level(FileChange("app/t.html", added=["{{ body|safe }}"])), 3)

    def test_whole_word_only(self) -> None:
        for line in ["medieval(x)", "x = evaluate(y)", "my_exec(z)", "shell=True_ish = 1"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 2, line)

    def test_removed_lines_and_documents_do_not_alarm(self) -> None:
        self.assertEqual(level(FileChange("app/x.py", removed=["eval(x)"])), 2)
        self.assertEqual(level(FileChange("docs/seguridad.md", added=["nunca uses eval("])), 2)

    def test_project_can_add_alarm_words(self) -> None:
        change = FileChange("app/x.py", added=["subprocess.Popen(cmd)"])
        self.assertEqual(level(change), 2)
        self.assertEqual(level(change, rules="alarma subprocess.Popen(\n"), 3)

    def test_reasons_name_the_file_and_the_word(self) -> None:
        _, reasons = risk.compute([FileChange("app/x.py", added=["eval(s)"])])
        self.assertEqual(reasons, [("app/x.py", 3, "alarma «eval(» · alarm word")])


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True)


class GitAdapterTests(unittest.TestCase):
    """Build a real repository and read its diff the way CI does."""

    def test_reads_renames_deletions_binaries_modes_and_lines(self) -> None:
        with helpers.in_temp_dir() as repo:
            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.invalid")
            git("config", "user.name", "Test")
            (repo / "tests").mkdir()
            (repo / "tests" / "test_a.py").write_text("def test_a():\n    assert True\n")
            (repo / "views.py").write_text("@login_required\ndef v(r):\n    return r\n")
            (repo / "run.py").write_text("print('hi')\n" * 5)
            (repo / "notes.md").write_text("una nota larga que se mueve de lugar\n" * 5)
            git("add", "-A")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "pr")
            (repo / "tests" / "test_a.py").unlink()
            (repo / "views.py").write_text("def v(r):\n    return r\n")
            (repo / "run.py").chmod(0o755)
            (repo / "blob.bin").write_bytes(bytes(range(256)))
            git("mv", "notes.md", "AGENTS.md")
            git("add", "-A")
            git("commit", "-qm", "pr")
            changes = {c.path: c for c in risk.changes_from_git("main", "pr")}
        self.assertEqual(changes["tests/test_a.py"].status, "D")
        self.assertEqual(changes["AGENTS.md"].old_path, "notes.md")
        self.assertTrue(changes["blob.bin"].binary)
        self.assertEqual(changes["run.py"].new_mode, "100755")
        self.assertIn("@login_required", changes["views.py"].removed)
        self.assertIn("    assert True", changes["tests/test_a.py"].removed)
        reasons = {path: lvl for path, lvl, _ in risk.compute(list(changes.values()))[1]}
        self.assertEqual(reasons, {"tests/test_a.py": 3, "views.py": 3, "run.py": 3, "blob.bin": 3,
                                   "AGENTS.md": 3})

    def test_cli_prints_the_risk(self) -> None:
        with helpers.in_temp_dir() as repo:
            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.invalid")
            git("config", "user.name", "Test")
            Path("docs").mkdir()
            Path("docs/ESTADO.md").write_text("a\n")
            git("add", "-A")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "pr")
            Path("docs/ESTADO.md").write_text("b\n")
            git("commit", "-qam", "pr")
            out = subprocess.run(["python3", str(helpers.CI_DIR / "risk.py"), "main", "pr"],
                                 capture_output=True, text=True, cwd=repo)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(out.stdout.strip(), "Riesgo 1")


if __name__ == "__main__":
    unittest.main()

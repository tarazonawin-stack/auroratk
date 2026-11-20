"""Second round: one rejection test per case the independent review found still at risk 2 (A3)."""

import subprocess
import unittest
from pathlib import Path

import helpers
import pr_check
import risk
from risk import FileChange
from test_pr_check import filled
from test_risk_hardening import git, repo_risk


def level(*changes: FileChange) -> int:
    return risk.compute(list(changes))[0]


class UnicodeTests(unittest.TestCase):
    def test_full_width_letters_do_not_hide_an_alarm(self) -> None:
        for line in ["x = ｅval(y)", "ｅxec(code)", "@csrf_ｅxempt"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)

    def test_full_width_letters_do_not_hide_a_removed_protection(self) -> None:
        self.assertEqual(level(FileChange("app/x.py", removed=["@ｌogin_required"])), 3)


class ConfigAndManifestTests(unittest.TestCase):
    def test_test_runner_settings_and_other_manifests_are_critical(self) -> None:
        for path in ["pytest.ini", "app/pytest.ini", "pom.xml", "svc/build.gradle.kts", "go.mod", "go.sum",
                     "Cargo.toml", "Cargo.lock", "CMakeLists.txt", "App.csproj", "Gemfile.lock", "composer.json",
                     ".npmrc", "web/.npmrc", ".env.production", "app/local_settings.py", "Dockerfile.prod",
                     "web.dockerfile", "jest.config.js", "vitest.config.ts", ".mocharc.yml", "noxfile.py"]:
            self.assertEqual(level(FileChange(path)), 3, path)


class DisabledTestsTests(unittest.TestCase):
    def test_renaming_a_test_so_runners_skip_it_is_critical(self) -> None:
        for new in ["tests/a.py", "tests/check_login.py", "app/tests/helpers_old.py"]:
            self.assertEqual(level(FileChange(new, "R", "tests/test_a.py")), 3, new)
        self.assertEqual(level(FileChange("tests/test_b.py", "R", "tests/test_a.py")), 2)

    def test_renaming_a_test_class_or_dropping_testcase_is_critical(self) -> None:
        self.assertEqual(level(FileChange("tests/test_a.py", removed=["class TestB:"], added=["class B:"])), 3)
        change = FileChange("tests/test_a.py", removed=["class TestA(unittest.TestCase):"], added=["class TestA:"])
        self.assertEqual(level(change), 3)


class CodeSuffixTests(unittest.TestCase):
    def test_more_code_suffixes_and_upper_case(self) -> None:
        for path in ["app/x.cjs", "app/x.mts", "app/x.wsgi", "bin/x.bash", "static/APP.JS", "app/X.PY"]:
            self.assertEqual(level(FileChange(path, added=["eval(x)"])), 3, path)


class PatternTests(unittest.TestCase):
    def test_sql_built_from_text(self) -> None:
        for line in ["cursor.execute('select ' + x)", 'cursor.execute(f"select {x}")', "c.execute(q + x)",
                     "cursor.execute('select %s' % x)", "cursor.execute('select {}'.format(x))"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)

    def test_parameterised_sql_is_normal(self) -> None:
        self.assertEqual(level(FileChange("app/x.py", added=["cursor.execute('select %s', [x])"])), 2)

    def test_truthy_shell_and_disabled_verify(self) -> None:
        for line in ["run(c, shell=1)", "run(c, shell='yes')", "run(c, shell=flag)", "get(u, verify=0)",
                     "get(u, verify=None)", "__import__('os').system(c)", "pickle.load(f)", "yaml.unsafe_load(t)"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 3, line)

    def test_shell_false_is_normal(self) -> None:
        for line in ["run(c, shell=False)", "run(c, shell=0)", "get(u, verify=True)"]:
            self.assertEqual(level(FileChange("app/x.py", added=[line])), 2, line)

    def test_more_permission_words(self) -> None:
        for line in ["@staff_member_required", "permission_classes = [IsAdminUser]", "if request.user.is_staff:"]:
            self.assertEqual(level(FileChange("app/views.py", removed=[line])), 3, line)


class FileNameTests(unittest.TestCase):
    def test_name_with_a_newline_keeps_its_lines(self) -> None:
        name = "app/x\n::warning::pwned.py"
        self.assertEqual(repo_risk({"a.txt": "a\n"}, lambda repo: (repo / name).parent.mkdir(exist_ok=True)
                                   or (repo / name).write_text("x = eval(y)\n")), 3)

    def test_non_utf8_content_and_names_do_not_stop_the_check(self) -> None:
        def latin1(repo: Path) -> None:
            (repo / "app").mkdir()
            (repo / "app" / "x.py").write_bytes("# café\nx = eval(y)\n".encode("latin-1"))
            (repo / "app" / "caf\udce9.py").write_bytes(b"print(1)\n")
        self.assertEqual(repo_risk({"a.txt": "a\n"}, latin1), 3)

    def test_safe_escapes_undecodable_bytes(self) -> None:
        self.assertEqual(risk.safe("caf\udce9\n.py"), "caf\\xe9\\x0a.py")


class DuplicateReportTests(unittest.TestCase):
    """Finding 1 of the second review of #14: a fake report before the template's one."""

    def test_a_second_technical_or_owner_report_is_an_error(self) -> None:
        for title in ["## Informe técnico\n- **Cambios:** x\n", "## Informe para el dueño\n- **Qué cambia:** x\n"]:
            body = title + "\n" + filled(2)
            self.assertTrue(any("más de un título" in p for p in pr_check.problems(body, 2)), title)


if __name__ == "__main__":
    unittest.main()

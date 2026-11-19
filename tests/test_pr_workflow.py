"""Security of perfiles/ci/pr-description.yml (R12): a PR can never lower its own risk."""

import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path

import helpers
import risk

WORKFLOW = (helpers.CI_DIR / "pr-description.yml").read_text(encoding="utf-8")


def step_script(name: str) -> str:
    """The shell script of the workflow step whose name starts with `name`."""
    pattern = rf"- name: {re.escape(name)}[^\n]*\n(?:(?!\s+- name:).*\n)*?\s+run: \|\n((?:\s{{10}}.*\n)+)"
    match = re.search(pattern, WORKFLOW)
    assert match is not None, name
    return "\n".join(line[10:] for line in match.group(1).splitlines())


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


class WorkflowShapeTests(unittest.TestCase):
    def test_runs_on_pull_request_target_only(self) -> None:
        on = WORKFLOW.split("\non:\n", 1)[1].split("\n\n", 1)[0]
        self.assertIn("pull_request_target:", on)
        self.assertNotRegex(on, r"^\s+pull_request:", "pull_request would run the PR's own scripts")

    def test_token_can_only_read(self) -> None:
        block = WORKFLOW.split("\npermissions:\n", 1)[1].split("\n\n", 1)[0]
        self.assertEqual(sorted(line.strip() for line in block.splitlines()),
                         ["contents: read", "pull-requests: read"])

    def test_never_checks_out_the_pr(self) -> None:
        self.assertNotRegex(WORKFLOW, r"^\s+ref:", "checkout must stay on the main branch")
        self.assertNotIn("head.ref", WORKFLOW)
        self.assertIn("refs/remotes/pr/head", WORKFLOW)

    def test_event_values_only_go_through_env(self) -> None:
        for line in WORKFLOW.splitlines():
            if "${{" in line and not line.lstrip().startswith("#"):
                if line.strip().startswith("group: "):
                    self.assertEqual(line.strip(), "group: pr-description-${{ github.event.pull_request.number }}")
                    continue
                self.assertRegex(line, r"^\s+[A-Z_]+: \$\{\{ [^}]+ \}\}$", line)

    def test_only_the_reviewed_steps_exist(self) -> None:
        steps = re.findall(r"^      - (?:name|uses): (.*)$", WORKFLOW, re.MULTILINE)
        self.assertEqual(steps, [
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0",
            "Fetch the PR commits as data (never checked out or run)",
            "R12 · Riesgo calculado (diff completo desde el merge-base)",
            "R12 · Descripción del PR",
        ], "a new step must be reviewed for security first (see the header of the workflow)")
        self.assertEqual(len(re.findall(r"^        run:", WORKFLOW, re.MULTILINE)), 3)  # step-level runs only

    def test_latest_run_wins_and_bash_uses_pipefail(self) -> None:
        self.assertIn("cancel-in-progress: true", WORKFLOW)
        self.assertIn("shell: bash", WORKFLOW)

    def test_django_ci_no_longer_runs_the_prs_pr_check(self) -> None:
        self.assertNotIn("pr_check.py", (helpers.CI_DIR / "python-django.yml").read_text(encoding="utf-8")
                         .split("jobs:", 1)[1])


class RiskStepTests(unittest.TestCase):
    """Run the workflow's real risk step against a repository where the PR attacks the check."""

    def run_step(self, edit_pr: object) -> str:
        with helpers.in_temp_dir() as repo:
            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.invalid")
            git("config", "user.name", "Test")
            (repo / "scripts").mkdir()
            shutil.copy(helpers.CI_DIR / "risk.py", repo / "scripts" / "risk.py")
            (repo / "app.py").write_text("x = 1\n")
            git("add", "-A")
            git("commit", "-qm", "main")
            base = git("rev-parse", "HEAD")
            git("checkout", "-qb", "pr")
            if callable(edit_pr):
                edit_pr(repo)
            git("add", "-A")
            git("commit", "-qm", "pr")
            head = git("rev-parse", "HEAD")
            git("checkout", "-q", "main")  # CI works on the main branch, the PR is only data
            env_file = repo / "github_env"
            env = {**os.environ, "BASE_SHA": base, "HEAD_SHA": head, "RUNNER_TEMP": str(repo),
                   "GITHUB_ENV": str(env_file)}
            subprocess.run(["bash", "-eo", "pipefail", "-c", step_script("R12 · Riesgo calculado")],
                           check=True, capture_output=True, env=env)
            return env_file.read_text()

    def test_a_pr_that_rewrites_risk_py_still_gets_risk_3(self) -> None:
        def cheat(repo: Path) -> None:
            (repo / "scripts" / "risk.py").write_text("print('Riesgo 1')\n")
        self.assertEqual(self.run_step(cheat), "COMPUTED_RISK=3\n")

    def test_a_pr_that_adds_a_risk_file_cannot_lower_its_risk(self) -> None:
        def cheat(repo: Path) -> None:
            (repo / ".github").mkdir()
            (repo / ".github" / "riesgo.txt").write_text("1 app.py\n")
            (repo / "app.py").write_text("x = eval(input())\n")
        self.assertEqual(self.run_step(cheat), "COMPUTED_RISK=3\n")

    def test_the_attacks_of_the_review_get_risk_3(self) -> None:
        def spaced(repo: Path) -> None:
            (repo / "dir con espacio").mkdir()
            (repo / "dir con espacio" / "a b.py").write_text("@csrf_exempt\ndef v(r):\n    return r\n")
        def executable(repo: Path) -> None:
            (repo / "tool").write_text("#!/bin/sh\necho hi\n")
            (repo / "tool").chmod(0o755)
        for name, attack in [("espacio + csrf_exempt", spaced), ("ejecutable nuevo", executable),
                             ("csrf_exempt", lambda r: (r / "app.py").write_text("@csrf_exempt\nx = 1\n")),
                             ("eval con espacio", lambda r: (r / "app.py").write_text("x = eval (y)\n"))]:
            self.assertEqual(self.run_step(attack), "COMPUTED_RISK=3\n", name)

    def test_a_normal_change_is_risk_2(self) -> None:
        self.assertEqual(self.run_step(lambda repo: (repo / "app.py").write_text("x = 2\n")),
                         "COMPUTED_RISK=2\n")


class LogSafetyTests(unittest.TestCase):
    def test_file_names_cannot_start_a_log_line(self) -> None:
        name = "a\n::error::fake\r.py"
        self.assertNotIn("\n", risk.safe(name))
        self.assertTrue(risk.safe(name).startswith("a\\x0a::error::"))
        self.assertEqual(risk.safe("ruta crítica · añadir"), "ruta crítica · añadir")


class KernelRiskFileTests(unittest.TestCase):
    def test_the_kernel_repo_treats_its_own_controls_as_risk_3(self) -> None:
        rules = (helpers.ROOT / ".github" / "riesgo.txt").read_text(encoding="utf-8")
        for path in ["KERNEL.md", "perfiles/ci/pr_check.py", "plantillas/PULL_REQUEST_TEMPLATE.md",
                     "guias/lo-entiendo.md", "SHA256SUMS", "tests/test_risk.py"]:
            self.assertEqual(risk.compute([risk.FileChange(path)], rules)[0], 3, path)
        self.assertEqual(risk.compute([risk.FileChange("README.md")], rules)[0], 2)


if __name__ == "__main__":
    unittest.main()

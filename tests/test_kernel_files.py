"""Consistency of the kernel files themselves: checksums, versions and links."""

import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT

SUMS = ROOT / "SHA256SUMS"
VERSION = re.compile(r"\*\*Versi[oó]n (\d+\.\d+\.\d+)\*\*")
LINK_REF = re.compile(r"github\.com/tarazonawin-stack/auroratk/(?:blob|tree)/([^/)\s]+)")
KERNEL_MENTION = re.compile(r"Kernel\D{0,6}v(\d+\.\d+\.\d+)")
LEAVING_PERFILES = re.compile(r"\]\((?:\.\./|ci/)")


def kernel_files() -> list[str]:
    """Files a project copies into docs/kernel/: they must match SHA256SUMS."""
    profiles = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "perfiles").glob("*.md"))
    return ["KERNEL.md", "KERNEL.en.md", *profiles]


def text_files() -> list[str]:
    names = [p for ext in ("*.md", "*.yml", "*.toml", "*.json") for p in ROOT.rglob(ext)]
    return [p.relative_to(ROOT).as_posix() for p in names
            if ".git" not in p.parts and p.name != "CHANGELOG.md"]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def current_version() -> str:
    match = VERSION.search(read("KERNEL.md"))
    assert match is not None, "KERNEL.md has no version header"
    return match.group(1)


class ChecksumTests(unittest.TestCase):
    def test_sums_list_exactly_the_copied_kernel_files(self) -> None:
        listed = [line.split("  ", 1)[1] for line in SUMS.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(listed, kernel_files())

    def test_sums_match_file_contents(self) -> None:
        for line in SUMS.read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            self.assertEqual(digest, actual, f"{name} changed: regenerate SHA256SUMS")


class VersionTests(unittest.TestCase):
    def test_english_kernel_and_changelog_carry_the_same_version(self) -> None:
        version = current_version()
        self.assertIn(f"**Version {version}**", read("KERNEL.en.md"))
        latest = re.search(r"^## \[(\d+\.\d+\.\d+)\]", read("CHANGELOG.md"), re.MULTILINE)
        self.assertIsNotNone(latest)
        assert latest is not None
        self.assertEqual(latest.group(1), version, "CHANGELOG's latest entry")

    def test_chat_versions_and_readmes_carry_the_same_version(self) -> None:
        version = current_version()
        for name in ["KERNEL-CHAT.md", "KERNEL-CHAT.en.md"]:
            self.assertIn(f"(v{version})", read(name).splitlines()[0], name)
        self.assertIn(f"**Versión {version}.**", read("README.md"))
        self.assertIn(f"**Version {version}.**", read("README.en.md"))

    def test_citation_file_carries_the_same_version(self) -> None:
        self.assertIn(f'version: "{current_version()}"', read("CITATION.cff").splitlines())

    def test_every_kernel_mention_uses_the_current_version(self) -> None:
        version = current_version()
        for name in text_files():
            for found in KERNEL_MENTION.findall(read(name)):
                self.assertEqual(found, version, name)

    def test_links_point_to_the_current_tag_spelled_vX_Y_Z(self) -> None:
        tag = f"v{current_version()}"
        for name in text_files():
            for ref in LINK_REF.findall(read(name)):
                self.assertEqual(ref, tag, f"{name} links to {ref}")


RULE_HEADING = re.compile(r"^\*\*(R\d{2}) ·", re.MULTILINE)
README_RULE_ROW = re.compile(r"^\| (R\d{2}) \|", re.MULTILINE)


class ReadmeRulesTests(unittest.TestCase):
    """The plain-words rule table in each README lists exactly the kernel's rules."""

    def test_readme_tables_list_every_kernel_rule(self) -> None:
        for kernel, readme, title in [("KERNEL.md", "README.md", "## Las {n} reglas"),
                                      ("KERNEL.en.md", "README.en.md", "## The {n} rules")]:
            rules = sorted(RULE_HEADING.findall(read(kernel)))
            self.assertEqual(sorted(README_RULE_ROW.findall(read(readme))), rules, readme)
            self.assertIn(title.format(n=len(rules)), read(readme), readme)


class WorkflowTests(unittest.TestCase):
    def test_every_action_is_pinned_to_a_full_commit_sha(self) -> None:
        uses = re.compile(r"uses:\s*([^\s#]+)")
        found = 0
        for path in [*ROOT.rglob("*.yml"), *ROOT.rglob("*.yaml")]:
            for ref in uses.findall(path.read_text(encoding="utf-8")):
                found += 1
                self.assertRegex(ref, r"@[0-9a-f]{40}$", f"{path.name}: pin {ref} to a commit SHA")
        self.assertGreater(found, 0)


def kernel_copy_step() -> str:
    """The shell script of the kernel-copy step in the Django CI template."""
    text = read("perfiles/ci/python-django.yml")
    match = re.search(r"- name: Kernel copy.*?\n( +)run: \|\n", text, re.DOTALL)
    assert match is not None, "the kernel-copy step is missing from python-django.yml"
    body = []
    for line in text[match.end():].splitlines():
        if len(line) - len(line.lstrip()) <= len(match.group(1)):
            break  # the block ends where the indentation goes back to the step's level
        body.append(line.strip())
    return "\n".join(body)


def git_in(folder: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(folder), *args], check=True, capture_output=True)


class KernelCopyStepTests(unittest.TestCase):
    """Run the real CI step: fetch a tagged kernel, then run that kernel's own check."""

    def run_step(self, damage: object = None) -> subprocess.CompletedProcess[str]:
        import kernel_sync
        with tempfile.TemporaryDirectory() as folder:
            kernel, project, temp = Path(folder, "kernel"), Path(folder, "project"), Path(folder, "t")
            tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"],
                                     check=True, capture_output=True, text=True).stdout.splitlines()
            for name in tracked:
                if (ROOT / name).is_file():
                    (kernel / name).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(ROOT / name, kernel / name)
            git_in(kernel, "init", "-q")
            git_in(kernel, "add", ".")
            git_in(kernel, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "k")
            git_in(kernel, "tag", f"v{current_version()}")
            project.mkdir()
            temp.mkdir()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.chdir(project):
                kernel_sync.main(["sync", "--from", str(kernel)])
                if callable(damage):
                    damage()
            env = {**os.environ, "KERNEL_REPO": str(kernel), "RUNNER_TEMP": str(temp)}
            return subprocess.run(["bash", "-c", kernel_copy_step()], cwd=project, env=env,
                                  capture_output=True, text=True)

    def test_exact_copy_passes(self) -> None:
        result = self.run_step()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Kernel copy OK", result.stdout)

    def test_edited_script_fails(self) -> None:
        def edit() -> None:
            Path("scripts/risk.py").write_text("print(1)\n", encoding="utf-8")
        result = self.run_step(edit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scripts/risk.py", result.stdout)

    def test_bad_version_line_fails_before_fetching(self) -> None:
        def pin() -> None:
            Path(".github/kernel.txt").write_text("version $(touch pwned)\n", encoding="utf-8")
        result = self.run_step(pin)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bad version line", result.stdout)

    def test_step_runs_the_fetched_kernels_script_not_the_projects(self) -> None:
        step = kernel_copy_step()
        self.assertIn('python3 -I "$kernel/perfiles/ci/kernel_sync.py" check', step)
        self.assertNotIn("scripts/kernel_sync.py", step)


class CopyableProfilesTests(unittest.TestCase):
    def test_profiles_have_no_relative_links_that_break_once_copied(self) -> None:
        for path in (ROOT / "perfiles").glob("*.md"):
            self.assertIsNone(LEAVING_PERFILES.search(path.read_text(encoding="utf-8")),
                              f"{path.name}: use a pinned absolute link to the kernel repo")


class ExamplesTests(unittest.TestCase):
    def test_python_examples_compile(self) -> None:
        """The examples cannot run here (no Django), but they must at least be valid Python."""
        examples = sorted((ROOT / "ejemplos").glob("*.py"))
        self.assertTrue(examples)
        for path in examples:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")


if __name__ == "__main__":
    unittest.main()

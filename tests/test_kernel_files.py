"""Consistency of the kernel files themselves: checksums, versions and links."""

import hashlib
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
    """The exact shell command of the kernel-copy step in the Django CI template."""
    text = read("perfiles/ci/python-django.yml")
    match = re.search(r"- name: Kernel copy.*?\n\s+run: (.+)", text, re.DOTALL)
    assert match is not None, "the kernel-copy step is missing from python-django.yml"
    return match.group(1).splitlines()[0]


class KernelCopyStepTests(unittest.TestCase):
    """Run the real CI step against good and broken copies of docs/kernel/."""

    def run_step(self, prepare: object = None) -> int:
        with tempfile.TemporaryDirectory() as folder:
            copy = Path(folder)
            for name in kernel_files():
                (copy / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(ROOT / name, copy / name)
            shutil.copy(SUMS, copy / "SHA256SUMS")
            if callable(prepare):
                prepare(copy)
            result = subprocess.run(["bash", "-eo", "pipefail", "-c", kernel_copy_step()],
                                    cwd=copy, capture_output=True)
            return result.returncode

    def test_exact_copy_passes(self) -> None:
        self.assertEqual(self.run_step(), 0)

    def test_edited_file_fails(self) -> None:
        def edit(copy: Path) -> None:
            with (copy / "KERNEL.en.md").open("a", encoding="utf-8") as f:
                f.write("edited\n")
        self.assertNotEqual(self.run_step(edit), 0)

    def test_missing_profile_fails(self) -> None:
        self.assertNotEqual(self.run_step(lambda c: (c / "perfiles/pais-peru.md").unlink()), 0)

    def test_missing_english_kernel_fails(self) -> None:
        self.assertNotEqual(self.run_step(lambda c: (c / "KERNEL.en.md").unlink()), 0)

    def test_extra_file_fails(self) -> None:
        self.assertNotEqual(self.run_step(lambda c: (c / "perfiles/nuevo.md").write_text("x")), 0)

    def test_profiles_in_the_wrong_folder_fail(self) -> None:
        def flatten(copy: Path) -> None:
            for path in (copy / "perfiles").glob("*.md"):
                path.rename(copy / path.name)
        self.assertNotEqual(self.run_step(flatten), 0)

    def test_missing_checksum_file_fails(self) -> None:
        self.assertNotEqual(self.run_step(lambda c: (c / "SHA256SUMS").unlink()), 0)


class ProfileScriptStyleTests(unittest.TestCase):
    def test_ci_scripts_fit_the_django_profile_line_length(self) -> None:
        """Projects copy these scripts and lint them with line-length 100 (pyproject-django.toml)."""
        for path in (ROOT / "perfiles" / "ci").glob("*.py"):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                self.assertLessEqual(len(line), 100, f"{path.name}:{number}")


class CopyableProfilesTests(unittest.TestCase):
    def test_profiles_have_no_relative_links_that_break_once_copied(self) -> None:
        for path in (ROOT / "perfiles").glob("*.md"):
            self.assertIsNone(LEAVING_PERFILES.search(path.read_text(encoding="utf-8")),
                              f"{path.name}: use a pinned absolute link to the kernel repo")


if __name__ == "__main__":
    unittest.main()

"""Consistency of the kernel files themselves: checksums, versions and links."""

import hashlib
import re
import unittest

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


class CopyableProfilesTests(unittest.TestCase):
    def test_profiles_have_no_relative_links_that_break_once_copied(self) -> None:
        for path in (ROOT / "perfiles").glob("*.md"):
            self.assertIsNone(LEAVING_PERFILES.search(path.read_text(encoding="utf-8")),
                              f"{path.name}: use a pinned absolute link to the kernel repo")


if __name__ == "__main__":
    unittest.main()

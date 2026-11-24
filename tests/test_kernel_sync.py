"""Tests for perfiles/ci/kernel_sync.py: adopt the kernel and keep the copy exact (4.0.0)."""

import contextlib
import io
import json
import unittest
from pathlib import Path

from helpers import ROOT, in_temp_dir

import kernel_sync


def run(*args: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = kernel_sync.main([*args, "--from", str(ROOT)])
    return code, out.getvalue()


class SyncTests(unittest.TestCase):
    def test_sync_then_check_passes(self) -> None:
        with in_temp_dir():
            self.assertEqual(run("sync", "--ci", "python-django")[0], 0)
            code, out = run("check")
            self.assertEqual(code, 0, out)
            for name in ["docs/kernel/KERNEL.md", "docs/kernel/perfiles/pais-peru.md", "scripts/risk.py",
                         "scripts/size_hook.py", ".github/workflows/pr-description.yml",
                         ".github/workflows/ci.yml", ".claude/skills/con-tus-palabras/SKILL.md",
                         "AGENTS.md", "docs/datos-reales.md", ".claude/settings.json"]:
                self.assertTrue(Path(name).is_file(), name)
            version = kernel_sync.kernel_version(ROOT)
            self.assertEqual(Path(".github/kernel.txt").read_text(encoding="utf-8"),
                             f"version v{version}\nci python-django\n")

    def test_sync_never_overwrites_the_projects_templates(self) -> None:
        with in_temp_dir():
            Path("AGENTS.md").write_text("mine\n", encoding="utf-8")
            run("sync")
            self.assertEqual(Path("AGENTS.md").read_text(encoding="utf-8"), "mine\n")

    def test_sync_restores_edited_kernel_files_and_drops_old_ones(self) -> None:
        with in_temp_dir():
            run("sync")
            Path("scripts/risk.py").write_text("weakened\n", encoding="utf-8")
            Path("docs/kernel/perfiles/viejo.md").write_text("old\n", encoding="utf-8")
            run("sync")
            self.assertEqual(Path("scripts/risk.py").read_bytes(),
                             (ROOT / "perfiles/ci/risk.py").read_bytes())
            self.assertFalse(Path("docs/kernel/perfiles/viejo.md").exists())

    def test_ref_can_pin_a_trial_tag_and_unsafe_names_are_refused(self) -> None:
        version = kernel_sync.kernel_version(ROOT)
        with in_temp_dir():
            run("sync", "--ref", f"v{version}-rc.1")
            self.assertEqual(kernel_sync.read_pin()["version"], f"v{version}-rc.1")
            self.assertEqual(run("check")[0], 0)
            with self.assertRaises(SystemExit):
                run("sync", "--ref", "0123abcd")
            with self.assertRaises(SystemExit):
                run("sync", "--ref", "v1; rm -rf /")


class CheckTests(unittest.TestCase):
    def broken(self, damage: object) -> str:
        with in_temp_dir():
            run("sync")
            assert callable(damage)
            damage()
            code, out = run("check")
            self.assertEqual(code, 1, out)
            return out

    def test_edited_script_fails(self) -> None:
        def edit() -> None:
            with Path("scripts/pr_check.py").open("a", encoding="utf-8") as f:
                f.write("# looser\n")
        self.assertIn("edited (the kernel's files are not changed in the project): scripts/pr_check.py",
                      self.broken(edit))

    def test_missing_kernel_skill_fails(self) -> None:
        out = self.broken(lambda: Path(".claude/skills/cerrar-sesion/SKILL.md").unlink())
        self.assertIn("missing: .claude/skills/cerrar-sesion/SKILL.md", out)

    def test_extra_file_in_docs_kernel_fails(self) -> None:
        out = self.broken(lambda: Path("docs/kernel/nota.md").write_text("x", encoding="utf-8"))
        self.assertIn("extra file in docs/kernel/: docs/kernel/nota.md", out)

    def test_removed_hook_or_deny_rule_fails(self) -> None:
        def loosen() -> None:
            path = Path(".claude/settings.json")
            settings = json.loads(path.read_text(encoding="utf-8"))
            settings["permissions"]["deny"].remove("Bash(git push --force:*)")
            del settings["hooks"]
            path.write_text(json.dumps(settings), encoding="utf-8")
        out = self.broken(loosen)
        self.assertIn("deny rule removed: Bash(git push --force:*)", out)
        self.assertIn("the R02 size hook is missing", out)

    def test_project_may_add_its_own_skills_and_allow_rules(self) -> None:
        with in_temp_dir():
            run("sync")
            Path(".claude/skills/mia/SKILL.md").parent.mkdir(parents=True)
            Path(".claude/skills/mia/SKILL.md").write_text("---\nname: mia\n---\n", encoding="utf-8")
            path = Path(".claude/settings.json")
            settings = json.loads(path.read_text(encoding="utf-8"))
            settings["permissions"]["allow"] = ["Bash(uv run pytest:*)"]
            path.write_text(json.dumps(settings), encoding="utf-8")
            self.assertEqual(run("check")[0], 0)

    def test_pinned_version_must_match_the_kernel_given(self) -> None:
        def pin_old() -> None:
            Path(".github/kernel.txt").write_text("version v1.0.0\n", encoding="utf-8")
        self.assertIn("pins v1.0.0", self.broken(pin_old))


class ReviewFixesTests(unittest.TestCase):
    """Findings of the independent review of 4.0.0: each test failed before its fix."""

    def check_with(self, change: object) -> tuple[int, str]:
        with in_temp_dir():
            run("sync")
            assert callable(change)
            change()
            return run("check")

    def test_only_release_tags_can_be_pinned(self) -> None:
        for ref in ["refs/pull/1/head", "main", "0123abcd" * 5, "v4.0"]:
            def pin(ref: str = ref) -> None:
                Path(".github/kernel.txt").write_text(f"version {ref}\n", encoding="utf-8")
            code, out = self.check_with(pin)
            self.assertEqual(code, 1, ref)
            self.assertIn("pin a release tag", out)

    def test_a_release_candidate_tag_of_the_same_version_is_accepted(self) -> None:
        version = kernel_sync.kernel_version(ROOT)
        def pin() -> None:
            Path(".github/kernel.txt").write_text(f"version v{version}-rc.1\n", encoding="utf-8")
        self.assertEqual(self.check_with(pin)[0], 0)

    def test_disabled_hooks_or_bypass_mode_fail(self) -> None:
        for key, value in [("disableAllHooks", True), ("permissions.defaultMode", "bypassPermissions")]:
            def loosen(key: str = key, value: object = value) -> None:
                path = Path(".claude/settings.json")
                settings = json.loads(path.read_text(encoding="utf-8"))
                if key.startswith("permissions."):
                    settings["permissions"][key.split(".")[1]] = value
                else:
                    settings[key] = value
                path.write_text(json.dumps(settings), encoding="utf-8")
            code, out = self.check_with(loosen)
            self.assertEqual(code, 1, key)
            self.assertIn(key.split(".")[-1], out)

    def test_sync_refuses_a_symlinked_kernel_folder(self) -> None:
        with in_temp_dir() as folder:
            outside = folder / "outside"
            outside.mkdir()
            (outside / "keep.txt").write_text("mine", encoding="utf-8")
            Path("project").mkdir()
            import os
            os.chdir("project")
            Path("docs").mkdir()
            Path("docs/kernel").symlink_to(outside)
            with self.assertRaises(SystemExit):
                run("sync")
            self.assertTrue((outside / "keep.txt").exists())

    def test_sync_says_which_project_files_it_replaced(self) -> None:
        with in_temp_dir():
            Path("scripts").mkdir()
            Path("scripts/size_check.py").write_text("# the project's own\n", encoding="utf-8")
            out = run("sync")[1]
            self.assertIn("replaced scripts/size_check.py", out)


if __name__ == "__main__":
    unittest.main()

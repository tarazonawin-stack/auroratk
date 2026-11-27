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

    def test_ref_can_pin_a_commit_for_a_trial_and_unsafe_names_are_refused(self) -> None:
        with in_temp_dir():
            run("sync", "--ref", "0123abcd" * 5)
            self.assertEqual(kernel_sync.read_pin()["version"], "0123abcd" * 5)
            self.assertEqual(run("check")[0], 0)
            for bad in ["v1; rm -rf /", "refs/pull/1/head", "main", "0123abcd"]:
                with self.assertRaises(SystemExit):
                    run("sync", "--ref", bad)


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

    def test_pin_must_be_a_tag_or_a_full_commit(self) -> None:
        # A pull request ref or a branch would let CI run a weakened kernel_sync.py.
        for pin in ["refs/pull/1/head", "main", "0123abcd"]:
            def pin_ref(pin: str = pin) -> None:
                Path(".github/kernel.txt").write_text(f"version {pin}\n", encoding="utf-8")
            self.assertIn("must be a release tag", self.broken(pin_ref))

    def test_hooks_switched_off_fail(self) -> None:
        def switch_off() -> None:
            path = Path(".claude/settings.json")
            settings = json.loads(path.read_text(encoding="utf-8"))
            settings["disableAllHooks"] = True
            path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertIn("settings.json: disableAllHooks", self.broken(switch_off))
        local = Path(".claude/settings.local.json")
        out = self.broken(lambda: local.write_text('{"disableAllHooks": true}', encoding="utf-8"))
        self.assertIn("settings.local.json: disableAllHooks", out)

    def test_settings_that_are_not_an_object_fail(self) -> None:
        out = self.broken(lambda: Path(".claude/settings.json").write_text("[]", encoding="utf-8"))
        self.assertIn("not a JSON object", out)


if __name__ == "__main__":
    unittest.main()

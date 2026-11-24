"""Tests for perfiles/ci/size_hook.py: the R02 brake after every `git commit` (Claude Code hook)."""

import contextlib
import io
import json
import os
import unittest
from pathlib import Path
from unittest import mock

from helpers import ROOT, in_temp_dir
from test_size_check import commit_all, start_repo, write_doc, write_lines

import size_hook


def run_hook(payload: object) -> str:
    out = io.StringIO()
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    with contextlib.redirect_stdout(out), mock.patch("sys.stdin", io.StringIO(raw)), \
            mock.patch.dict(os.environ, {"KERNEL_BASE": "base"}):
        code = size_hook.main()
    assert code == 0, "the hook must never fail the session"
    return out.getvalue()


def commit_payload(command: str = 'git commit -m "x"') -> dict[str, object]:
    return {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(Path.cwd())}


class DecideTests(unittest.TestCase):
    def test_small_change_says_nothing(self) -> None:
        self.assertIsNone(size_hook.decide(320, 160))

    def test_from_80_percent_of_either_cap_it_warns(self) -> None:
        for code, docs in [(321, 0), (0, 161)]:
            out = size_hook.decide(code, docs)
            assert out is not None
            self.assertIn("additionalContext", out["hookSpecificOutput"])  # type: ignore[operator]

    def test_over_either_cap_it_blocks(self) -> None:
        for code, docs in [(401, 0), (0, 201)]:
            out = size_hook.decide(code, docs)
            assert out is not None
            self.assertEqual(out["decision"], "block")
            self.assertIn("divide el PR", str(out["reason"]))


class HookTests(unittest.TestCase):
    def test_commit_over_the_cap_blocks(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 401)
            commit_all()
            out = json.loads(run_hook(commit_payload("git add . && git commit -m big")))
            self.assertEqual(out["decision"], "block")
            self.assertIn("401/400", out["reason"])

    def test_docs_over_the_cap_block(self) -> None:
        with in_temp_dir():
            start_repo()
            write_doc("docs/a.md", 201)
            commit_all()
            self.assertEqual(json.loads(run_hook(commit_payload()))["decision"], "block")

    def test_near_the_cap_warns(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 330)
            commit_all()
            out = json.loads(run_hook(commit_payload("git -c user.name=x commit -qm y")))
            self.assertIn("330/400", out["hookSpecificOutput"]["additionalContext"])

    def test_other_commands_are_ignored(self) -> None:
        with in_temp_dir():
            start_repo()
            write_lines("app/a.py", 500)
            commit_all()
            for command in ["git status", "echo commit", "ls", "git-commit-msg-check", ""]:
                self.assertEqual(run_hook(commit_payload(command)), "", command)

    def test_bad_input_or_missing_base_is_silent(self) -> None:
        with in_temp_dir():
            start_repo()
            self.assertEqual(run_hook("not json"), "")
            self.assertEqual(run_hook({"tool_input": "x"}), "")
            with mock.patch.dict(os.environ, {"KERNEL_BASE": "no-such-branch"}):
                out = io.StringIO()
                with contextlib.redirect_stdout(out), \
                        mock.patch("sys.stdin", io.StringIO(json.dumps(commit_payload()))):
                    self.assertEqual(size_hook.main(), 0)
                self.assertEqual(out.getvalue(), "")


class SettingsTests(unittest.TestCase):
    """The settings template and the kernel's own settings wire the hook after Bash."""

    def hook_commands(self, name: str) -> list[str]:
        settings = json.loads((ROOT / name).read_text(encoding="utf-8"))
        return [hook["command"] for entry in settings["hooks"]["PostToolUse"]
                if entry["matcher"] == "Bash" for hook in entry["hooks"] if hook["type"] == "command"]

    def test_template_runs_the_copied_script(self) -> None:
        self.assertIn('python3 "$CLAUDE_PROJECT_DIR/scripts/size_hook.py"',
                      self.hook_commands("plantillas/claude-settings.json"))

    def test_kernel_repo_runs_its_own_script(self) -> None:
        self.assertIn('python3 "$CLAUDE_PROJECT_DIR/perfiles/ci/size_hook.py"',
                      self.hook_commands(".claude/settings.json"))

    def test_kernel_repo_keeps_every_deny_rule_of_the_template(self) -> None:
        def deny(name: str) -> set[str]:
            return set(json.loads((ROOT / name).read_text(encoding="utf-8"))["permissions"]["deny"])
        self.assertLessEqual(deny("plantillas/claude-settings.json"), deny(".claude/settings.json"))


if __name__ == "__main__":
    unittest.main()

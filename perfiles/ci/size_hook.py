"""Claude Code hook: measure the PR after every git command that adds commits (AuroraTK R02). Standard library only.

Wire it as a PostToolUse hook on Bash (see plantillas/claude-settings.json). It reads the hook's
JSON on stdin and, only when a command starts with a git subcommand that adds commits (commit, merge,
cherry-pick, revert, am, rebase, pull), measures the branch with size_check:
- from 80 % of a cap: a warning the AI reads (it should plan the split now);
- over a cap: it stops the AI ("decision": "block") so the change is split before going on.
Known limits (CI measures again anyway): quoted text with a `;`, `&` or `|` before `git commit` can
warn by mistake, and `/usr/bin/git`, `sudo git`, quoted `-c`/`-C` values or backticks are missed.
It reads the repository of the hook's cwd (not of `git -C dir`). It never fails the session: any other command, or git trouble, means silence.
Base branch: the KERNEL_BASE environment variable; else, for a stacked PR, the branch's own base
(`git config branch.<name>.kernelbase <base-branch>`); else origin/main.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import size_check  # noqa: E402

WARN_SHARE = 0.8
# git at the start of a command (not inside quoted text), with global options, then a subcommand
# that creates commits on the branch.
GIT_WRITES = re.compile(r"(?:^|[;&|(\n])\s*(?:\w+=\S*\s+)*git(?:\s+(?:-[cC]\s+\S+|--[\w-]+(?:=\S+)?))*"
                        r"\s+(?:commit|merge|cherry-pick|revert|am|rebase|pull)(?![\w-])")


def message(code: int, docs: int) -> str:
    return (f"Tamaño del PR · PR size (R02): código · code {code}/{size_check.CODE_CAP}, "
            f"documentación · docs {docs}/{size_check.DOC_CAP}.")


def base_ref() -> str:
    """The branch this PR is measured against (see the module docstring)."""
    if os.environ.get("KERNEL_BASE"):
        return os.environ["KERNEL_BASE"]
    try:
        branch = size_check.git_lines("rev-parse", "--abbrev-ref", "HEAD")[0]
        configured = subprocess.run(["git", "config", f"branch.{branch}.kernelbase"],
                                    capture_output=True, text=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError, IndexError):
        configured = ""
    return configured or "origin/main"


def decide(code: int, docs: int) -> dict[str, object] | None:
    """Hook output for these sizes: block over a cap, warn from 80 %, else nothing."""
    if code > size_check.CODE_CAP or docs > size_check.DOC_CAP:
        return {"decision": "block",
                "reason": message(code, docs) + " Pasó el tope: divide el PR antes de seguir. "
                          "· Over the cap: split the PR before going on."}
    if code >= WARN_SHARE * size_check.CODE_CAP or docs >= WARN_SHARE * size_check.DOC_CAP:
        return {"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message(code, docs) + " Cerca del tope: planea cómo dividirlo. "
                                                        "· Near the cap: plan the split."}}
    return None


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    tool_input = data.get("tool_input") if isinstance(data, dict) else None
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    if not isinstance(command, str) or not GIT_WRITES.search(command):
        return 0
    cwd = data.get("cwd")
    if isinstance(cwd, str) and Path(cwd).is_dir():
        os.chdir(cwd)
    try:
        code, docs = size_check.changed_lines(base_ref())
    except (subprocess.CalledProcessError, OSError, ValueError):
        return 0
    output = decide(code, docs)
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Claude Code hook: measure the PR after every `git commit` (AuroraTK R02). Standard library only.

Wire it as a PostToolUse hook on Bash (see plantillas/claude-settings.json). It reads the hook's
JSON on stdin and, only when the command ran `git commit`, measures the branch with size_check:
- from 80 % of a cap: a warning the AI reads (it should plan the split now);
- over a cap: it stops the AI ("decision": "block") so the change is split before going on.
It never fails the session: any other command, or git trouble, means silence.
Base branch: origin/main, or the KERNEL_BASE environment variable.
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
GIT_COMMIT = re.compile(r"(?<![\w-])git\s+(?:[^;&|\n]*?\s)?commit(?![\w-])")


def message(code: int, docs: int) -> str:
    return (f"Tamaño del PR · PR size (R02): código · code {code}/{size_check.CODE_CAP}, "
            f"documentación · docs {docs}/{size_check.DOC_CAP}.")


def decide(code: int, docs: int) -> dict[str, object] | None:
    """Hook output for these sizes: block over a cap, warn from 80 %, else nothing."""
    if code > size_check.CODE_CAP or docs > size_check.DOC_CAP:
        return {"decision": "block",
                "reason": message(code, docs) + " Pasó el tope: divide el PR antes de seguir. "
                          "· Over the cap: split the PR before going on."}
    if code > WARN_SHARE * size_check.CODE_CAP or docs > WARN_SHARE * size_check.DOC_CAP:
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
    if not isinstance(command, str) or not GIT_COMMIT.search(command):
        return 0
    cwd = data.get("cwd")
    if isinstance(cwd, str) and Path(cwd).is_dir():
        os.chdir(cwd)
    try:
        code, docs = size_check.changed_lines(os.environ.get("KERNEL_BASE", "origin/main"))
    except (subprocess.CalledProcessError, OSError, ValueError):
        return 0
    output = decide(code, docs)
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Facts about a PR that change what R12 asks (AuroraTK). Standard library only; read with local git.

Usage: python3 pr_meta.py BASE HEAD   (env PR_AUTHOR: the PR author's login)
Prints KEY=VALUE lines for $GITHUB_ENV, values are always 0 or 1:
- IS_REVERT=1 when the PR is exactly `git revert` of one change already on the main branch: undoing
  never asks the owner to write anything. Exact means the same patch, compared with git patch-id.
- DEPENDABOT_OK=1 when the PR author is dependabot[bot] and every commit is authored by it. Limit:
  commit authors can be forged; this catches someone else's push, not a determined forgery.
"""

import os
import re
import subprocess
import sys

DEPENDABOT = "dependabot[bot]"
DEPENDABOT_EMAIL = "49699333+dependabot[bot]@users.noreply.github.com"
REVERTS = re.compile(r"^This reverts commit ([0-9a-f]{40})\b", re.MULTILINE)


def git(*args: str, stdin: str | None = None) -> str:
    return subprocess.run(["git", *args], input=stdin, capture_output=True, text=True, check=True).stdout


def patch_id(diff: str) -> str:
    """Stable id of a change: the same edits give the same id, whatever the line numbers."""
    out = git("patch-id", "--stable", stdin=diff).split()
    return out[0] if out else ""


def is_exact_revert(base: str, head: str) -> bool:
    """One commit that says it reverts a change on the base branch and undoes exactly that change."""
    commits = git("rev-list", "--no-merges", f"{base}..{head}").split()
    merges = git("rev-list", "--merges", f"{base}..{head}").split()
    if len(commits) != 1 or merges:
        return False
    match = REVERTS.search(git("log", "-1", "--format=%B", commits[0]))
    if match is None:
        return False
    target = match.group(1)
    if subprocess.run(["git", "merge-base", "--is-ancestor", target, base]).returncode != 0:
        return False
    first_parent = f"{target}^1"
    undo_of_target = git("diff", "--binary", target, first_parent)
    this_pr = git("diff", "--binary", f"{commits[0]}^", commits[0])
    return bool(undo_of_target.strip()) and patch_id(undo_of_target) == patch_id(this_pr)


def dependabot_only(base: str, head: str) -> bool:
    """Every commit of the PR is authored by Dependabot."""
    authors = git("log", "--format=%an <%ae>", f"{base}..{head}").splitlines()
    return bool(authors) and all(a == f"{DEPENDABOT} <{DEPENDABOT_EMAIL}>" for a in authors)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2])
        return 2
    base, head = argv[1], argv[2]
    print(f"IS_REVERT={int(is_exact_revert(base, head))}")
    if os.environ.get("PR_AUTHOR", "") == DEPENDABOT:
        print(f"DEPENDABOT_OK={int(dependabot_only(base, head))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

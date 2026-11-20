"""Facts about a PR that change what R12 asks (AuroraTK). Standard library only; read with local git.

Usage: python3 pr_meta.py BASE HEAD   (env PR_AUTHOR: the PR author's login)
Prints KEY=VALUE lines for $GITHUB_ENV, values are always 0 or 1:
- IS_REVERT=1 when the PR is exactly `git revert` of one of the last RECENT changes of the main branch:
  undoing never asks the owner to write anything. Exact means the same files byte for byte: the
  revert commit's tree equals the tree git builds when it reverts that change itself.
- DEPENDABOT_OK=1 when the PR author is dependabot[bot], every commit is authored by it and every file
  is a dependency manifest, lock file or workflow. Limit: commit authors can be forged.
"""

import os
import re
import subprocess
import sys

from risk import matches

RECENT = 20  # an exact revert skips the owner only for one of the last 20 changes of the main branch
DEPENDENCY_FILES = ["**/uv.lock", "**/pyproject.toml", "**/requirements*.txt", "**/poetry.lock", "**/Pipfile*",
                    "**/package.json", "**/package-lock.json", "**/yarn.lock", "**/pnpm-lock.yaml", "**/go.mod",
                    "**/go.sum", "**/Cargo.toml", "**/Cargo.lock", "**/pom.xml", "**/build.gradle*",
                    "**/Gemfile*", "**/composer.json", "**/composer.lock", ".github/workflows/*.yml",
                    ".github/workflows/*.yaml"]

DEPENDABOT = "dependabot[bot]"
DEPENDABOT_EMAIL = "49699333+dependabot[bot]@users.noreply.github.com"
REVERTS = re.compile(r"^This reverts commit ([0-9a-f]{40})\b", re.MULTILINE)


def git(*args: str, stdin: str | None = None) -> str:
    return subprocess.run(["git", *args], input=stdin, capture_output=True, text=True, check=True).stdout


def is_exact_revert(base: str, head: str) -> bool:
    """One commit that says it reverts a recent change on the base branch and leaves exactly the files
    that git itself produces when reverting that change (whitespace and modes included)."""
    commits = git("rev-list", "--no-merges", f"{base}..{head}").split()
    merges = git("rev-list", "--merges", f"{base}..{head}").split()
    if len(commits) != 1 or merges:
        return False
    match = REVERTS.search(git("log", "-1", "--format=%B", commits[0]))
    if match is None:
        return False
    target = match.group(1)
    recent = git("rev-list", "--first-parent", f"--max-count={RECENT}", base).split()
    if target not in recent:
        return False
    result = subprocess.run(["git", "merge-tree", "--write-tree", f"--merge-base={target}",
                             f"{commits[0]}^", f"{target}^1"], capture_output=True, text=True)
    if result.returncode != 0:  # the revert has conflicts: not exact
        return False
    reverted_tree = result.stdout.split()[0]
    return reverted_tree == git("rev-parse", f"{commits[0]}^{{tree}}").strip() != \
        git("rev-parse", f"{commits[0]}^^{{tree}}").strip()


def dependabot_only(base: str, head: str) -> bool:
    """Every commit of the PR is authored by Dependabot and every file is a dependency file."""
    authors = git("log", "--format=%an <%ae>", f"{base}..{head}").splitlines()
    files = git("diff", "--name-only", "-z", f"{base}...{head}").split("\0")
    return (bool(authors) and all(a == f"{DEPENDABOT} <{DEPENDABOT_EMAIL}>" for a in authors)
            and all(matches(f, DEPENDENCY_FILES) for f in files if f))


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

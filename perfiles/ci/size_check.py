"""Check change size and file size (AuroraTK R02). Language-agnostic.

Usage: python size_check.py <base-ref>     e.g. python size_check.py origin/main
- Changed lines in the PR: warning above 200, failure above 400.
- Code files: warning above 300 lines, failure above 400.
Lock files, migrations and generated files are excluded.
"""

import subprocess
import sys
from pathlib import Path

CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".h", ".cpp", ".hpp",
                 ".cs", ".go", ".rs", ".html", ".css", ".scss", ".vue", ".svelte", ".gd"}
EXCLUDED_PARTS = {"migrations", "node_modules", "dist", "build", "vendor", "generated"}
EXCLUDED_NAMES = {"uv.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock"}
CHANGE_TARGET, CHANGE_CAP, FILE_WARN, FILE_CAP = 200, 400, 300, 400


def is_excluded(path: Path) -> bool:
    """Skip lock files, migrations and generated folders."""
    return path.name in EXCLUDED_NAMES or bool(EXCLUDED_PARTS & set(path.parts))


def git_lines(*args: str) -> list[str]:
    """Run a git command and return its output lines."""
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def changed_lines(base: str) -> int:
    """Count added plus deleted lines against the merge base, excluding generated files."""
    total = 0
    for line in git_lines("diff", "--numstat", f"{base}...HEAD"):
        added, deleted, name = line.split("\t", 2)
        if added == "-" or is_excluded(Path(name)):
            continue
        total += int(added) + int(deleted)
    return total


def oversized_files() -> tuple[list[str], list[str]]:
    """Return (warnings, failures) for tracked code files by line count."""
    warnings, failures = [], []
    for name in git_lines("ls-files"):
        path = Path(name)
        if path.suffix not in CODE_SUFFIXES or is_excluded(path) or not path.is_file():
            continue
        count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if count > FILE_CAP:
            failures.append(f"{name}: {count} lines (cap {FILE_CAP})")
        elif count > FILE_WARN:
            warnings.append(f"{name}: {count} lines (split it before {FILE_CAP})")
    return warnings, failures


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    changed = changed_lines(base)
    print(f"Changed lines: {changed} (target {CHANGE_TARGET}, cap {CHANGE_CAP})")
    warnings, failures = oversized_files()
    for item in warnings:
        print(f"::warning::{item}")
    for item in failures:
        print(f"::error::{item}")
    if changed > CHANGE_TARGET:
        print(f"::warning::Change is above the {CHANGE_TARGET}-line target")
    return 1 if failures or changed > CHANGE_CAP else 0


if __name__ == "__main__":
    sys.exit(main())

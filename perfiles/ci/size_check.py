"""Check change size and file size (AuroraTK R02). Language-agnostic.

Usage: python size_check.py <base-ref>     e.g. python size_check.py origin/main
- Changed lines in the PR, counted apart: code (warning above 200, failure above 400) and
  documentation, .md/.rst/.adoc (failure above 200). Each cap blocks on its own.
- Code files: warning above 300 lines, failure above 400.
- AGENTS.md at the root: failure above 450 words (R13: instructions for the AI stay short).
Lock files, migrations, generated files and third-party files (third_party/, LICENSES/) and UI translation files (.po, .mo) are excluded.
"""

import subprocess
import sys
from pathlib import Path

CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".h", ".cpp", ".hpp",
                 ".cs", ".go", ".rs", ".html", ".css", ".scss", ".vue", ".svelte", ".gd"}
EXCLUDED_PARTS = {"migrations", "node_modules", "dist", "build", "vendor", "generated",
                  "third_party", "LICENSES"}  # vendored files are inventoried under R07
EXCLUDED_SUFFIXES = {".po", ".mo"}  # UI translations, checked by the R11 parity test
EXCLUDED_NAMES = {"uv.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock"}
DOC_SUFFIXES = {".md", ".rst", ".adoc"}  # counted against DOC_CAP, not CODE_CAP
CODE_TARGET, CODE_CAP, DOC_CAP, FILE_WARN, FILE_CAP = 200, 400, 200, 300, 400
AGENTS_FILE, AGENTS_WORD_CAP = Path("AGENTS.md"), 450


def is_excluded(path: Path) -> bool:
    """Skip lock files, migrations and generated folders."""
    return (path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES
            or bool(EXCLUDED_PARTS & set(path.parts)))


def git_lines(*args: str) -> list[str]:
    """Run a git command and return its output lines."""
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def changed_lines(base: str) -> tuple[int, int]:
    """Return (code, docs): added plus deleted lines against the merge base, excluding generated files."""
    code = docs = 0
    for line in git_lines("diff", "--numstat", f"{base}...HEAD"):
        added, deleted, name = line.split("\t", 2)
        path = Path(name)
        if added == "-" or is_excluded(path):
            continue
        if path.suffix.lower() in DOC_SUFFIXES:
            docs += int(added) + int(deleted)
        else:
            code += int(added) + int(deleted)
    return code, docs


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


def agents_too_long() -> str | None:
    """R13: the AI's instruction file stays under the word cap; detail goes to skills."""
    if not AGENTS_FILE.is_file():
        return None
    words = len(AGENTS_FILE.read_text(encoding="utf-8", errors="replace").split())
    if words > AGENTS_WORD_CAP:
        return f"{AGENTS_FILE}: {words} words (cap {AGENTS_WORD_CAP}): move detail to .claude/skills/"
    return None


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    code, docs = changed_lines(base)
    print(f"Changed lines: code {code} (target {CODE_TARGET}, cap {CODE_CAP}) · docs {docs} (cap {DOC_CAP})")
    warnings, failures = oversized_files()
    agents = agents_too_long()
    if agents:
        failures.append(agents)
    for item in warnings:
        print(f"::warning::{item}")
    for item in failures:
        print(f"::error::{item}")
    if code > CODE_CAP:
        print(f"::error::Code is above the {CODE_CAP}-line cap: split the PR")
    elif code > CODE_TARGET:
        print(f"::warning::Code is above the {CODE_TARGET}-line target")
    if docs > DOC_CAP:
        print(f"::error::Documentation is above the {DOC_CAP}-line cap: split the PR")
    return 1 if failures or code > CODE_CAP or docs > DOC_CAP else 0


if __name__ == "__main__":
    sys.exit(main())

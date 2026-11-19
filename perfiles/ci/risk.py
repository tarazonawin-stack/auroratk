"""Minimum risk of a change, computed from its files and lines (AuroraTK R12). Standard library only.

Risk 1 (routine) only by exact list; risk 3 (critical) by path, file kind or content; risk 2 is
everything else, including any unknown path. The PR may declare a higher risk, never a lower one.
A project may ADD risk-3 paths and alarm words in a risk file; it can never remove the defaults,
and changing that file is itself risk 3.

Usage: python3 risk.py BASE [HEAD]   (prints the risk and the reason for every file above 1)
"""

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

RISK_FILE = ".github/riesgo.txt"

ROUTINE = ["docs/ESTADO.md", "CHANGELOG.md", "docs/evidencia/**"]

CRITICAL_PATHS = [
    ".github/**", "scripts/**", "Dockerfile", "**/Dockerfile", "compose*.y*ml", "docker-compose*.y*ml",
    "pyproject.toml", "uv.lock", "poetry.lock", "requirements*.txt", "package.json", "package-lock.json",
    "pnpm-lock.yaml", "yarn.lock", "docs/kernel/**", "docs/excepciones.md", "AGENTS.md", "CLAUDE.md",
    ".claude/**", "config/settings*", "**/settings.py", "**/settings/**", ".env.example", "**/wsgi.py",
    "**/asgi.py", RISK_FILE,
]

# Removing or changing these lines weakens access control: Django profile.
PERMISSION_WORDS = ["csrf_exempt", ".raw(", "RawSQL", ".extra(", "login_required", "permission_required",
                    "has_perm", "LoginRequiredMixin", "PermissionRequiredMixin", "UserPassesTestMixin"]

# Added lines containing these raise an alarm (risk 3). An alarm, not a lock.
ALARM_WORDS = ["eval(", "exec(", "pytest.mark.skip", "xfail", "shell=True", "verify=False", "|safe",
               "mark_safe"]

# Migration operations that delete, rename, change or transform data.
DESTRUCTIVE_MIGRATION = ["RemoveField", "DeleteModel", "RenameField", "RenameModel", "AlterField",
                         "AlterModelTable", "RunPython", "RunSQL", "RemoveIndex", "RemoveConstraint",
                         "AlterUniqueTogether"]

CODE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".html", ".jinja", ".j2", ".sh", ".java",
                 ".cpp", ".cc", ".c", ".h", ".hpp", ".go", ".rb", ".php", ".vue", ".svelte"}
SYMLINK, EXECUTABLE = "120000", "100755"


@dataclass
class FileChange:
    """One file of the diff. A rename has both paths; lines are the added and removed text."""
    path: str
    status: str = "M"  # A added, M modified, D deleted, R renamed, T type changed
    old_path: str | None = None
    binary: bool = False
    old_mode: str = ""
    new_mode: str = ""
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


def glob_regex(pattern: str) -> re.Pattern[str]:
    """'**' crosses folders, '*' does not; a pattern without '/' matches a top-level path only."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(out + r"\Z")


def matches(path: str, patterns: list[str]) -> bool:
    return any(glob_regex(p).match(path) for p in patterns)


def contains_word(line: str, word: str) -> bool:
    """Whole-word search: no letter, digit or '_' glued before or (for plain words) after it."""
    before = r"(?<![A-Za-z0-9_])" if word[0].isalnum() or word[0] == "_" else ""
    after = r"(?![A-Za-z0-9_])" if word[-1].isalnum() or word[-1] == "_" else ""
    return re.search(before + re.escape(word) + after, line) is not None


def is_test_file(path: str) -> bool:
    name = PurePosixPath(path).name
    return (matches(path, ["tests/**", "**/tests/**", "test/**", "**/test/**"])
            or name.startswith("test_") or name.endswith(("_test.py", ".test.js", ".test.ts", ".spec.ts")))


def load_project_rules(text: str) -> tuple[list[str], list[str]]:
    """Risk file lines: '3 <glob>' adds a critical path, 'alarma <text>' adds an alarm word; others ignored."""
    paths, words = [], []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("3 "):
            paths.append(line[2:].strip())
        elif line.startswith("alarma "):
            words.append(line[len("alarma "):].strip())
    return paths, words


def file_risk(change: FileChange, critical: list[str], alarms: list[str]) -> tuple[int, str]:
    """Risk of one file and why. Every path of a rename counts."""
    paths = [p for p in (change.old_path, change.path) if p]
    if SYMLINK in (change.old_mode, change.new_mode):
        return 3, "enlace simbólico · symlink"
    if change.new_mode == EXECUTABLE and change.old_mode not in ("", EXECUTABLE):
        return 3, "pasa a ejecutable · becomes executable"
    if any(matches(p, critical) for p in paths):
        return 3, "ruta crítica · critical path"
    if change.status == "D" and any(is_test_file(p) for p in paths):
        return 3, "borra pruebas · deletes tests"
    if any(matches(p, ["**/migrations/*.py"]) and not p.endswith("__init__.py") for p in paths):
        if change.status == "D" or any(contains_word(line, op) for line in change.added
                                       for op in DESTRUCTIVE_MIGRATION):
            return 3, "migración que borra o cambia datos · destructive migration"
    if any(PurePosixPath(p).suffix in CODE_SUFFIXES for p in paths):
        for line in change.removed:
            if any(contains_word(line, w) for w in PERMISSION_WORDS):
                return 3, f"quita o cambia permisos · removes or changes access control: {line.strip()[:60]}"
        for line in change.added:
            word = next((w for w in alarms if contains_word(line, w)), None)
            if word:
                return 3, f"alarma «{word}» · alarm word"
    if all(matches(p, ROUTINE) for p in paths):
        return 1, "rutina · routine"
    if change.binary and not any(p.endswith(".mo") for p in paths):
        return 3, "binario · binary"
    return 2, "normal"


def compute(changes: list[FileChange], project_rules: str = "") -> tuple[int, list[tuple[str, int, str]]]:
    """Risk of the whole change (the highest of its files) and the reason for each file."""
    extra_paths, extra_words = load_project_rules(project_rules)
    critical, alarms = CRITICAL_PATHS + extra_paths, ALARM_WORDS + extra_words
    reasons = [(c.path, *file_risk(c, critical, alarms)) for c in changes]
    return max((r for _, r, _ in reasons), default=1), reasons


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def changes_from_git(base: str, head: str = "HEAD") -> list[FileChange]:
    """Read the full diff from the merge base with local git: never a paginated list."""
    span = f"{base}...{head}"
    changes: dict[str, FileChange] = {}
    fields = git("diff", "--raw", "-M", "-z", "--no-abbrev", span).split("\0")
    i = 0
    while i < len(fields) - 1:
        old_mode, new_mode, _, _, status = fields[i].lstrip(":").split(" ")
        renamed = status[0] in "RC"
        old, new = (fields[i + 1], fields[i + 2]) if renamed else (None, fields[i + 1])
        i += 3 if renamed else 2
        changes[new] = FileChange(new, status[0], old, False,
                                  "" if set(old_mode) == {"0"} else old_mode,
                                  "" if set(new_mode) == {"0"} else new_mode)
    numstat = git("diff", "--numstat", "-M", "-z", span).split("\0")
    i = 0
    while i < len(numstat) - 1:
        added, _, name = numstat[i].split("\t", 2)
        if name:
            i += 1
        else:  # rename: old and new path follow as their own fields
            name = numstat[i + 2]
            i += 3
        if added == "-" and name in changes:
            changes[name].binary = True
    by_any_path = {p: c for c in changes.values() for p in (c.path, c.old_path) if p}
    current: FileChange | None = None
    old_side = ""
    for line in git("diff", "-U0", "-M", "--no-color", "--no-prefix", span).splitlines():
        if line.startswith("diff --git"):
            current, old_side = None, ""
        elif line.startswith("--- ") and current is None:
            old_side = line[4:]
        elif line.startswith("+++ ") and current is None:
            target = line[4:] if line[4:] != "/dev/null" else old_side
            current = by_any_path.get(target)
        elif current and line.startswith("+"):
            current.added.append(line[1:])
        elif current and line.startswith("-"):
            current.removed.append(line[1:])
    return list(changes.values())


def safe(text: str) -> str:
    """One printable line: a file name from the PR must never start a line in the CI log."""
    return text.encode("unicode_escape").decode("ascii")


def main(argv: list[str]) -> int:
    if not 2 <= len(argv) <= 3:
        print(__doc__.strip().splitlines()[-1])
        return 2
    rules = Path(RISK_FILE).read_text(encoding="utf-8") if Path(RISK_FILE).exists() else ""
    risk, reasons = compute(changes_from_git(*argv[1:]), rules)
    print(f"Riesgo {risk}")
    for path, level, why in reasons:
        if level > 1:
            print(f"  {level}  {safe(path)}: {safe(why)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

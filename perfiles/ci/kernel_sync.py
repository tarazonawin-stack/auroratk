"""Copy the AuroraTK kernel into a project and check that the copy stays exact. Standard library only.

    python3 kernel_sync.py sync  --from KERNEL_DIR [--ci python-django] [--ref REF]
    python3 kernel_sync.py check --from KERNEL_DIR

KERNEL_DIR is a checkout of the kernel at the pinned version (git ref in `.github/kernel.txt`).
- FIXED files are the kernel's own (rules, profiles, CI scripts, the R12 workflow, kernel skills):
  `sync` overwrites them and `check` fails if one is missing or differs, or if docs/kernel/ has extras.
- TEMPLATES belong to the project once copied: `sync` copies them only when they are missing.
- `check` also fails if .claude/settings.json lost the size hook or a deny rule of the template, turns
  hooks off or bypasses permissions. Not checked: .claude/settings.local.json, emptied `ask` rules,
  wider `allow` rules, or the hook's type and timeout; review covers those (R13).
In CI, run `check` with the kernel_sync.py of the fetched kernel, never the project's own copy.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

PIN_FILE = Path(".github/kernel.txt")
SCRIPTS = ["risk.py", "pr_check.py", "pr_meta.py", "size_check.py", "size_hook.py",
           "mutation_threshold.py", "kernel_sync.py"]
TEMPLATES = {
    "plantillas/AGENTS.md": "AGENTS.md", "plantillas/CLAUDE.md": "CLAUDE.md",
    "plantillas/PULL_REQUEST_TEMPLATE.md": ".github/PULL_REQUEST_TEMPLATE.md",
    "plantillas/dependabot.yml": ".github/dependabot.yml",
    "plantillas/claude-settings.json": ".claude/settings.json",
    "plantillas/ESTADO.md": "docs/ESTADO.md", "plantillas/ESTRUCTURA.md": "docs/ESTRUCTURA.md",
    "plantillas/EXCEPCIONES.md": "docs/excepciones.md",
    "plantillas/DATOS-REALES.md": "docs/datos-reales.md",
}
VERSION = re.compile(r"\*\*Versi[oó]n (\d+\.\d+\.\d+)\*\*")
SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
RELEASE_TAG = re.compile(r"^v(\d+\.\d+\.\d+)(?:-rc\.\d+)?$")  # vX.Y.Z or a trial tag like vX.Y.Z-rc.1


def fixed_files(kernel: Path) -> dict[str, str]:
    """Kernel path → project path for every file the project must keep byte for byte."""
    files = {name: f"docs/kernel/{name}" for name in ["KERNEL.md", "KERNEL.en.md", "SHA256SUMS"]}
    for path in sorted((kernel / "perfiles").glob("*.md")):
        files[f"perfiles/{path.name}"] = f"docs/kernel/perfiles/{path.name}"
    files.update({f"perfiles/ci/{name}": f"scripts/{name}" for name in SCRIPTS})
    files["perfiles/ci/pr-description.yml"] = ".github/workflows/pr-description.yml"
    for path in sorted((kernel / "plantillas/skills").glob("*/SKILL.md")):
        rel = path.relative_to(kernel / "plantillas").as_posix()
        files[f"plantillas/{rel}"] = f".claude/{rel}"
    return files


def kernel_version(kernel: Path) -> str:
    match = VERSION.search((kernel / "KERNEL.md").read_text(encoding="utf-8"))
    if match is None:
        raise SystemExit(f"{kernel}: not an AuroraTK kernel (no version in KERNEL.md)")
    return match.group(1)


def read_pin() -> dict[str, str]:
    """`.github/kernel.txt`: lines 'version <git ref>' and, optionally, 'ci <profile>'."""
    pin: dict[str, str] = {}
    if PIN_FILE.is_file():
        for line in PIN_FILE.read_text(encoding="utf-8").splitlines():
            key, _, value = line.partition(" ")
            if key in {"version", "ci"} and value.strip():
                pin[key] = value.strip()
    return pin


def copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def sync(kernel: Path, ci: str | None, ref: str | None) -> int:
    pin = read_pin()
    ci = ci or pin.get("ci")
    ref = ref or f"v{kernel_version(kernel)}"
    if ci and not SAFE_NAME.match(ci):
        raise SystemExit(f"unsafe CI profile name: {ci!r}")
    match = RELEASE_TAG.match(ref)
    if match is None or match.group(1) != kernel_version(kernel):
        raise SystemExit(f"--ref must be a release tag of this kernel (v{kernel_version(kernel)} or "
                         f"v{kernel_version(kernel)}-rc.N), not {ref!r}")
    templates = dict(TEMPLATES)
    if ci:
        templates[f"perfiles/ci/{ci}.yml"] = ".github/workflows/ci.yml"
    for dest in {Path(d) for d in [*fixed_files(kernel).values(), *templates.values(), str(PIN_FILE)]}:
        if any(part.is_symlink() for part in [dest, *dest.parents]):  # broken links too
            raise SystemExit(f"refusing to write through a symbolic link: {dest}")
    for kept in Path("docs/kernel").rglob("*") if Path("docs/kernel").is_dir() else []:
        if kept.is_file():
            kept.unlink()  # docs/kernel/ is the kernel's: files of an older version go away
    for src, dest in fixed_files(kernel).items():
        if Path(dest).is_file() and Path(dest).read_bytes() != (kernel / src).read_bytes():
            print(f"replaced {dest} with the kernel's version")
        copy(kernel / src, Path(dest))
    for src, dest in templates.items():
        if not Path(dest).exists():
            copy(kernel / src, Path(dest))
            print(f"created {dest} (yours now: fill it in)")
    for folder in ["docs/specs", "docs/decisiones", "docs/evidencia"]:
        Path(folder).mkdir(parents=True, exist_ok=True)
    PIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    PIN_FILE.write_text(f"version {ref}\n" + (f"ci {ci}\n" if ci else ""), encoding="utf-8")
    print(f"AuroraTK kernel {ref} synced. Run `check` next.")
    return 0


def settings_problems(kernel: Path) -> list[str]:
    path = Path(".claude/settings.json")
    try:
        mine = json.loads(path.read_text(encoding="utf-8"))
        template = json.loads((kernel / "plantillas/claude-settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{path}: missing or not valid JSON ({error.__class__.__name__})"]
    if not isinstance(mine, dict):
        return [f"{path}: must be a JSON object"]
    permissions, hooks = mine.get("permissions", {}), mine.get("hooks", {})
    if not isinstance(permissions, dict) or not isinstance(hooks, dict):
        return [f"{path}: 'permissions' and 'hooks' must be JSON objects"]
    problems = [f"{path}: deny rule removed: {rule}"
                for rule in template["permissions"]["deny"]
                if rule not in permissions.get("deny", [])]
    if mine.get("disableAllHooks"):
        problems.append(f"{path}: disableAllHooks turns the R02 size hook off")
    if permissions.get("defaultMode") == "bypassPermissions":
        problems.append(f"{path}: defaultMode bypassPermissions skips every deny and ask rule (R13)")
    wanted = template["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
    entries = hooks.get("PostToolUse", [])
    commands = [hook.get("command") for entry in (entries if isinstance(entries, list) else [])
                if isinstance(entry, dict) and entry.get("matcher") == "Bash"
                for hook in entry.get("hooks", []) if isinstance(hook, dict)]
    if wanted not in commands:
        problems.append(f"{path}: the R02 size hook is missing ({wanted})")
    return problems


def check(kernel: Path) -> int:
    problems = []
    pinned = read_pin().get("version")
    if pinned is None:
        problems.append(f"{PIN_FILE}: missing 'version <ref>' line")
    elif (match := RELEASE_TAG.match(pinned)) is None:
        problems.append(f"{PIN_FILE}: pin a release tag (vX.Y.Z or vX.Y.Z-rc.N), not {pinned!r}")
    elif match.group(1) != kernel_version(kernel):
        problems.append(f"{PIN_FILE} pins {pinned}, but the kernel given is v{kernel_version(kernel)}")
    files = fixed_files(kernel)
    for src, dest in files.items():
        if Path(dest).is_symlink():
            problems.append(f"symbolic link: {dest} (the kernel's files are real files in the repo)")
        elif not Path(dest).is_file():
            problems.append(f"missing: {dest}")
        elif Path(dest).read_bytes() != (kernel / src).read_bytes():
            problems.append(f"edited (the kernel's files are not changed in the project): {dest}")
    expected = set(files.values())
    for extra in sorted(Path("docs/kernel").rglob("*")) if Path("docs/kernel").is_dir() else []:
        if extra.is_file() and extra.as_posix() not in expected:
            problems.append(f"extra file in docs/kernel/: {extra.as_posix()}")
    problems += settings_problems(kernel)
    for problem in problems:
        print(f"::error::{problem}")
    print("Kernel copy OK" if not problems else f"{len(problems)} problem(s) with the kernel copy")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["sync", "check"])
    parser.add_argument("--from", dest="kernel", required=True, type=Path)
    parser.add_argument("--ci", help="CI profile to start from, e.g. python-django")
    parser.add_argument("--ref", help="tag to pin instead of vX.Y.Z, e.g. vX.Y.Z-rc.1 for a trial")
    args = parser.parse_args(argv)
    if args.command == "sync":
        return sync(args.kernel, args.ci, args.ref)
    return check(args.kernel)


if __name__ == "__main__":
    sys.exit(main())

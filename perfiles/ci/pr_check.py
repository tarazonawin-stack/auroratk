"""Check the PR description before merge (AuroraTK R12). Language-agnostic.

Fails if:
- the owner's report has no decision level (1, 2 or 3), or misses an item that level requires;
- the "Lo entiendo" section is empty or still has the template text;
- any kernel checkbox is left unchecked ("- [ ]").
The PR body arrives in the PR_BODY environment variable.
"""

import os
import re
import sys

SECTION = re.compile(r"^##\s+Lo entiendo.*?$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
REPORT = re.compile(r"^##\s+Informe para el dueño.*?$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
LEVEL = re.compile(r"^\s*\*\*Nivel[^*]*:\*\*\s*([123])\b", re.MULTILINE)
UNCHECKED = re.compile(r"^\s*-\s\[\s\]", re.MULTILINE)

# Report items each decision level adds, by their Spanish label.
ITEMS_BY_LEVEL = {
    1: ["Qué hace", "Pruebas", "Cómo se deshace"],
    2: ["Qué no hace", "Riesgos", "Plan B"],
    3: ["Opciones y recomendación", "Si no se integra"],
}


def written(text: str) -> bool:
    """True when the text is not empty and not a <template placeholder>."""
    text = text.strip()
    return bool(text) and not text.startswith("<")


def understanding_written(body: str) -> bool:
    """True when the understanding section has a line that is not template text."""
    match = SECTION.search(body)
    if match is None:
        return False
    return any(written(line) for line in match.group(1).splitlines())


def report_problems(body: str) -> list[str]:
    """What the owner's report is missing: its section, its level or a required item."""
    match = REPORT.search(body)
    if match is None:
        return ["Add the owner's report ('Informe para el dueño')."]
    report = match.group(1)
    level = LEVEL.search(report)
    if level is None:
        return ["State the owner's report level: 1, 2 or 3."]
    missing = []
    for item_level, labels in ITEMS_BY_LEVEL.items():
        if item_level > int(level.group(1)):
            break
        for label in labels:
            item = re.search(rf"^\s*-\s*\*\*{re.escape(label)}[^*]*:\*\*(.*)$", report, re.MULTILINE)
            if item is None or not written(item.group(1)):
                missing.append(label)
    if missing:
        return [f"Owner's report, level {level.group(1)}: fill in {', '.join(missing)}."]
    return []


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    problems = report_problems(body)
    if not understanding_written(body):
        problems.append("Write in one line, in your own words, what this change does ('Lo entiendo').")
    unchecked = len(UNCHECKED.findall(body))
    if unchecked:
        problems.append(f"{unchecked} checkbox(es) still unchecked: check them or mark N/A.")
    for problem in problems:
        print(f"::error::{problem}")
    if not problems:
        print("PR description complete.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

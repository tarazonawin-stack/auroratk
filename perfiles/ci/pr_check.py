"""Check the PR description before merge (AuroraTK R12). Language-agnostic.

Fails if the "Lo entiendo" section is empty or still has the template text,
or if any kernel checkbox is left unchecked ("- [ ]").
The PR body arrives in the PR_BODY environment variable.
"""

import os
import re
import sys

SECTION = re.compile(r"^##\s+Lo entiendo.*?$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
UNCHECKED = re.compile(r"^\s*-\s\[\s\]", re.MULTILINE)


def understanding_written(body: str) -> bool:
    """True when the understanding section has a line that is not template text."""
    match = SECTION.search(body)
    if match is None:
        return False
    lines = [line.strip() for line in match.group(1).splitlines()]
    return any(line and not line.startswith("<") for line in lines)


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    problems = []
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

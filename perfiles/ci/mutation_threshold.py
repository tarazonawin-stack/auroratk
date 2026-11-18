"""Fail CI when the mutmut mutation score is below a threshold (AuroraTK R03).

Usage: python mutation_threshold.py 60
Reads mutants/mutmut-cicd-stats.json, written by `mutmut export-cicd-stats`.
Timeouts count as killed: the tests did notice the mutant.
"""

import json
import sys
from pathlib import Path

STATS_FILE = Path("mutants/mutmut-cicd-stats.json")


def mutation_score(stats: dict[str, int]) -> float:
    """Return the percentage of evaluated mutants the tests caught."""
    evaluated = stats["total"] - stats["skipped"]
    if evaluated <= 0:
        return 0.0
    caught = stats["killed"] + stats["timeout"]
    return 100.0 * caught / evaluated


def main() -> int:
    threshold = float(sys.argv[1])
    stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))
    score = mutation_score(stats)
    print(f"Mutation score: {score:.1f}% (threshold {threshold:.0f}%)")
    return 0 if score >= threshold else 1


if __name__ == "__main__":
    sys.exit(main())

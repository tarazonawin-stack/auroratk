"""Tests for perfiles/ci/mutation_threshold.py (R03)."""

import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest import mock

from helpers import in_temp_dir

import mutation_threshold


def stats(killed: int, timeout: int, survived: int, skipped: int = 0) -> dict[str, int]:
    total = killed + timeout + survived + skipped
    return {"killed": killed, "timeout": timeout, "survived": survived,
            "skipped": skipped, "total": total}


def run(threshold: str, data: dict[str, int] | None) -> tuple[int, str]:
    out = io.StringIO()
    with in_temp_dir():
        if data is not None:
            Path("mutants").mkdir()
            Path("mutants/mutmut-cicd-stats.json").write_text(json.dumps(data), encoding="utf-8")
        with contextlib.redirect_stdout(out), \
                mock.patch("sys.argv", ["mutation_threshold.py", threshold]):
            code = mutation_threshold.main()
    return code, out.getvalue()


class ScoreTests(unittest.TestCase):
    def test_timeouts_count_as_caught_and_skipped_are_left_out(self) -> None:
        self.assertEqual(mutation_threshold.mutation_score(stats(5, 1, 4, skipped=10)), 60.0)

    def test_nothing_evaluated_scores_zero(self) -> None:
        self.assertEqual(mutation_threshold.mutation_score(stats(0, 0, 0, skipped=3)), 0.0)


class ThresholdTests(unittest.TestCase):
    def test_exactly_at_threshold_passes(self) -> None:
        code, out = run("60", stats(6, 0, 4))
        self.assertEqual(code, 0)
        self.assertIn("Mutation score: 60.0% (threshold 60%)", out)

    def test_below_threshold_fails(self) -> None:
        self.assertEqual(run("60", stats(5, 0, 5))[0], 1)

    def test_strict_threshold_is_applied(self) -> None:
        self.assertEqual(run("75", stats(7, 0, 3))[0], 1)

    def test_missing_stats_file_fails_with_a_hint(self) -> None:
        code, out = run("60", None)
        self.assertEqual(code, 1)
        self.assertIn("mutmut export-cicd-stats", out)


if __name__ == "__main__":
    unittest.main()

"""Tests for perfiles/ci/pr_check.py (R12)."""

import contextlib
import io
import os
import unittest
from unittest import mock

import helpers  # noqa: F401  (puts perfiles/ci on the import path)
import pr_check

TEMPLATE = (helpers.ROOT / "plantillas" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")


def run(body: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), mock.patch.dict(os.environ, {"PR_BODY": body}):
        code = pr_check.main()
    return code, out.getvalue()


def filled(body: str) -> str:
    """Template with every box checked and the understanding line written."""
    body = body.replace("- [ ]", "- [x]")
    return body.replace("## Lo entiendo · I understand it (R12)\n",
                        "## Lo entiendo · I understand it (R12)\nAgrega el filtro por contrata.\n")


class UnderstandingTests(unittest.TestCase):
    def test_untouched_template_fails_on_both_checks(self) -> None:
        code, out = run(TEMPLATE)
        self.assertEqual(code, 1)
        self.assertIn("Lo entiendo", out)
        self.assertIn("still unchecked", out)

    def test_fully_filled_template_passes(self) -> None:
        code, out = run(filled(TEMPLATE))
        self.assertEqual(code, 0)
        self.assertIn("PR description complete.", out)

    def test_only_template_placeholder_lines_do_not_count(self) -> None:
        body = "## Lo entiendo\n<write here>\n\n## Evidencia\nlink"
        self.assertFalse(pr_check.understanding_written(body))

    def test_text_in_next_section_does_not_count(self) -> None:
        body = "## Lo entiendo\n\n## Evidencia\nCI run link"
        self.assertFalse(pr_check.understanding_written(body))

    def test_missing_section_fails(self) -> None:
        self.assertFalse(pr_check.understanding_written("## Qué cambia\nAlgo"))

    def test_empty_body_fails(self) -> None:
        code, _ = run("")
        self.assertEqual(code, 1)


class CheckboxTests(unittest.TestCase):
    def test_one_unchecked_box_fails_and_is_counted(self) -> None:
        body = filled(TEMPLATE).replace("- [x] R10", "- [ ] R10", 1)
        code, out = run(body)
        self.assertEqual(code, 1)
        self.assertIn("1 checkbox(es) still unchecked", out)

    def test_uppercase_x_counts_as_checked(self) -> None:
        body = filled(TEMPLATE).replace("- [x]", "- [X]")
        self.assertEqual(run(body)[0], 0)


if __name__ == "__main__":
    unittest.main()

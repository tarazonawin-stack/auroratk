"""Tests for perfiles/ci/pr_check.py (R12)."""

import contextlib
import io
import os
import re
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


def filled(body: str, level: int = 3) -> str:
    """Template with every box checked, the report at `level` and the understanding line written."""
    body = body.replace("- [ ]", "- [x]")
    body = re.sub(r"(\*\*Nivel · Level:\*\*) <[^>]*>", rf"\g<1> {level}", body)
    body = re.sub(r"^(- \*\*[^*]+:\*\*) <[^>]*>$", r"\1 Escrito: https://ci/run/1", body, flags=re.MULTILINE)
    return body.replace("## Lo entiendo · I understand it (R12)\n",
                        "## Lo entiendo · I understand it (R12)\nAgrega el filtro por contrata.\n")


TECHNICAL = {"Cambios": "a.py", "Verificado": "tests OK", "No verificado": "nada",
             "Limitaciones": "ninguna conocida"}


def items(values: dict[str, str]) -> list[str]:
    return [f"- **{label}:** {text}" for label, text in values.items()]


def report(level: str, technical: dict[str, str] = TECHNICAL, **owner: str) -> str:
    """A minimal PR body: both reports and the understanding line."""
    return "\n".join(["## Informe para el dueño", f"**Nivel · Level:** {level}", *items(owner),
                      "", "## Informe técnico", *items(technical),
                      "", "## Lo entiendo", "Hace algo.", ""])


LEVEL_1 = {"Qué hace": "a", "Pruebas": "OK: https://ci/run/1", "Cómo se deshace": "c"}
LEVEL_2 = {**LEVEL_1, "Qué no hace": "d", "Riesgos": "e", "Plan B": "f"}


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


class ReportTests(unittest.TestCase):
    def test_untouched_template_fails_on_the_level(self) -> None:
        self.assertIn("level: 1, 2 or 3", run(TEMPLATE)[1])

    def test_missing_report_fails(self) -> None:
        code, out = run("## Lo entiendo\nHace algo.\n")
        self.assertEqual(code, 1)
        self.assertIn("Informe para el dueño", out)

    def test_level_1_needs_only_its_three_items(self) -> None:
        self.assertEqual(run(report("1", **LEVEL_1))[0], 0)

    def test_level_1_missing_an_item_fails_and_names_it(self) -> None:
        items = {**LEVEL_1, "Cómo se deshace": "<…>"}
        code, out = run(report("1", **items))
        self.assertEqual(code, 1)
        self.assertIn("level 1: fill in Cómo se deshace.", out)

    def test_level_2_needs_risks_and_plan_b(self) -> None:
        code, out = run(report("2", **LEVEL_1))
        self.assertEqual(code, 1)
        self.assertIn("Qué no hace, Riesgos, Plan B", out)
        self.assertEqual(run(report("2", **LEVEL_2))[0], 0)

    def test_level_3_needs_options_and_what_if_not_merged(self) -> None:
        code, out = run(report("3", **LEVEL_2))
        self.assertIn("Opciones y recomendación, Si no se integra", out)
        self.assertEqual(code, 1)

    def test_every_level_of_the_filled_template_passes(self) -> None:
        for level in (1, 2, 3):
            self.assertEqual(run(filled(TEMPLATE, level))[0], 0, level)

    def test_empty_item_does_not_count(self) -> None:
        self.assertEqual(run(report("1", **{**LEVEL_1, "Pruebas": "  "}))[0], 1)

    def test_tests_item_needs_a_link(self) -> None:
        code, out = run(report("1", **{**LEVEL_1, "Pruebas": "pasaron"}))
        self.assertEqual(code, 1)
        self.assertIn("Pruebas (with a link)", out)

    def test_colon_outside_the_bold_label_counts(self) -> None:
        body = report("1", **LEVEL_1).replace("**Qué hace:**", "**Qué hace**:")
        self.assertEqual(run(body)[0], 0)

    def test_level_outside_1_to_3_fails(self) -> None:
        self.assertIn("level: 1, 2 or 3", run(report("4", **LEVEL_2))[1])


class TechnicalReportTests(unittest.TestCase):
    def test_missing_technical_report_fails(self) -> None:
        body = report("1", **LEVEL_1).replace("## Informe técnico", "## Otra cosa")
        self.assertIn("Informe técnico", run(body)[1])

    def test_not_verified_must_be_stated_even_if_nothing(self) -> None:
        technical = {**TECHNICAL, "No verificado": "<…>"}
        code, out = run(report("1", technical, **LEVEL_1))
        self.assertEqual(code, 1)
        self.assertIn("Technical report: fill in No verificado.", out)

    def test_verified_and_not_verified_are_told_apart(self) -> None:
        technical = {label: text for label, text in TECHNICAL.items() if label != "Verificado"}
        self.assertIn("fill in Verificado.", run(report("1", technical, **LEVEL_1))[1])


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

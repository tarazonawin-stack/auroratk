"""Tests for perfiles/ci/pr_check.py (R12 by risk)."""

import contextlib
import io
import os
import re
import unittest
from unittest import mock

import helpers
import pr_check

TEMPLATE = (helpers.ROOT / "plantillas" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
OWNER_HEADING = "## Con tus palabras: ¿qué cambia con este PR? · In your own words: what does this PR change? (R12)\n"


def filled(risk: int, line: str = "Ahora el técnico ve sus turnos de la semana.",
           if_it_fails: str = "los técnicos no verían sus turnos un rato") -> str:
    """The template with every box checked, every item written and the owner's lines."""
    body = TEMPLATE.replace("- [ ]", "- [x]")
    body = re.sub(r"(\*\*Riesgo · Risk:\*\*) <[^>]*>", rf"\g<1> {risk}", body)
    body = re.sub(r"^(- \*\*[^*]+:\*\*) <.*>$", r"\1 Escrito: https://ci.example/run/1", body, flags=re.M)
    body = body.replace(OWNER_HEADING, OWNER_HEADING + line + "\n")
    return body.replace("Si sale mal, ¿qué pasaría?: <solo riesgo 3 · risk 3 only>",
                        f"Si sale mal, ¿qué pasaría?: {if_it_fails}")


def problems(body: str, computed: int = 1, level: str = "estandar") -> list[str]:
    return pr_check.problems(body, computed, level)


def run(body: str, computed: str = "2", level: str = "estandar") -> tuple[int, str]:
    out = io.StringIO()
    env = {"PR_BODY": body, "COMPUTED_RISK": computed, "KERNEL_LEVEL": level}
    with contextlib.redirect_stdout(out), mock.patch.dict(os.environ, env):
        code = pr_check.main()
    return code, out.getvalue()


class RiskTests(unittest.TestCase):
    def test_untouched_template_fails_on_the_risk(self) -> None:
        self.assertTrue(any("Falta el riesgo" in p for p in problems(TEMPLATE)))

    def test_cannot_declare_less_than_computed(self) -> None:
        found = problems(filled(2), computed=3)
        self.assertTrue(any("menor que el calculado (3)" in p for p in found))

    def test_a_low_declared_risk_still_lists_what_the_computed_risk_asks(self) -> None:
        found = problems(filled(1, line="", if_it_fails="<…>"), computed=3)
        self.assertIn(pr_check.EMPTY_LINE, found)
        self.assertTrue(any("Si sale mal" in p for p in found))

    def test_may_declare_more_than_computed(self) -> None:
        self.assertEqual(problems(filled(3), computed=1), [])

    def test_computed_risk_rules_even_when_declared_is_missing(self) -> None:
        body = filled(3).replace("**Riesgo · Risk:** 3", "**Riesgo · Risk:** <…>")
        found = problems(body, computed=3)
        self.assertTrue(any("Falta el riesgo" in p for p in found))

    def test_risk_must_be_1_2_or_3(self) -> None:
        for value in ["4", "12", "dos"]:
            body = filled(2).replace("**Riesgo · Risk:** 2", f"**Riesgo · Risk:** {value}")
            self.assertTrue(any("Falta el riesgo" in p for p in problems(body)), value)

    def test_ci_must_pass_the_computed_risk(self) -> None:
        code, out = run(filled(2), computed="")
        self.assertEqual(code, 1)
        self.assertIn("COMPUTED_RISK", out)


class OwnerByRiskTests(unittest.TestCase):
    def test_risk_1_needs_nothing_from_the_owner(self) -> None:
        body = filled(1, line="").replace("Si sale mal, ¿qué pasaría?: los técnicos no verían sus turnos un rato",
                                          "")
        body = re.sub(r"(- \*\*(Qué|Cómo|Recomendación)[^*]*:\*\*).*", r"\1 <…>", body)
        self.assertEqual(problems(body, computed=1), [])

    def test_risk_2_needs_the_owner_report_and_line(self) -> None:
        self.assertEqual(problems(filled(2), computed=2), [])
        found = problems(filled(2, line=""), computed=2)
        self.assertIn(pr_check.EMPTY_LINE, found)
        body = filled(2).replace("- **Qué puede salir mal · What can go wrong:** Escrito: https://ci.example/run/1",
                                 "- **Qué puede salir mal · What can go wrong:** <…>")
        self.assertTrue(any("Qué puede salir mal" in p for p in problems(body, computed=2)))

    def test_risk_3_also_needs_what_if_it_fails(self) -> None:
        self.assertEqual(problems(filled(3), computed=3), [])
        found = problems(filled(3, if_it_fails="<solo riesgo 3>"), computed=3)
        self.assertTrue(any("Si sale mal" in p for p in found))
        self.assertTrue(problems(filled(3, if_it_fails="ok"), computed=3))

    def test_what_if_it_fails_does_not_count_as_what_changes(self) -> None:
        self.assertIn(pr_check.EMPTY_LINE, problems(filled(3, line=""), computed=3))

    def test_light_level_asks_the_owner_only_at_risk_3(self) -> None:
        self.assertEqual(problems(filled(2, line=""), computed=2, level="ligero"), [])
        self.assertIn(pr_check.EMPTY_LINE, problems(filled(3, line=""), computed=3, level="ligero"))

    def test_strict_level_asks_like_standard(self) -> None:
        self.assertIn(pr_check.EMPTY_LINE, problems(filled(2, line=""), computed=2, level="estricto"))


class OwnerLineFilterTests(unittest.TestCase):
    def test_bare_approval_words_are_rejected_in_any_spelling(self) -> None:
        for line in ["ok", "OK.", "Sí", "si!!", "Listo", "Lo entiendo", "lo entiendo.", "APROBADO", "dale"]:
            self.assertIn(pr_check.EMPTY_LINE, problems(filled(2, line=line), computed=2), line)

    def test_spelling_and_wording_never_matter(self) -> None:
        for line in ["aora el tecnico be sus turnos", "ok, ahora se ven los turnos", "turnos semana técnico"]:
            self.assertEqual(problems(filled(2, line=line), computed=2), [], line)

    def test_template_text_is_not_an_answer(self) -> None:
        self.assertIn(pr_check.EMPTY_LINE, problems(filled(2, line="<escribe aquí>"), computed=2))

    def test_old_title_lo_entiendo_still_works(self) -> None:
        body = filled(2).replace(OWNER_HEADING, "## Lo entiendo · I understand it (R12)\n")
        self.assertEqual(problems(body, computed=2), [])

    def test_title_without_accents_or_question_marks_works(self) -> None:
        body = filled(2).replace(OWNER_HEADING, "## con tus palabras que cambia con este PR\n")
        self.assertEqual(problems(body, computed=2), [])

    def test_windows_line_endings_work(self) -> None:
        self.assertEqual(problems(filled(3).replace("\n", "\r\n"), computed=3), [])


class ReviewFindingsTests(unittest.TestCase):
    """Minor findings of the independent review of #14."""

    def test_a_second_owner_title_is_an_error(self) -> None:
        body = "## Con tus palabras: ¿qué cambia?\nlo escribió la IA aquí\n\n" + filled(2, line="")
        self.assertTrue(any("más de un título" in p for p in problems(body, computed=2)))

    def test_star_bullets_count(self) -> None:
        body = filled(2).replace("- **", "* **")
        self.assertEqual(problems(body, computed=2), [])

    def test_star_checkbox_counts_as_unchecked(self) -> None:
        self.assertTrue(any("casilla" in p for p in problems(filled(2) + "\n* [ ] otra\n", computed=2)))

    def test_anything_starting_with_angle_bracket_is_template(self) -> None:
        self.assertIn(pr_check.EMPTY_LINE, problems(filled(2, line="<texto"), computed=2))

    def test_unknown_level_is_an_error(self) -> None:
        code, out = run(filled(2), computed="2", level="estrico")
        self.assertEqual(code, 1)
        self.assertIn("KERNEL_LEVEL desconocido", out)


class TechnicalReportTests(unittest.TestCase):
    def test_every_risk_needs_the_technical_report(self) -> None:
        body = filled(1).replace("- **No verificado · Not verified:** Escrito: https://ci.example/run/1",
                                 "- **No verificado · Not verified:** <…>")
        self.assertTrue(any("No verificado" in p for p in problems(body, computed=1)))

    def test_verified_needs_a_link(self) -> None:
        body = filled(1).replace("- **Verificado · Verified:** Escrito: https://ci.example/run/1",
                                 "- **Verificado · Verified:** pasó todo")
        self.assertTrue(any("Verificado (con enlace)" in p for p in problems(body, computed=1)))

    def test_colon_outside_the_bold_label_counts(self) -> None:
        body = filled(1).replace("**Cambios · Changes:**", "**Cambios · Changes**:")
        self.assertEqual(problems(body, computed=1), [])


class CheckboxTests(unittest.TestCase):
    def test_one_unchecked_box_fails_and_is_counted(self) -> None:
        body = filled(2).replace("- [x] R10", "- [ ] R10", 1)
        self.assertIn("Quedan 1 casilla(s) sin marcar: márcalas o escribe N/A.", problems(body, 2))

    def test_uppercase_x_counts_as_checked(self) -> None:
        self.assertEqual(problems(filled(2).replace("- [x]", "- [X]"), computed=2), [])


class MainTests(unittest.TestCase):
    def test_complete_description_passes_and_says_the_risk(self) -> None:
        code, out = run(filled(3), computed="3")
        self.assertEqual(code, 0)
        self.assertIn("Riesgo calculado: 3", out)
        self.assertIn("Descripción del PR completa.", out)

    def test_problems_are_github_errors(self) -> None:
        code, out = run(TEMPLATE, computed="2")
        self.assertEqual(code, 1)
        self.assertIn("::error::Falta el riesgo", out)


if __name__ == "__main__":
    unittest.main()

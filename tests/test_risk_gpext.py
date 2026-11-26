"""risk.py, 4.0.0-rc.2 (SPEC-002): two real bypasses found in the GPEXT trial. Both tests failed before."""

import unittest

import helpers  # noqa: F401  (puts perfiles/ci on the path)
import risk
from risk import FileChange


def level(*changes: FileChange, rules: str = "") -> int:
    return risk.compute(list(changes), rules)[0]


class RemovedAssertTests(unittest.TestCase):
    def test_removing_asserts_from_a_test_is_critical(self) -> None:
        for removed in ["    assert response.status_code == 404", "        self.assertEqual(a, b)",
                        "    assertThat(x).isTrue();"]:
            change = FileChange("tickets/tests/test_views.py", removed=[removed], added=["    pass"])
            self.assertEqual(level(change), 3, removed)

    def test_rewording_an_assert_is_not_a_removal(self) -> None:
        change = FileChange("tickets/tests/test_views.py", removed=["    assert a == 1"], added=["    assert a == 2"])
        self.assertEqual(level(change), 2)

    def test_asserts_outside_tests_are_not_this_rule(self) -> None:
        self.assertEqual(level(FileChange("tickets/views.py", removed=["    assert user"])), 2)


class ProjectRemovalWordTests(unittest.TestCase):
    RULES = "quitar scoped(\n"

    def test_removing_a_project_guard_is_critical(self) -> None:
        change = FileChange("tickets/views.py", removed=["    qs = scoped(Ticket.objects, request.user)"],
                            added=["    qs = Ticket.objects.all()"])
        self.assertEqual(level(change, rules=self.RULES), 3)
        self.assertIn("scoped(", risk.compute([change], self.RULES)[1][0][2])

    def test_adding_the_guard_or_other_files_stay_normal(self) -> None:
        added = FileChange("tickets/views.py", added=["    qs = scoped(Ticket.objects, request.user)"])
        self.assertEqual(level(added, rules=self.RULES), 2)
        doc = FileChange("docs/notas.md", removed=["usa scoped( siempre"])
        self.assertEqual(level(doc, rules=self.RULES), 2)

    def test_the_rule_only_adds_never_lowers(self) -> None:
        change = FileChange("AGENTS.md", removed=["x"])
        self.assertEqual(level(change, rules="quitar \nquitar x\n"), 3)


if __name__ == "__main__":
    unittest.main()

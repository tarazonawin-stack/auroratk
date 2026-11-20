"""Check the PR description before merge (AuroraTK R12, by risk). Standard library only.

Inputs, by environment variable (never pasted into a script):
- PR_BODY: the PR description.
- COMPUTED_RISK: the minimum risk that risk.py computed for the diff (1, 2 or 3).
- KERNEL_LEVEL: ligero, estandar (default) or estricto.
- HEAD_SHA: the PR head; the checked review line must name it ("Hay cambios nuevos sin revisar").
- IS_REVERT, DEPENDABOT_OK (from pr_meta.py), PR_AUTHOR and DEPENDABOT_EXCEPTION (the project's
  written exception for Dependabot, e.g. "EXC-004"; empty means Dependabot PRs are checked as any PR).

What it asks, at the project's Standard level:
- every PR: "**Riesgo:** N", never lower than COMPUTED_RISK; the technical report; no unchecked box;
- risk 2: also the owner's report (4 items) and the owner's line, in their own words;
- risk 3: also the owner's "Si sale mal, ¿qué pasaría?" line.
Light level asks the owner only at risk 3. It never checks spelling or wording: it only rejects
an empty line, template text, or a line that is nothing but an approval word.
"""

import os
import re
import sys
import unicodedata

OWNER_TITLES = ["con tus palabras", "lo entiendo"]  # "Lo entiendo" accepted during the transition
OWNER_REPORT, TECHNICAL = "informe para el dueno", "informe tecnico"
OWNER_ITEMS = ["Qué cambia", "Qué puede salir mal", "Cómo se deshace", "Recomendación"]
TECHNICAL_ITEMS = ["Cambios", "Verificado", "No verificado", "Limitaciones"]
NEEDS_LINK = {"Verificado"}  # "it works" only counts with a link to the CI run or to real output
IF_IT_FAILS = "si sale mal que pasaria"
APPROVAL_WORDS = {"ok", "okay", "si", "listo", "acepto", "aprobado", "lo entiendo", "entendido", "vale",
                  "dale", "de acuerdo", "conforme"}
RISK = re.compile(r"^\s*-?\s*\*\*Riesgo[^*]*?\*\*\s*:?\s*([123])(?!\d)", re.MULTILINE | re.IGNORECASE)
UNCHECKED = re.compile(r"^\s*[-*+]\s\[\s\]", re.MULTILINE)
LEVELS = {"ligero", "estandar", "estricto"}
REVIEWED = re.compile(r"^\s*[-*+]\s\[[xX]\]\s*R12 Revisado.*$", re.MULTILINE)
SHA = re.compile(r"\b[0-9a-f]{12,40}\b")  # 7 characters can be forged cheaply; 12 cannot
EMPTY_LINE = "Falta decir qué cambia; con pocas palabras basta. No importa la redacción ni la ortografía."


def plain(text: str) -> str:
    """Lowercase, without accents, punctuation or extra spaces: «¿Qué cambia?» → «que cambia»."""
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w\s]", " ", text).split())


def sections(body: str) -> dict[str, str]:
    """Text under each '## Title', keyed by its plain title."""
    found: dict[str, str] = {}
    parts = re.split(r"^##(?!#)[ \t]*(.*)$", body.replace("\r\n", "\n"), flags=re.MULTILINE)
    for title, text in zip(parts[1::2], parts[2::2]):
        text = re.split(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$", text, maxsplit=1, flags=re.MULTILINE)[0]
        found.setdefault(plain(title), text)  # a horizontal rule ends the section
    return found


def titles(body: str) -> list[str]:
    """Every '## Title' of the body, plain, duplicates included."""
    return [plain(t) for t in re.findall(r"^##(?!#)[ \t]*(.*)$", body.replace("\r\n", "\n"), re.MULTILINE)]


def section(body: str, *starts: str) -> str | None:
    """The first section whose plain title starts with one of `starts`."""
    for title, text in sections(body).items():
        if any(title.startswith(start) for start in starts):
            return text
    return None


def written(text: str) -> bool:
    """Not empty and not a <template placeholder> (anything that starts with '<')."""
    text = text.strip()
    return bool(text) and not text.startswith("<")


def items(text: str) -> dict[str, str]:
    """'- **Label · EN:** value' lines (also with '*' or '+'), keyed by the plain label in Spanish."""
    found = {}
    for match in re.finditer(r"^\s*[-*+]\s*\*\*(.+?)\*\*(.*)$", text, re.MULTILINE):
        label = plain(match.group(1).split("·")[0])
        found.setdefault(label, match.group(2).strip().lstrip(":").strip())
    return found


def missing_items(text: str | None, labels: list[str]) -> list[str]:
    if text is None:
        return labels
    found = items(text)
    missing = []
    for label in labels:
        value = found.get(plain(label))
        if value is None or not written(value):
            missing.append(label)
        elif label in NEEDS_LINK and "http" not in value:
            missing.append(f"{label} (con enlace)")
    return missing


def owner_says_what_changes(text: str | None) -> bool:
    """A line of the owner's own that is not template text, the risk-3 line or a bare approval."""
    if text is None:
        return False
    for line in text.splitlines():
        said = plain(line)
        if written(line) and said and not said.startswith(IF_IT_FAILS) and said not in APPROVAL_WORDS:
            return True
    return False


def owner_says_what_if_it_fails(text: str | None) -> bool:
    for line in (text or "").splitlines():
        if plain(line).startswith(IF_IT_FAILS):
            answer = line.split("?", 1)[-1].split(":", 1)[-1] if "?" in line or ":" in line else ""
            return written(answer) and bool(plain(answer)) and plain(answer) not in APPROVAL_WORDS
    return False


def review_problems(body: str, head_sha: str) -> list[str]:
    """The checked review line must name the commit it reviewed, and that commit must be the PR head."""
    line = REVIEWED.search(body)
    if line is None or not head_sha:
        return []
    shas = SHA.findall(line.group(0))
    if not shas:
        return ["La casilla de revisión debe decir en qué commit se revisó (SHA de 12 caracteres o más)."]
    if not any(head_sha.startswith(sha) for sha in shas):
        return [f"Hay cambios nuevos sin revisar: la revisión fue en {shas[-1][:7]} y el PR va en "
                f"{head_sha[:7]}. Hay que pedirle otra revisión a la IA, no a ti."]
    return []


def problems(body: str, computed: int, level: str = "estandar", head_sha: str = "") -> list[str]:
    """Everything the description still lacks, as friendly messages."""
    found = review_problems(body, head_sha)
    match = RISK.search(body)
    declared = int(match.group(1)) if match else 0
    if declared == 0:
        found.append(f"Falta el riesgo: escribe «**Riesgo:** 1, 2 o 3». El CI calculó {computed}.")
    elif declared < computed:
        found.append(f"El riesgo declarado ({declared}) es menor que el calculado ({computed}). "
                     "Puede subir, nunca bajar.")
    risk = max(declared, computed)
    asks_owner = risk == 3 if level == "ligero" else risk >= 2
    for starts, name in [(OWNER_TITLES, "«Con tus palabras» o «Lo entiendo»"),
                         ([OWNER_REPORT], "«Informe para el dueño»"), ([TECHNICAL], "«Informe técnico»")]:
        if sum(any(t.startswith(s) for s in starts) for t in titles(body)) > 1:
            found.append(f"Hay más de un título {name}: deja solo el de la plantilla.")
    if asks_owner:
        missing = missing_items(section(body, OWNER_REPORT), OWNER_ITEMS)
        if missing:
            found.append(f"Al informe para el dueño le falta: {', '.join(missing)}.")
        owner = section(body, *OWNER_TITLES)
        if not owner_says_what_changes(owner):
            found.append(EMPTY_LINE)
        if risk == 3 and not owner_says_what_if_it_fails(owner):
            found.append("Riesgo 3: falta la línea «Si sale mal, ¿qué pasaría?: …», con tus palabras.")
    missing = missing_items(section(body, TECHNICAL), TECHNICAL_ITEMS)
    if missing:
        found.append(f"Al informe técnico le falta: {', '.join(missing)}.")
    unchecked = len(UNCHECKED.findall(body))
    if unchecked:
        found.append(f"Quedan {unchecked} casilla(s) sin marcar: márcalas o escribe N/A.")
    return found


def main() -> int:
    computed_text = os.environ.get("COMPUTED_RISK", "").strip()
    if computed_text not in ("1", "2", "3"):
        print("::error::COMPUTED_RISK debe ser 1, 2 o 3 (lo calcula risk.py en el CI).")
        return 1
    level = plain(os.environ.get("KERNEL_LEVEL", "estandar")) or "estandar"
    if level not in LEVELS:
        print(f"::error::KERNEL_LEVEL desconocido ({level}): usa ligero, estandar o estricto.")
        return 1
    print(f"Riesgo calculado: {computed_text} · nivel del proyecto: {level}")
    if os.environ.get("IS_REVERT") == "1":
        print("Revert exacto de un cambio ya integrado: no se le pide nada al dueño.")
        return 0
    if os.environ.get("PR_AUTHOR") == "dependabot[bot]" and os.environ.get("DEPENDABOT_EXCEPTION", "").strip():
        if os.environ.get("DEPENDABOT_OK") != "1":
            print("::error::Este PR de Dependabot tiene commits de otra persona: se revisa como cualquier PR.")
            return 1
        print(f"PR de Dependabot, cubierto por {plain(os.environ['DEPENDABOT_EXCEPTION']).upper()}: "
              "todos los commits son de dependabot[bot].")
        return 0
    found = problems(os.environ.get("PR_BODY", ""), int(computed_text), level, os.environ.get("HEAD_SHA", ""))
    for problem in found:
        print(f"::error::{problem}")
    if not found:
        print("Descripción del PR completa.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

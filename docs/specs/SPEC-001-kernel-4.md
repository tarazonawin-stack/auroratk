# Spec · Kernel 4.0.0: la versión definitiva · the final version

- **ID:** SPEC-001 · **Fecha · Date:** 2026-11-24 · **Estado · Status:** aprobada · approved (el dueño respondió «a» a las 4 preguntas de la propuesta · *the owner answered "a" to the 4 proposal questions*)
- **Responsable · Owner:** Jose Alejandro Tarazona

## Objetivo · Goal
Dejar el kernel listo para usarse tal cual en proyectos con datos reales, empezando por GPEXT, sin que cada proyecto invente su propio proceso. Se corrigen las contradicciones, lo obligatorio pasa de texto a máquina (CI y *hook*) y la adopción se hace con un script. Después, el kernel se congela.
*Make the kernel usable as-is in projects with real data, starting with GPEXT, without each project inventing its own process. Fix contradictions, move what is mandatory from text to machines (CI and a hook), make adoption a script, then freeze the kernel.*

## Fuera de alcance · Out of scope
- Los carriles de GPEXT (`scripts/lane.py`): el riesgo 1/2/3 de `risk.py` ya cumple esa función. · *GPEXT's lanes: `risk.py` already does that.*
- Cambiar `risk.py` (está congelado) y tratar Dependabot como riesgo 1 (sigue abierto). · *Changing `risk.py` (frozen) or Dependabot as risk 1 (still open).*
- La regla semgrep `scoped(...)` de GPEXT: es propia de ese proyecto y se queda allí como personalización permitida. · *GPEXT's semgrep rule stays there as an allowed customization.*
- Adoptar la versión en GPEXT: eso se hace en una sesión aparte. · *Adopting it in GPEXT is a separate session.*

## Criterios de aceptación · Acceptance criteria
- **AC-01 (R02):** `size_check.py` cuenta por separado el código y la documentación (`.md`, `.rst`, `.txt`, `.adoc`). Falla si el código pasa de 400 líneas **o** si la documentación pasa de 200. · *Counts code and docs separately and fails above 400 code or 200 doc lines.*
- **AC-02 (R02):** `size_hook.py` funciona como *hook* `PostToolUse` de Claude Code. Tras un `git commit`, avisa desde el 80 % de cualquiera de los dos topes y frena a la IA (`decision: block`) al pasarlo. Con cualquier otro comando, o si git falla, no hace nada. · *Claude Code PostToolUse hook: warns from 80 % and blocks over a cap after `git commit`; otherwise silent.*
- **AC-03 (R02):** `plantillas/claude-settings.json` trae ese *hook*, y el repo del kernel lo usa. · *The settings template ships the hook; the kernel repo uses it.*
- **AC-04 (R13):** `size_check.py` falla si `AGENTS.md` pasa de 450 palabras. La plantilla cabe con margen; el detalle pasa a skills en `plantillas/skills/`. · *Fails when `AGENTS.md` exceeds 450 words; the template fits; detail moves to skills.*
- **AC-05 (R06):** `ejemplos/test_aislamiento_django.py` comprueba dos cosas: que toda URL exige login (salvo una lista de públicas) y que un id ajeno responde 404, igual que uno inexistente. Una prueba del kernel comprueba que el ejemplo compila. · *Isolation example: every URL needs login, and another user's id returns the same 404 as a missing one.*
- **AC-06 (R12/R09):** la «Definición de terminado» sigue a R12 por riesgo (en riesgo 1 no se le pide nada al dueño). R09 ya no dice que la compruebe el escáner de secretos. · *Definition of done follows R12 by risk; R09 no longer claims a secret scanner checks it.*
- **AC-07:** `plantillas/DATOS-REALES.md` reúne en una sola lista lo que hay que tener antes de usar datos reales (R06, R08, R09, R14, R16 y el perfil de país). · *One pre-real-data checklist.*
- **AC-08 (adopción):** `kernel_sync.py sync` copia desde una copia del kernel los archivos fijos (siempre) y las plantillas (solo si faltan). `check` falla si un archivo fijo falta o cambió respecto de la versión fijada en `.github/kernel.txt`, si sobra algo en `docs/kernel/`, o si `.claude/settings.json` perdió el *hook* o una regla `deny` de la plantilla. · *`sync` copies fixed files and missing templates; `check` fails on drift from the pinned version, extra files, or a weakened settings file.*
- **AC-09:** el CI de Django compara la copia del proyecto con el kernel de la versión fijada, descargado en el CI, y usa el `kernel_sync.py` de esa descarga, no el del proyecto. · *Django CI compares against the pinned kernel fetched in CI, using that fetch's script.*
- **AC-10:** `guias/adoptar.md` (ES/EN) explica «Cómo adoptar», «Migrar desde un proceso local» y qué se puede personalizar y qué no. · *Adoption guide.*
- **AC-11:** versión 4.0.0 en todos los archivos, `SHA256SUMS` regenerado y la política de congelación escrita en «Versiones del kernel». · *Version 4.0.0 everywhere, regenerated checksums, written freeze policy.*

## Abuso · Abuse (R01)
- **Una IA o una persona edita en el proyecto un script del kernel para aflojarlo.** Lo impide `check`, que corre desde el kernel descargado en el CI y no desde la copia del proyecto; además, `scripts/**` es riesgo 3. · *Editing a kernel script in a project: `check` runs from the fetched kernel, and `scripts/**` is risk 3.*
- **Quitar el *hook*.** `check` lo exige en `.claude/settings.json`. Límite: un *hook* reduce el riesgo, no es un candado; el CI vuelve a medir el tamaño (R13). · *Removing the hook: `check` requires it; the CI measures again anyway.*

## Datos y permisos · Data and permissions
- **Datos personales · Personal data:** ninguno · *none*. Solo cambian scripts, plantillas y textos · *Scripts, templates and text only.*

## Personas · People
- Español primero, inglés listo (R11); explicaciones para alguien que no programa. · *Spanish first, English ready; plain explanations.*

## Riesgos y preguntas abiertas · Risks and open questions
- Un proyecto con `docs/` grande cambia de comportamiento: un PR con más de 200 líneas de documentación ahora falla. Por eso es 4.0.0 (ver DEC-001). · *Projects with big doc PRs now fail: hence 4.0.0.*
- `check` necesita red en el CI para descargar el kernel (el repo es público). · *`check` needs network in CI to fetch the kernel.*

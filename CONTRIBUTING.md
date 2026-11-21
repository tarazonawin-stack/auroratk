# Cómo contribuir · Contributing

> Español · *English below each point*

¡Gracias por querer mejorar AuroraTK! El kernel se aplica a sí mismo: cada cambio pasa por las mismas puertas que pide.
*Thanks for helping improve AuroraTK! The kernel applies to itself: every change goes through the same gates it requires.*

## Qué aporta más · What helps most

- **Perfiles nuevos:** otros lenguajes (`stack-<nombre>.md`), tipos de proyecto (`tipo-<nombre>.md`) y países (`pais-<nombre>.md`, con fuentes oficiales y fecha de revisión). Copia la tabla de uno existente: cada regla necesita una herramienta o un "N/A" con su motivo.
  *New profiles: other languages, project types and countries (with official sources and a review date). Copy an existing table: every rule needs a tool or an "N/A" with a reason.*
- **Errores en los scripts de CI** (`perfiles/ci/`), con una prueba que falle antes del arreglo (R03). `risk.py` está **congelado**: no se aceptan palabras de alarma nuevas salvo que muestres una forma real de esquivarlo, con su prueba.
  *Bugs in the CI scripts, with a test that fails before the fix. `risk.py` is **frozen**: new alarm words only with a real bypass shown by a test.*
- **Casos reales:** qué pasó al aplicar el kernel en tu proyecto, en un issue.
  *Real cases: what happened when you applied the kernel to your project, in an issue.*

## Proponer o cambiar una regla · Proposing or changing a rule

Abre un issue antes del PR. Una regla nueva o más exigente debe traer:
*Open an issue before the PR. A new or stricter rule must bring:*

1. qué exige, en una o dos frases · *what it requires, in one or two sentences;*
2. cómo se comprueba (CI o revisión) · *how it is checked (CI or review);*
3. por qué, con un caso real · *why, with a real case;*
4. una fuente pública y reconocida (estándar, ley, estudio) · *a recognized public source (standard, law, study).*

Lo que no se puede comprobar va a *Principios*, no a las reglas. El autor decide qué entra al kernel y en qué versión.
*What cannot be checked goes under Principles, not rules. The author decides what enters the kernel and in which version.*

## Cómo se trabaja un PR · How a PR works

- Pequeño: una idea, ~200 líneas (R02). Español e inglés en el mismo PR (R11).
  *Small: one idea, ~200 lines. Spanish and English in the same PR.*
- `python3 -m unittest discover -s tests -v` en verde, y `SHA256SUMS` regenerado si cambias `KERNEL*.md` o `perfiles/*.md`.
  *Tests green, and `SHA256SUMS` regenerated if you change those files.*
- Completa la plantilla del PR; el CI calcula su riesgo (R12).
  *Fill in the PR template; CI computes its risk.*

## Certificado de origen · Developer Certificate of Origin

Firma cada commit con `git commit -s`. Así declaras que tienes derecho a aportar ese contenido bajo las licencias del repositorio ([DCO 1.1](https://developercertificate.org/)). Lo que aportas se publica con la licencia de su ruta (ver `LICENSE` y `REUSE.toml`).
*Sign off every commit with `git commit -s`, certifying you have the right to contribute it under the repository's licenses. Contributions are published under the license of their path.*

## Contenido generado por IA · AI-generated content

Se acepta, igual que el humano: pasa las mismas pruebas y la misma revisión (R13). Si una IA propone una dependencia, comprueba su nombre exacto en el registro oficial (R07).
*Accepted on the same terms as human work: same tests and review. If an AI suggests a dependency, check its exact name in the official registry.*

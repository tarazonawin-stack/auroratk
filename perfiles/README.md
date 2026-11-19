# Perfiles · Profiles

Un perfil traduce las reglas del kernel a herramientas concretas. Cada proyecto usa **un perfil de stack** y **un perfil de tipo**.
*A profile maps the kernel rules to concrete tools. Each project uses **one stack profile** and **one type profile**.*

| Stack | Tipo · Type |
|---|---|
| [Python / Django](stack-python.md) | [Web y apps · Web & apps](tipo-web.md) |
| [Node / TypeScript](stack-node-typescript.md) | [Juego · Game](tipo-juego.md) |
| [Java](stack-java.md) | [Librería y CLI · Library & CLI](tipo-libreria-cli.md) |
| [C++](stack-cpp.md) | [Automatización y agentes · Automation & agents](tipo-automatizacion.md) |

**País · Country (R09):** cada proyecto declara los países donde tiene usuarios. · *Each project declares the countries where it has users.*

| País · Country | Perfil · Profile |
|---|---|
| Perú · Peru | [pais-peru.md](pais-peru.md) |

¿Otro país? Crea `pais-<nombre>.md` copiando el de Perú, con fecha de revisión y fuentes oficiales, y valídalo con un abogado local. · *Another country? Copy the Peru profile, with a review date and official sources, and validate it with a local lawyer.*

**Comunes a todos los stacks · Common to every stack:**

| Regla · Rule | Herramienta · Tool |
|---|---|
| R05 Secretos · Secrets | `gitleaks` |
| R06 Análisis de seguridad · Security analysis | `semgrep` |
| R07 Dependencias · Dependencies | `osv-scanner` + Dependabot ([plantilla](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/plantillas/dependabot.yml)) o Renovate |
| R02 Tamaño · Size | [`ci/size_check.py`](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/perfiles/ci/size_check.py) (cualquier lenguaje · *any language*) |
| R06 Lista corta · Short checklist | [`asvs-corto.md`](asvs-corto.md) |
| R12 Riesgo y descripción del PR · Risk and PR description | [`ci/pr-description.yml`](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/perfiles/ci/pr-description.yml) + [`ci/risk.py`](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/perfiles/ci/risk.py) + [`ci/pr_check.py`](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/perfiles/ci/pr_check.py), ejecutados desde la rama principal · *run from the main branch* |
| R07 Dependencias nuevas · New dependencies | Comprobar el nombre exacto en el registro oficial (PyPI, npm, Maven Central) antes de instalar · *Check the exact name in the official registry before installing* |
| R14 Alertas · Alerts | Alertas del hosting o un servicio de errores (p. ej. Sentry, plan gratuito) · *Hosting alerts or an error service (e.g. Sentry free tier)* |
| R12 Gobierno · Governance | Protección de rama si el plan la permite; en repo privado gratuito, merge manual solo con CI en verde · *Branch protection if the plan allows it; on a free private repo, manual merge only with green CI* + [plantilla de PR](https://github.com/tarazonawin-stack/auroratk/blob/v2.1.0/plantillas/PULL_REQUEST_TEMPLATE.md) |

¿Falta tu stack? Crea `stack-<nombre>.md` copiando la tabla de uno existente: cada regla debe tener una herramienta o un "N/A" con su motivo.
*Missing your stack? Create `stack-<name>.md` by copying an existing table: every rule needs a tool or an "N/A" with a reason.*

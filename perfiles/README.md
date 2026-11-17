# Perfiles · Profiles

Un perfil traduce las reglas del kernel a herramientas concretas. Cada proyecto usa **un perfil de stack** y **un perfil de tipo**.
*A profile maps the kernel rules to concrete tools. Each project uses **one stack profile** and **one type profile**.*

| Stack | Tipo · Type |
|---|---|
| [Python / Django](stack-python.md) | [Web y apps · Web & apps](tipo-web.md) |
| [Node / TypeScript](stack-node-typescript.md) | [Juego · Game](tipo-juego.md) |
| [Java](stack-java.md) | [Librería y CLI · Library & CLI](tipo-libreria-cli.md) |
| [C++](stack-cpp.md) | [Automatización y agentes · Automation & agents](tipo-automatizacion.md) |

**Comunes a todos los stacks · Common to every stack:**

| Regla · Rule | Herramienta · Tool |
|---|---|
| R05 Secretos · Secrets | `gitleaks` |
| R06 Análisis de seguridad · Security analysis | `semgrep` |
| R07 Dependencias · Dependencies | `osv-scanner` + Dependabot o Renovate |
| R12 Gobierno · Governance | Protección de rama · Branch protection + [plantilla de PR](../plantillas/PULL_REQUEST_TEMPLATE.md) |

¿Falta tu stack? Crea `stack-<nombre>.md` copiando la tabla de uno existente: cada regla debe tener una herramienta o un "N/A" con su motivo.
*Missing your stack? Create `stack-<name>.md` by copying an existing table: every rule needs a tool or an "N/A" with a reason.*

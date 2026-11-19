# Changelog · Historial

Formato basado en *Keep a Changelog*; versionado semántico. · *Based on Keep a Changelog; semantic versioning.*

## [2.1.0] · 2026-11-19

Versión MENOR: ninguna regla se vuelve más exigente; se agregan herramientas y una recomendación. · *MINOR: no rule becomes stricter; tooling and a recommendation are added.*

### Corregido · Fixed
- **Enlaces rotos:** la etiqueta de la 2.0.0 se publicó como `v.2.0.0` y el kernel enlazaba a `v2.0.0`, así que todos sus enlaces fijados daban 404. Desde la 2.1.0 la etiqueta se escribe `vX.Y.Z` y una prueba revisa el formato. · *Broken links: the 2.0.0 tag was published as `v.2.0.0`; tags are now `vX.Y.Z`, checked by a test.*
- **Perfiles copiables:** `perfiles/README.md` y `stack-python.md` usaban enlaces relativos a `ci/` y `../plantillas/` que se rompen al copiarlos a `docs/kernel/` de un proyecto; ahora son enlaces absolutos fijados a la versión. · *Profiles used relative links that broke once copied; now pinned absolute links.*

### Añadido · Added
- **El kernel cumple lo que exige:** pruebas de sus scripts de CI (`tests/`, solo biblioteca estándar) y un CI propio (`.github/workflows/ci.yml`). *Por qué:* un fallo en `pr_check.py` aprobaría PRs incompletos en todos los proyectos a la vez. · *The kernel now tests its own CI scripts and has its own CI.*
- **`SHA256SUMS`** y un paso en el CI de Django que compara la copia de `docs/kernel/` con esas huellas. *Por qué:* la copia de GPEXT ya se había editado a mano en 4 archivos sin que nadie lo notara. · *Checksums and a CI step that catches hand-edited kernel copies.*
- **R12, recomendación:** que algunas revisiones las haga un modelo o herramienta distinta del que escribió el código, y que el PR diga cuál. *Por qué:* dos sesiones del mismo modelo comparten puntos ciegos. · *Recommend reviews by a different model or tool.*
- README: pasos para publicar una versión. · *Release steps in the README.*

### Cambiado · Changed
- CI de Django: acciones de GitHub fijadas a su commit exacto (mismas versiones que antes), con una prueba que lo exige. *Por qué:* una etiqueta se puede mover a otro código; un commit no (R07). · *Actions pinned to commit SHAs.*

## [2.0.0] · 2026-11-18

Versión MAYOR porque varias reglas se vuelven más exigentes. Revisada por tres sesiones independientes antes de integrar. · *MAJOR because several rules become stricter. Reviewed by three independent sessions before merging.*

### Más exigente · Stricter
- **R01:** pregunta de abuso en cada spec (con vía rápida para cambios triviales). · *Abuse question in every spec, with a trivial-change path.*
- **R02:** alerta a las 300 líneas por archivo y script de tamaño para cualquier lenguaje. · *300-line file warning and a language-agnostic size script.*
- **R03:** pruebas de mutación semanales en los módulos de negocio (≥ 60 % Estándar, ≥ 75 % Estricto); cada arreglo trae una prueba que fallaba antes; no valen pruebas sin verificación real. *Por qué:* las pruebas escritas por IA suelen pasar sin verificar nada y la cobertura no lo detecta. · *Weekly mutation testing; regression test per fix; no assertion-free tests.*
- **R05:** `.env.example` y ninguna clave secreta en el navegador. · *`.env.example`; no secrets in the browser.*
- **R07:** toda dependencia nueva se comprueba en el registro oficial con su nombre exacto y la aprueba un humano; actualizaciones automáticas con Dependabot. *Por qué:* las IA inventan nombres de librerías que luego se publican con código malicioso (*slopsquatting*). · *New dependencies verified and human-approved; Dependabot.*
- **R08:** prohibidas las consultas N+1 en listas; plan de vuelta atrás antes de migraciones irreversibles; en Estándar, una restauración probada antes de la primera salida a producción, en un entorno aislado que cuenta como producción. · *No N+1; rollback plan for irreversible migrations; tested restore in an isolated environment.*
- **R09:** consentimiento o base legal en todos los niveles; plazo de conservación; derechos de la persona (ver, corregir, exportar, borrar o anonimizar); procedimiento ante filtraciones; perfiles de país obligatorios, validados con un abogado antes de producción con datos reales. *Por qué:* las leyes cambian por país, pero sus principios (ISO/IEC 29100, OCDE) son comunes. · *Legal basis at every level, retention, rights, breach procedure, country profiles.*
- **R12:** el humano escribe en una línea qué hace el cambio y el CI lo comprueba; `docs/ESTADO.md` obligatorio; si algo se rompe, primero se revierte al último CI en verde. *Por qué:* aprobar sin entender debilita justo la habilidad de detectar errores. · *Understanding line checked by CI; state file; revert first.*
- **R13:** `AGENTS.md` corto (meta 150 líneas) con errores frecuentes de la IA; límite de gasto de IA y de CI; permisos mínimos del agente, aclarando que reducen el riesgo pero no son un candado. *Por qué:* las instrucciones innecesarias bajan el éxito de los agentes y suben su costo. · *Short AGENTS.md, spending cap, least-privilege settings.*

### Añadido · Added
- **R14 · Registros que avisan** (OWASP A09:2025), con el ID interno del usuario, nunca datos personales. · *Logs that alert, with internal user IDs.*
- **R15 · Claro para quien lo usa:** estados de carga, vacío y error; sistema de diseño; validación con una persona usuaria real. · *Clear for the people who use it.*
- Niveles aclarados: Estricto es para datos sensibles, clientes externos o dinero; contratistas dentro de tu sistema y el número de DNI de trabajadores quedan en Estándar. · *Levels clarified.*
- *Ligero* simplificado: N/A en R10 y R11; revisión independiente opcional en R12; solo mensajes de error claros en R15. · *Light level simplified.*
- R06 separado en núcleo sin excepciones y verificación ASVS, con la lista corta `perfiles/asvs-corto.md`. · *R06 core vs ASVS, with a short checklist.*
- R12 aplicable en un repo privado del plan gratuito de GitHub: el merge del dueño es la aprobación. · *R12 workable on GitHub's free private plan.*
- Activación por etapas que ubica todas las reglas, seleccionable en el CI con `KERNEL_STAGE`. · *Staged activation, selectable in CI.*
- `perfiles/ci/`: CI de Django, `pyproject` base y scripts de tamaño, descripción del PR y umbral de mutación. · *Ready-to-copy CI, base config and scripts.*
- `plantillas/claude-settings.json` y `plantillas/dependabot.yml`. · *Agent settings and Dependabot templates.*
- `perfiles/pais-peru.md`: primer perfil de país (Ley 29733 y Reglamento 2024). · *First country profile.*
- Principio "Aprende construyendo". · *"Learn by building" principle.*
- `KERNEL-CHAT.md` / `.en.md`: versión corta para chats sin repositorio. · *Short chat version.*
- `plantillas/ESTADO.md` y `ejemplos/SPEC-ejemplo.md`. · *State template and spec example.*
- Perfiles: umbrales exactos (complejidad 10, aviso 300, tope 400), mutación con umbral, N+1 y registros por stack; `django-stubs` y `pytest-django`; TBT en lugar de INP en laboratorio. · *Profiles updated.*
- Incluye la aclaración de la 1.0.1 (archivos de terceros en `third_party/` con su inventario `THIRD_PARTY.md`), que también aplica el script de tamaño; y R02 tampoco cuenta los archivos de traducción de la interfaz (`.po`, `.mo`), que revisa la prueba de paridad de R11. · *Includes the 1.0.1 third-party clarification; R02 also skips UI translation files.*
- Enlaces del kernel fijados a la etiqueta `v2.0.0`. · *Kernel links pinned to the `v2.0.0` tag.*

## [1.0.1] · 2026-11-17

### Aclarado · Clarified
- R07: los archivos de terceros copiados al repo (tipografías, íconos, scripts) son dependencias. Van en `third_party/`, con un glosario `THIRD_PARTY.md` (origen, versión, licencia, hash SHA-256) y cada licencia una sola vez en `LICENSES/` (estándar REUSE). Una prueba de CI comprueba el glosario y los hashes. · *R07: vendored third-party files are dependencies: `third_party/`, a `THIRD_PARTY.md` inventory with hashes, licenses once in `LICENSES/` (REUSE), checked in CI.*
- R02: los archivos registrados de `third_party/` y los textos de `LICENSES/` no cuentan para el tamaño del PR. · *R02: registered `third_party/` files and `LICENSES/` texts do not count toward PR size.*

### Por qué · Why
- Las tipografías de GPEXT (SPEC-002) sumaban líneas a R02 sin ser código propio, y no había un lugar fijo para su origen y licencia. Se publica como PARCHE porque R07 ya exigía licencias compatibles: esto dice cómo cumplirlo con archivos copiados. · *GPEXT's fonts counted toward R02 without being our code. Released as a PATCH because R07 already required compatible licenses.*

## [1.0.0] · 2026-11-17

### Aprobado · Approved
- Aprobado por el autor. Decisiones confirmadas: código en inglés e interfaz y documentación en ES/EN; nombre AuroraTK Kernel; primer proyecto: GPEXT (nivel Estándar, perfiles Python/Django + web). · *Approved by the author.*

### Añadido · Added
- Kernel universal y bilingüe con 13 reglas en cinco bloques (Construir, Proteger, Datos, Personas, Gobernar). · *Universal bilingual kernel with 13 rules in five blocks.*
- Niveles Ligero, Estándar y Estricto. · *Light, Standard and Strict levels.*
- Perfiles de stack (Python, Node/TypeScript, Java, C++) y de tipo (web, juego, librería/CLI, automatización). · *Stack and type profiles.*
- Plantillas: `AGENTS.md`, `CLAUDE.md`, spec, decisión, excepciones y plantilla de PR. · *Templates.*

### Origen · Origin
- Evoluciona del kernel K01–K12 de AuroraTK: lo comprobable pasó a reglas y lo demás a principios; se añadieron reglas por lo aprendido en dos prototipos (tamaño, errores ocultos, dependencias, idiomas, IA con límites). · *Evolves from AuroraTK's K01–K12.*

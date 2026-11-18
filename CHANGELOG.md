# Changelog · Historial

Formato basado en *Keep a Changelog*; versionado semántico. · *Based on Keep a Changelog; semantic versioning.*

## [2.0.0] · 2026-11-18

Versión MAYOR porque varias reglas se vuelven más exigentes (R01, R02, R03, R05, R07, R08, R09, R12 y R13). Revisada por una sesión independiente antes de integrar. · *MAJOR because several rules become stricter. Reviewed by an independent session before merging.*

### Más exigente · Stricter
- **R03:** pruebas de mutación en los módulos de negocio (≥ 60 % Estándar, ≥ 75 % Estricto); cada arreglo trae una prueba que fallaba antes; no valen pruebas sin verificación real. *Por qué:* las pruebas escritas por IA suelen pasar sin verificar nada y la cobertura no lo detecta. · *Mutation testing; regression test per fix; no assertion-free tests.*
- **R07:** toda dependencia nueva se comprueba en el registro oficial con su nombre exacto y la aprueba un humano. *Por qué:* las IA inventan nombres de librerías que luego se publican con código malicioso (*slopsquatting*). · *New dependencies verified in the official registry and human-approved.*
- **R08:** prohibidas las consultas N+1 en listas; en Estándar, respaldo automático y una restauración probada antes de la primera salida a producción. · *No N+1 queries; Standard needs a tested restore before first release.*
- **R12:** el humano escribe en una línea qué hace el cambio antes de aprobar; `docs/ESTADO.md` obligatorio; si algo se rompe, primero se revierte al último CI en verde. *Por qué:* aprobar sin entender debilita justo la habilidad de detectar errores. · *One-line understanding before approval; state file; revert first.*
- **R13:** `AGENTS.md` corto (meta 150 líneas) con sección de errores frecuentes de la IA. *Por qué:* las instrucciones innecesarias bajan el éxito de los agentes y suben su costo. · *Short AGENTS.md with frequent AI mistakes.*
- **R09:** plazo de conservación escrito y forma de borrar los datos al vencer; derechos de la persona (ver, corregir, exportar, borrar); procedimiento ante filtraciones; perfiles de país obligatorios. *Por qué:* las leyes cambian por país, pero sus principios (ISO/IEC 29100, OCDE) son comunes. · *Retention, data-subject rights, breach procedure, mandatory country profiles.*
- **R01:** pregunta de abuso en cada spec (con vía rápida para cambios triviales). · *Abuse question in every spec (with a trivial-change path).*
- **R02:** alerta a las 300 líneas por archivo. · *File warning at 300 lines.*
- **R05:** `.env.example` y ninguna clave secreta en el navegador. · *`.env.example`; no secrets in the browser.*
- **R08:** plan de vuelta atrás antes de migraciones irreversibles; la restauración se prueba en un entorno aislado que cuenta como producción. · *Rollback plan for irreversible migrations; restore tested in an isolated production-grade environment.*
- **R13:** límite de gasto de IA y de minutos de CI en `AGENTS.md`. · *AI and CI spending cap.*

### Añadido · Added
- **R14 · Registros que avisan** (OWASP A09:2025). · *Logs that alert.*
- **R15 · Claro para quien lo usa:** estados de carga, vacío y error; sistema de diseño; validación con una persona usuaria real. · *Clear for the people who use it.*
- Niveles aclarados: Estricto es para datos sensibles, clientes externos o dinero; datos de trabajadores para uso interno quedan en Estándar con R09. · *Levels clarified.*
- *Ligero* marcado N/A donde no aplica (R10, R11, R12, R15). · *Light marked N/A where it does not apply.*
- R06 separado en núcleo sin excepciones y verificación ASVS (con excepciones con fecha). · *R06 split into a no-exception core and ASVS verification.*
- R12 aplicable en un repo privado del plan gratuito de GitHub: el merge del dueño es la aprobación. · *R12 workable on GitHub's free private plan.*
- Activación por etapas que ubica todas las reglas. · *Staged activation covering every rule.*
- `perfiles/ci/python-django.yml` y `mutation_threshold.py`: CI listo para copiar. · *Ready-to-copy CI.*
- `plantillas/claude-settings.json`: permisos mínimos del agente. · *Least-privilege agent settings.*
- `perfiles/pais-peru.md`: primer perfil de país (Ley 29733 y Reglamento 2024). · *First country profile.*
- Principio "Aprende construyendo". · *"Learn by building" principle.*
- `KERNEL-CHAT.md` / `.en.md`: versión corta para chats sin repositorio. · *Short chat version.*
- `plantillas/ESTADO.md` y `ejemplos/SPEC-ejemplo.md`. · *State template and spec example.*
- Perfiles: umbrales exactos (complejidad 10, aviso 300, tope 400), mutación semanal con umbral, N+1 y registros por stack; `django-stubs` y `pytest-django`; TBT en lugar de INP en laboratorio. · *Profiles updated.*

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

# Changelog · Historial

Formato basado en *Keep a Changelog*; versionado semántico. · *Based on Keep a Changelog; semantic versioning.*

## [1.0.1] · 2026-11-17

### Aclarado · Clarified
- R07: los archivos de terceros copiados al repo (tipografías, íconos, scripts) son dependencias. Van en `third_party/`, con un glosario `THIRD_PARTY.md` (origen, versión, licencia, hash SHA-256) y cada licencia una sola vez en `LICENSES/` (estándar REUSE). Una prueba de CI comprueba el glosario y los hashes. · *R07: vendored third-party files are dependencies: `third_party/`, a `THIRD_PARTY.md` inventory with hashes, licenses once in `LICENSES/` (REUSE), checked in CI.*
- R02: los archivos de `third_party/` registrados no cuentan para el tamaño del PR. · *R02: registered `third_party/` files do not count toward PR size.*

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

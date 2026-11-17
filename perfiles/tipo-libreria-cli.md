# Tipo · Type: Librería y CLI · Library & CLI

| Tema · Topic | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| Versiones · Versions | Versionado semántico; cada cambio incompatible sube la versión MAYOR · *Semantic versioning; breaking changes bump MAJOR* | `CHANGELOG.md` al día · *up to date* |
| API pública · Public API | Toda función pública documentada con un ejemplo · *Every public function documented with an example* | Generador de documentación sin avisos · *Doc generator with no warnings* |
| R03 Pruebas · Tests | Cobertura ≥ 80 % de la API pública · *of the public API* | Cobertura en CI · *Coverage in CI* |
| R10 CLI | `--help` y `--version`; códigos de salida documentados (0 = éxito); salida legible sin color (`NO_COLOR`) · *documented exit codes; readable output without color* | Pruebas de la CLI · *CLI tests* |
| R11 Idiomas · Languages | Mensajes para personas en archivos de traducción; mensajes para máquinas (logs, códigos de error) en inglés estable · *Human messages translated; machine messages (logs, error codes) in stable English* | Paridad ES/EN · *ES/EN parity* |
| R08 Datos · Data | N/A salvo que guarde archivos: entonces, formatos versionados · *N/A unless it writes files: then versioned formats* | — |

# Perfil · Profile: C++ (CMake)

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | `clang-tidy` (`readability-function-cognitive-complexity`) | `clang-tidy -p build` |
| R03 Pruebas · Tests | GoogleTest o Catch2 + `llvm-cov` o `gcovr` | `ctest --output-on-failure` |
| R03 Mutación · Mutation | Mull sobre la lógica principal · *on core logic* | Ejecución de Mull en CI · *Mull run in CI* |
| R04 Estricto · Strict | `-Wall -Wextra -Wpedantic -Werror`, `clang-tidy`, `clang-format` | `cmake --build build && clang-format --dry-run --Werror` |
| R06 Seguridad · Security | Sanitizadores · Sanitizers: AddressSanitizer + UndefinedBehaviorSanitizer en las pruebas · *in tests* | Compilar las pruebas con `-fsanitize=address,undefined` |
| R07 Dependencias · Dependencies | vcpkg (con *baseline* fijada) o Conan (con *lockfile*) | Build reproducible desde el lock · *Reproducible build from lock* |
| R08 Datos · Data | Formatos de archivo versionados, con migración entre versiones · *Versioned file formats with migration* | Prueba de lectura de versiones antiguas · *Old-version read test* |
| R14 Registros · Logs | `spdlog` | Prueba de que cada acción crítica registra · *Test that each critical action logs* |
| R10 Accesibilidad · Accessibility | Según el tipo · *Per type*: [juego](tipo-juego.md) o [CLI](tipo-libreria-cli.md) | — |
| R11 Idiomas · Languages | `gettext` o archivos de recursos · *or resource files* | Prueba de paridad de claves · *Key parity test* |

**Notas · Notes**
- Preferir RAII y punteros inteligentes; prohibido `new`/`delete` manual salvo excepción escrita. *Prefer RAII and smart pointers; no manual `new`/`delete` without a written exception.*

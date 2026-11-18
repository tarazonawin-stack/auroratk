# Perfil · Profile: Python / Django

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | `ruff` (C901) + script de tamaño | `ruff check --select C901` |
| R03 Pruebas · Tests | `pytest` + `pytest-cov` | `pytest --cov --cov-fail-under=80` |
| R03 Mutación · Mutation | `mutmut` sobre los módulos de negocio · *on business modules* | `mutmut run` (≥ 60 % Estándar, ≥ 75 % Estricto) |
| R04 Estricto · Strict | `ruff` (lint + format) + `mypy --strict` | `ruff check . && ruff format --check . && mypy .` |
| R06 Seguridad · Security | Auth, permisos y CSRF de Django · Django auth, permissions & CSRF | `python manage.py check --deploy --fail-level WARNING` |
| R07 Dependencias · Dependencies | `uv` (lock) + `pip-audit` | `uv lock --check && pip-audit` |
| R08 Datos · Data | Migraciones de Django · Django migrations | `python manage.py makemigrations --check --dry-run` |
| R08 Consultas N+1 · N+1 queries | `select_related` / `prefetch_related` | Pruebas de listas con `assertNumQueries` · *List tests with `assertNumQueries`* |
| R14 Registros · Logs | `logging` de Python con formato JSON · *Python `logging` with JSON format* | Prueba de que cada acción crítica registra · *Test that each critical action logs* |
| R10 Accesibilidad · Accessibility | Playwright + axe | Ver · See [tipo-web](tipo-web.md) |
| R11 Idiomas · Languages | `gettext` de Django (`.po`) | Prueba de paridad de claves ES/EN · *ES/EN key parity test* |

**Notas · Notes**
- Base de datos recomendada: PostgreSQL. *Recommended database: PostgreSQL.*
- Prohibido · Forbidden: `except:` vacío, `except Exception: pass` (`ruff` BLE001, S110, E722).

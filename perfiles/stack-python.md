# Perfil · Profile: Python / Django

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | `ruff` (C901) + script de tamaño | `ruff check --select C901` |
| R03 Pruebas · Tests | `pytest` + `pytest-cov` | `pytest --cov --cov-fail-under=80` |
| R04 Estricto · Strict | `ruff` (lint + format) + `mypy --strict` | `ruff check . && ruff format --check . && mypy .` |
| R06 Seguridad · Security | Auth, permisos y CSRF de Django · Django auth, permissions & CSRF | `python manage.py check --deploy --fail-level WARNING` |
| R07 Dependencias · Dependencies | `uv` (lock) + `pip-audit` | `uv lock --check && pip-audit` |
| R08 Datos · Data | Migraciones de Django · Django migrations | `python manage.py makemigrations --check --dry-run` |
| R10 Accesibilidad · Accessibility | Playwright + axe | Ver · See [tipo-web](tipo-web.md) |
| R11 Idiomas · Languages | `gettext` de Django (`.po`) | Prueba de paridad de claves ES/EN · *ES/EN key parity test* |

**Notas · Notes**
- Base de datos recomendada: PostgreSQL. *Recommended database: PostgreSQL.*
- Prohibido · Forbidden: `except:` vacío, `except Exception: pass` (`ruff` BLE001, S110, E722).

# Perfil · Profile: Python / Django

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | `ruff` (C901 con `max-complexity = 10`) + script de tamaño (aviso 300, tope 400) | `ruff check --select C901` |
| R03 Pruebas · Tests | `pytest` + `pytest-django` + `pytest-cov` | `pytest --cov --cov-fail-under=80` |
| R03 Mutación · Mutation | `mutmut` sobre los módulos de negocio listados en `AGENTS.md` · *on the business modules listed in `AGENTS.md`* | Semanal · *Weekly*: `mutmut run`, luego `mutmut export-cicd-stats` y un script que falla bajo el umbral (60 % Estándar, 75 % Estricto) |
| R04 Estricto · Strict | `ruff` (lint + format) + `mypy --strict` con `django-stubs` · *with `django-stubs`* | `ruff check . && ruff format --check . && mypy .` |
| R06 Seguridad · Security | Auth, permisos y CSRF de Django · Django auth, permissions & CSRF | `python manage.py check --deploy --fail-level WARNING` |
| R07 Dependencias · Dependencies | `uv` (lock) + `pip-audit` | `uv lock --check && pip-audit` |
| R06 Aislamiento · Isolation | `pytest-django`: toda URL exige login y un id ajeno da el mismo 404 que uno inexistente · *every URL needs login; another user's id gives the same 404 as a missing one* | [`ejemplos/test_aislamiento_django.py`](https://github.com/tarazonawin-stack/auroratk/blob/v4.0.0/ejemplos/test_aislamiento_django.py) en `pytest` |
| R08 Datos · Data | Migraciones de Django · Django migrations | `python manage.py makemigrations --check --dry-run` |
| R08 Consultas N+1 · N+1 queries | `select_related` / `prefetch_related` | Pruebas de listas con `assertNumQueries` · *List tests with `assertNumQueries`* |
| R14 Registros · Logs | `logging` de Python con formato JSON · *Python `logging` with JSON format* | Prueba de que cada acción crítica registra · *Test that each critical action logs* |
| R10 Accesibilidad · Accessibility | Playwright + axe | Ver · See [tipo-web](tipo-web.md) |
| R11 Idiomas · Languages | `gettext` de Django (`.po`) | Prueba de paridad de claves ES/EN · *ES/EN key parity test* |

**Notas · Notes**
- Base de datos recomendada: PostgreSQL. *Recommended database: PostgreSQL.*
- `mutmut` no funciona en Windows: en la PC se usa con WSL (Linux dentro de Windows); en el CI corre en Linux sin problema. *`mutmut` doesn't run on Windows: use WSL locally; CI runs it on Linux.*
- CI listo para copiar · Ready-to-copy CI: [`ci/python-django.yml`](https://github.com/tarazonawin-stack/auroratk/blob/v4.0.0/perfiles/ci/python-django.yml) + configuración base · *base config* [`ci/pyproject-django.toml`](https://github.com/tarazonawin-stack/auroratk/blob/v4.0.0/perfiles/ci/pyproject-django.toml) + scripts en [`ci/`](https://github.com/tarazonawin-stack/auroratk/tree/v4.0.0/perfiles/ci).
- Antes de la etapa 1, crea una primera prueba simple: sin pruebas, `pytest` termina con código 5 y el CI falla. · *Create a first simple test before stage 1.*
- Prohibido · Forbidden: `except:` vacío, `except Exception: pass` (`ruff` BLE001, S110, E722).

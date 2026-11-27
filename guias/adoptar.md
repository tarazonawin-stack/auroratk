# Adoptar el kernel

> Español · [English](adoptar.en.md)
> Guía de trabajo. Un proyecto usa el kernel tal cual: copia una versión fija, la personaliza solo donde se permite y deja que el CI vigile la copia.

## Cómo adoptar (proyecto nuevo o existente)

1. **Descarga el kernel en la versión que vas a usar**, fuera de tu proyecto:
   `git clone --depth 1 --branch v4.0.1 https://github.com/tarazonawin-stack/auroratk ../auroratk`
2. **Copia el kernel al proyecto**, desde la carpeta del proyecto:
   `python3 ../auroratk/perfiles/ci/kernel_sync.py sync --from ../auroratk --ci python-django`
   Escribe `docs/kernel/`, `scripts/`, el flujo de R12, las skills y `.github/kernel.txt` con la versión. Las plantillas (`AGENTS.md`, `ci.yml`, `.claude/settings.json`…) se crean solo si faltan.
3. **Completa** `AGENTS.md` (nivel, perfiles, países y comandos; tope de 450 palabras) y une `perfiles/ci/pyproject-django.toml` a tu `pyproject.toml`.
4. **Comprueba:** `python3 ../auroratk/perfiles/ci/kernel_sync.py check --from ../auroratk`. El CI lo repite en cada PR con el kernel que descarga, no con tu copia.
5. **Activa el CI por etapas** (`KERNEL_STAGE`) y la protección de la rama si tu plan lo permite.
6. **Integra todo en un PR de riesgo 3**, con revisión independiente.

**Probar antes de la etiqueta final:** el dueño crea una etiqueta de prueba (`v4.0.0-rc.1`), se clona esa etiqueta y se usa `--ref v4.0.0-rc.1` en el paso 2. El CI solo acepta etiquetas, no ramas ni commits.
**Si ya tienes `.claude/settings.json`:** `sync` no lo toca; agrega a mano el bloque `hooks` y las reglas `deny` de la plantilla (`check` te dice qué falta). `.claude/settings.local.json` no lo revisa nadie: no lo uses para aflojar reglas.
**PR apilados:** el *hook* mide contra `origin/main`. Si un PR sale de otra rama, declara su base: `git config branch.<rama>.kernelbase <base>`.

## Qué se puede personalizar y qué no

| Del kernel: no se edita (lo vigila `check`) | Del proyecto: se personaliza |
|---|---|
| `docs/kernel/**` (reglas y perfiles) | `AGENTS.md`, dentro del tope de 450 palabras |
| `scripts/` del kernel: `risk.py`, `pr_check.py`, `pr_meta.py`, `size_check.py`, `size_hook.py`, `mutation_threshold.py`, `kernel_sync.py` | `.github/workflows/ci.yml`: se **agregan** pasos; los del nivel no se quitan |
| `.github/workflows/pr-description.yml` (R12) | `.github/riesgo.txt`: solo **agregar** casos de riesgo 3: rutas (`3 <ruta>`), palabras nuevas (`alarma <texto>`) y protecciones que no se pueden quitar (`quitar <texto>`, p. ej. `quitar scoped(`) |
| Skills del kernel en `.claude/skills/` | Skills propias, en otras carpetas de `.claude/skills/` |
| El *hook* de tamaño y las reglas `deny` de `.claude/settings.json` | Reglas `allow`, `ask` y más `deny` en ese mismo archivo |
| | Reglas de análisis propias (p. ej. `.semgrep/`), pruebas, `docs/` |
| | Romper una regla: solo con una excepción con fecha en `docs/excepciones.md` |

¿Algo del kernel no encaja? No lo cambies en el proyecto: abre un issue en el kernel. Si es un error con su prueba que falla, va a un parche (DEC-001).

## Actualizar a otra versión

1. Lee el `CHANGELOG.md` de la versión nueva.
2. Vuelve a correr `sync` desde el kernel nuevo: reemplaza los archivos del kernel y borra los que ya no existen en `docs/kernel/`.
3. Revisa a mano lo que cambió en las plantillas, porque `sync` no toca las tuyas.
4. Abre un PR de riesgo 3. Subir de versión es una decisión del dueño, nunca automática.

## Migrar desde un proceso local (el caso GPEXT)

Cuando un proyecto inventó su propio proceso, cada pieza local se cambia por la del kernel. Lo que el kernel no cubre se queda como personalización permitida.

| Pieza local | Qué hacer |
|---|---|
| Carriles verde/amarillo/rojo (`scripts/lane.py`) | Quitar: el riesgo 1/2/3 de `risk.py` hace ese trabajo desde la rama principal |
| `scripts/check_size.py` (400 de código + 200 de documentación) | Quitar: `size_check.py` mide lo mismo |
| *Hook* `.claude/hooks/size-after-commit.sh` | Quitar: `size_hook.py` lo reemplaza; agrega el bloque `hooks` de la plantilla a tu `.claude/settings.json` |
| `AGENTS.md` largo, o corto con detalle en skills | Rehacerlo desde la plantilla; las skills propias se quedan |
| Prueba de aislamiento de URL | Conservarla o partir de `ejemplos/test_aislamiento_django.py` |
| Regla semgrep propia (p. ej. `scoped(...)`) | Conservarla: el kernel no la cubre |
| Copia editada de `docs/kernel/` o de `scripts/` | `sync` la reemplaza; lo que se quería cambiar va a un issue del kernel |

Orden recomendado: un PR para quitar lo duplicado y correr `sync`, y otro para las personalizaciones. Los dos son de riesgo 3. Antes de crear la etiqueta de la versión, el CI del proyecto tiene que pasar con el kernel nuevo.

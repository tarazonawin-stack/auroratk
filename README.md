# AuroraTK Kernel

> Español · [English](README.en.md)

**Un estándar de calidad propio, universal y bilingüe, para construir software con IA sin declarar "listo" nada que no tenga evidencia.**

## Misión

La IA escribe rápido, pero se equivoca con total seguridad. Este kernel existe para que **cada proyecto nazca con reglas claras, evidencia de máquina y una persona que decide**, sin importar el lenguaje, el tipo de software ni la IA que se use.

## Qué es y qué no es

| Es | No es |
|---|---|
| 15 reglas comprobables, con su porqué y su fuente oficial. | Una aplicación ni un servicio. |
| Perfiles que traducen las reglas a herramientas por lenguaje y tipo de proyecto. | Una certificación ni una auditoría. |
| Plantillas listas para copiar a cada proyecto nuevo. | Un reemplazo de profesionales con experiencia. |
| Agnóstico a la IA: funciona con Claude, otras IAs o personas. | Algo que obligue a usar una herramienta de pago. |

## Qué puedes esperar

- **Proyectos que empiezan bien:** cada proyecto arranca con su spec, sus pruebas, su CI y sus límites desde el primer commit.
- **Menos sorpresas:** contraseñas en el código, errores silenciados, archivos gigantes o datos duplicados los detecta una máquina antes de que entren.
- **Una IA que se comporta igual en cada sesión,** porque las reglas y el mapa del proyecto están escritos en el repo, no en la memoria de nadie.
- **Poder juzgar sin ser experto:** si el CI está en verde y la revisión independiente aprobó, tienes evidencia; si no, sabes exactamente qué falta.
- **Lo que no puedes esperar:** cero errores. El kernel los reduce y los hace visibles; no los elimina.

## Cómo se usa en un proyecto nuevo

1. **Elige el nivel:** Ligero, Estándar o Estricto (ver [KERNEL.md](KERNEL.md#niveles)).
2. **Elige tus perfiles** en [`perfiles/`](perfiles/): uno de stack, uno de tipo y uno por cada país donde tendrás usuarios.
3. **Copia las plantillas** al proyecto:
   - `plantillas/AGENTS.md` → `AGENTS.md` (raíz), y complétalo.
   - `plantillas/CLAUDE.md` → `CLAUDE.md` (raíz).
   - `plantillas/PULL_REQUEST_TEMPLATE.md` → `.github/PULL_REQUEST_TEMPLATE.md`.
   - `KERNEL.md`, `KERNEL.en.md` y `SHA256SUMS` → `docs/kernel/`, y **todos** los perfiles (`perfiles/*.md`) → `docs/kernel/perfiles/`, para que la IA los vea (los que usa el proyecto se declaran en `AGENTS.md`). Cópialos sin editar y sin agregar nada: el CI del perfil falla si falta, sobra o cambió algún archivo respecto de `SHA256SUMS`.
   - `plantillas/dependabot.yml` → `.github/dependabot.yml`.
   - `plantillas/ESTADO.md` → `docs/ESTADO.md`.
   - `plantillas/claude-settings.json` → `.claude/settings.json` (permisos mínimos del agente, R13).
   - El CI de tu perfil, si existe (p. ej. `perfiles/ci/python-django.yml` → `.github/workflows/ci.yml`, y los scripts de `perfiles/ci/` → `scripts/`).
   - Crea `docs/specs/`, `docs/decisiones/` y `docs/excepciones.md` (desde `plantillas/EXCEPCIONES.md`).
4. **Configura el CI por etapas** con los comandos de tus perfiles (ver *Activación por etapas* en el kernel) y activa la protección de la rama principal si tu plan de GitHub lo permite (en un repo privado gratuito no: haz merge solo con el CI en verde).
5. **Trabaja así, cada vez:** spec → cambio pequeño con su prueba → CI → revisión independiente → escribes en una línea qué hace → tu aprobación → `docs/ESTADO.md` al día. ¿Dudas con la línea «Lo entiendo»? Lee la [guía](guias/lo-entiendo.md).

**¿Sin repositorio?** En un chat como Google AI Studio, pega [`KERNEL-CHAT.md`](KERNEL-CHAT.md) en las instrucciones del sistema.

## Estructura

```
KERNEL.md / KERNEL.en.md     el estándar (15 reglas, niveles, excepciones, versiones)
KERNEL-CHAT.md / .en.md      versión corta para pegar en un chat sin repositorio
perfiles/                    reglas → herramientas por stack, tipo de proyecto y país
plantillas/                  archivos para copiar a cada proyecto
ejemplos/                    ejemplos de cómo se ve bien hecho
guias/                       guías para quien aprueba sin programar a diario (p. ej. «Lo entiendo»)
tests/                       pruebas de los scripts de CI y de la coherencia del kernel
SHA256SUMS                   huellas de los archivos que se copian a docs/kernel/
CHANGELOG.md                 historial de versiones del kernel
```

## Estado

**Versión 2.1.0.** Las reglas, los perfiles y las plantillas están completos. Las configuraciones de CI listas para copiar se agregan por perfil a medida que cada uno se usa por primera vez en un proyecto real (el primero: GPEXT, con Python/Django + web).

## Publicar una versión

1. Anota el cambio en `CHANGELOG.md` y sube la versión en todos los archivos (las pruebas avisan si falta alguno).
2. Regenera las huellas: `sha256sum KERNEL.md KERNEL.en.md perfiles/*.md > SHA256SUMS`.
3. Verifica: `python3 -m unittest discover -s tests -v` (lo mismo que corre el CI).
4. Después del merge, crea la etiqueta **`vX.Y.Z`, sin punto después de la v** (por ejemplo `v2.1.0`): los enlaces del kernel apuntan a ese nombre exacto.

## Autoría y licencia

© 2026 Jose Alejandro Tarazona. Uso interno. Ver [LICENSE](LICENSE).

# AuroraTK Kernel

> Español · [English](README.en.md)

**Un estándar de calidad propio, universal y bilingüe, para construir software con IA sin declarar "listo" nada que no tenga evidencia.**

## Misión

La IA escribe rápido, pero se equivoca con total seguridad. Este kernel existe para que **cada proyecto nazca con reglas claras, evidencia de máquina y una persona que decide**, sin importar el lenguaje, el tipo de software ni la IA que se use.

## Qué es y qué no es

| Es | No es |
|---|---|
| 13 reglas comprobables, con su porqué y su fuente oficial. | Una aplicación ni un servicio. |
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
2. **Elige dos perfiles:** uno de stack y uno de tipo, en [`perfiles/`](perfiles/).
3. **Copia las plantillas** al proyecto:
   - `plantillas/AGENTS.md` → `AGENTS.md` (raíz), y complétalo.
   - `plantillas/CLAUDE.md` → `CLAUDE.md` (raíz).
   - `plantillas/PULL_REQUEST_TEMPLATE.md` → `.github/PULL_REQUEST_TEMPLATE.md`.
   - `KERNEL.md` → `docs/kernel/KERNEL.md`.
   - Crea `docs/specs/`, `docs/decisiones/` y `docs/excepciones.md` (desde `plantillas/EXCEPCIONES.md`).
4. **Configura el CI** con los comandos de tus perfiles y activa la protección de la rama principal.
5. **Trabaja así, cada vez:** spec → cambio pequeño con su prueba → CI → revisión independiente → tu aprobación.

## Estructura

```
KERNEL.md / KERNEL.en.md     el estándar (13 reglas, niveles, excepciones, versiones)
perfiles/                    reglas → herramientas por stack y por tipo de proyecto
plantillas/                  archivos para copiar a cada proyecto
CHANGELOG.md                 historial de versiones del kernel
```

## Estado

**Versión 1.0.0.** Las reglas, los perfiles y las plantillas están completos. Las configuraciones de CI listas para copiar se agregan por perfil a medida que cada uno se usa por primera vez en un proyecto real (el primero: GPEXT, con Python/Django + web).

## Autoría y licencia

© 2026 Jose Alejandro Tarazona. Uso interno. Ver [LICENSE](LICENSE).

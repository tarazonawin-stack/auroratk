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
- **Si usas una app hecha con el kernel:** se maneja con teclado y en un celular de 360 px, viene en español con el inglés listo, cada pantalla avisa cuando carga, está vacía o falla (con mensajes que dicen qué hacer), y tus datos personales se guardan con un fin y un plazo escritos.
- **Lo que no puedes esperar:** cero errores. El kernel los reduce y los hace visibles; no los elimina. Tampoco es una certificación, una auditoría ni una revisión legal.

## Para quién es: los tres niveles

Cada proyecto declara su nivel en su `AGENTS.md`. Cuando el software pasa a usarse con clientes o empresas externas, sube a Estricto.

| Nivel | Para qué | Ejemplos |
|---|---|---|
| **Ligero** | Experimentos y herramientas personales, sin datos de otros. | Un script, un prototipo, un ejercicio. |
| **Estándar** | Software que usan otras personas, incluidos datos de trabajadores para uso interno. | Una app interna, un juego publicado, una librería. |
| **Estricto** | Datos sensibles (salud, documentos de identidad, finanzas), clientes o usuarios externos, o dinero. | Producción con clientes, pagos. |

## Las 15 reglas en palabras simples

El detalle (qué exige, cómo se comprueba, por qué y su fuente) está en [KERNEL.md](KERNEL.md).

| ID | Regla | Qué significa |
|---|---|---|
| R01 | Spec antes de código | Todo cambio nace de una nota con objetivo, límites y cómo podría abusarse. |
| R02 | Pequeño y legible | Un cambio es una idea, de hasta 400 líneas; los archivos avisan a las 300. |
| R03 | Pruebas que prueban | Cada criterio tiene una prueba que verifica el resultado, no solo que "no falló". |
| R04 | Sin errores ocultos | Prohibido tragarse un error: se maneja, se registra o se muestra. |
| R05 | Cero secretos en el repo | Claves y contraseñas solo en variables de entorno. Sin excepciones. |
| R06 | Seguridad con piezas probadas | Login, permisos y cifrado con librerías maduras; permisos validados en el servidor. |
| R07 | Dependencias bajo control | Una librería nueva se verifica en el registro oficial y la aprueba un humano. |
| R08 | Datos fiables | Migraciones, nada se borra sin confirmar, respaldos que se prueban restaurando. |
| R09 | Datos personales con cuidado | Solo lo mínimo, con base legal, derechos de la persona y perfil de país. |
| R10 | Accesible | Usable con teclado y en celular de 360 px (WCAG 2.2 AA). |
| R11 | Bilingüe | Ningún texto de la interfaz va fijo en el código; español base e inglés listo. |
| R12 | Quien construye no aprueba | CI en verde, revisión independiente y tu aprobación; todo queda escrito y se puede volver atrás. |
| R13 | IA con límites | Instrucciones cortas para la IA, permisos mínimos y límite de gasto. |
| R14 | Registros que avisan | Errores y acciones críticas quedan registrados, sin datos personales, y un error grave genera una alerta. |
| R15 | Claro para quien lo usa | Estados de carga, vacío y error en cada pantalla, y una persona real valida el flujo principal. |

## Cómo se usa en un proyecto nuevo

1. **Elige el nivel:** Ligero, Estándar o Estricto (ver [KERNEL.md](KERNEL.md#niveles)).
2. **Elige tus perfiles** en [`perfiles/`](perfiles/): uno de stack, uno de tipo y uno por cada país donde tendrás usuarios.
3. **Copia las plantillas** al proyecto:
   - `plantillas/AGENTS.md` → `AGENTS.md` (raíz), y complétalo.
   - `plantillas/CLAUDE.md` → `CLAUDE.md` (raíz).
   - `plantillas/PULL_REQUEST_TEMPLATE.md` → `.github/PULL_REQUEST_TEMPLATE.md`.
   - `KERNEL.md` y los perfiles elegidos → `docs/kernel/`, para que la IA los vea.
   - `plantillas/dependabot.yml` → `.github/dependabot.yml`.
   - `plantillas/ESTADO.md` → `docs/ESTADO.md`.
   - `plantillas/claude-settings.json` → `.claude/settings.json` (permisos mínimos del agente, R13).
   - El CI de tu perfil, si existe (p. ej. `perfiles/ci/python-django.yml` → `.github/workflows/ci.yml`, y los scripts de `perfiles/ci/` → `scripts/`).
   - Crea `docs/specs/`, `docs/decisiones/` y `docs/excepciones.md` (desde `plantillas/EXCEPCIONES.md`).
4. **Configura el CI por etapas** con los comandos de tus perfiles (ver *Activación por etapas* en el kernel) y activa la protección de la rama principal si tu plan de GitHub lo permite (en un repo privado gratuito no: haz merge solo con el CI en verde).
5. **Trabaja así, cada vez:** spec → cambio pequeño con su prueba → CI → revisión independiente → escribes en una línea qué hace → tu aprobación → `docs/ESTADO.md` al día.

**¿Sin repositorio?** En un chat como Google AI Studio, pega [`KERNEL-CHAT.md`](KERNEL-CHAT.md) en las instrucciones del sistema.

## Preguntas frecuentes

- **¿Necesito saber programar?** No ser experto, pero sí entender lo bastante para escribir en una línea qué hace cada cambio antes de aprobarlo. La IA explica el porqué de cada decisión.
- **¿Qué es el CI?** Un comprobador automático que corre en cada cambio y lo bloquea si algo falla.
- **¿Y si una regla no encaja?** Se puede romper solo con una excepción escrita en `docs/excepciones.md`, con motivo, riesgo, responsable y fecha de vencimiento. R05 y el núcleo de R06 no admiten excepciones.
- **¿Qué país cubre?** El primer perfil de país es Perú (Ley 29733 y su Reglamento de 2024). Para otro país se crea su perfil antes de producción.

## Estructura

```
KERNEL.md / KERNEL.en.md     el estándar (15 reglas, niveles, excepciones, versiones)
KERNEL-CHAT.md / .en.md      versión corta para pegar en un chat sin repositorio
perfiles/                    reglas → herramientas por stack, tipo de proyecto y país
plantillas/                  archivos para copiar a cada proyecto
ejemplos/                    ejemplos de cómo se ve bien hecho
CHANGELOG.md                 historial de versiones del kernel
```

## Estado

**Versión 2.0.0.** Las reglas, los perfiles y las plantillas están completos. Las configuraciones de CI listas para copiar se agregan por perfil a medida que cada uno se usa por primera vez en un proyecto real (el primero: GPEXT, con Python/Django + web).

## Autoría y licencia

© 2026 Jose Alejandro Tarazona. Uso interno. Ver [LICENSE](LICENSE).

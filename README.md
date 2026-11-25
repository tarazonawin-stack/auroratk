# AuroraTK Kernel

> Español · [English](README.en.md)

**Un estándar de calidad propio, universal y bilingüe, para construir software con IA sin declarar "listo" nada que no tenga evidencia.**

## Misión

La IA escribe rápido, pero se equivoca con total seguridad. Este kernel existe para que **cada proyecto nazca con reglas claras, evidencia de máquina y una persona que decide**, sin importar el lenguaje, el tipo de software ni la IA que se use.

## Qué es y qué no es

| Es | No es |
|---|---|
| 16 reglas comprobables, con su porqué y su fuente oficial. | Una aplicación ni un servicio. |
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

## Las 16 reglas en palabras simples

El detalle (qué exige, cómo se comprueba, por qué y su fuente) está en [KERNEL.md](KERNEL.md).

| ID | Regla | Qué significa |
|---|---|---|
| R01 | Spec antes de código | Todo cambio nace de una nota con objetivo, límites y cómo podría abusarse. |
| R02 | Pequeño y legible | Un cambio es una idea: hasta 400 líneas de código y 200 de documentación; los archivos avisan a las 300. |
| R03 | Pruebas que prueban | Cada criterio tiene una prueba que verifica el resultado, no solo que "no falló". |
| R04 | Sin errores ocultos | Prohibido tragarse un error: se maneja, se registra o se muestra. |
| R05 | Cero secretos en el repo | Claves y contraseñas solo en variables de entorno. Sin excepciones. |
| R06 | Seguridad con piezas probadas | Login, permisos y cifrado con librerías maduras; permisos validados en el servidor. |
| R07 | Dependencias bajo control | Una librería nueva se verifica en el registro oficial y la aprueba un humano. |
| R08 | Datos fiables | Migraciones, nada se borra sin confirmar, respaldos que se prueban restaurando. |
| R09 | Datos personales con cuidado | Solo lo mínimo, con base legal, derechos de la persona y perfil de país. |
| R10 | Accesible | Usable con teclado y en celular de 360 px (WCAG 2.2 AA). |
| R11 | Bilingüe | Ningún texto de la interfaz va fijo en el código; español base e inglés listo. |
| R12 | Quien construye no aprueba | CI en verde, revisión independiente y tu merge; según el riesgo del cambio, dices con tus palabras qué cambia. Todo queda escrito y se puede volver atrás. |
| R13 | IA con límites | Instrucciones cortas para la IA, permisos mínimos y límite de gasto. |
| R14 | Registros que avisan | Errores y acciones críticas quedan registrados, sin datos personales, y un error grave genera una alerta. |
| R15 | Claro para quien lo usa | Estados de carga, vacío y error en cada pantalla, y una persona real valida el flujo principal. |
| R16 | Desplegar sin miedo y volver atrás | Publica el CI con tu aprobación, se comprueba tras desplegar y volver a la versión anterior está probado. |

## Cómo se usa en un proyecto nuevo

1. **Elige el nivel:** Ligero, Estándar o Estricto (ver [KERNEL.md](KERNEL.md#niveles)).
2. **Elige tus perfiles** en [`perfiles/`](perfiles/): uno de stack, uno de tipo y uno por cada país donde tendrás usuarios.
3. **Copia el kernel con un comando** (`perfiles/ci/kernel_sync.py sync`): deja `docs/kernel/`, los scripts, el flujo de R12, las skills y las plantillas que falten, con la versión fijada en `.github/kernel.txt`. El CI comprueba con `check` que nadie edite la copia. Pasos, qué se puede personalizar y cómo migrar desde un proceso propio: [guía «Adoptar»](guias/adoptar.md).
4. **Configura el CI por etapas** con los comandos de tus perfiles (ver *Activación por etapas* en el kernel) y activa la protección de la rama principal si tu plan de GitHub lo permite (en un repo privado gratuito no: haz merge solo con el CI en verde).
5. **Trabaja así, cada vez:** spec → cambio pequeño con su prueba → CI → revisión independiente → según el riesgo, dices con tus palabras qué cambia → tu aprobación → `docs/ESTADO.md` al día. ¿Dudas con «Con tus palabras»? Lee la [guía](guias/lo-entiendo.md). ¿Varias sesiones de IA a la vez? Lee [La oficina](guias/oficina.md).

**¿Sin repositorio?** En un chat como Google AI Studio, pega [`KERNEL-CHAT.md`](KERNEL-CHAT.md) en las instrucciones del sistema.

## Preguntas frecuentes

- **¿Necesito saber programar?** No ser experto, pero sí entender lo bastante para decir con tus palabras qué cambia en los cambios de riesgo 2 y 3 (los de rutina no te piden nada). La IA explica el porqué de cada decisión.
- **¿Qué es el CI?** Un comprobador automático que corre en cada cambio y lo bloquea si algo falla.
- **¿Y si una regla no encaja?** Se puede romper solo con una excepción escrita en `docs/excepciones.md`, con motivo, riesgo, responsable y fecha de vencimiento. R05 y el núcleo de R06 no admiten excepciones.
- **¿Qué país cubre?** El primer perfil de país es Perú (Ley 29733 y su Reglamento de 2024). Para otro país se crea su perfil antes de producción.

## Estructura

```
KERNEL.md / KERNEL.en.md     el estándar (16 reglas, niveles, excepciones, versiones)
KERNEL-CHAT.md / .en.md      versión corta para pegar en un chat sin repositorio
perfiles/                    reglas → herramientas por stack, tipo de proyecto y país
plantillas/                  archivos para copiar a cada proyecto
ejemplos/                    ejemplos de cómo se ve bien hecho
guias/                       guías: «Adoptar», «Con tus palabras» (para quien aprueba) y «La oficina» (sesiones en paralelo)
plantillas/roles/            instrucciones por rol: analista, coordinador, especialista, revisor y avance
tests/                       pruebas de los scripts de CI y de la coherencia del kernel
SHA256SUMS                   huellas de los archivos que se copian a docs/kernel/
CHANGELOG.md                 historial de versiones del kernel
LICENSE, LICENSES/, REUSE.toml  licencias por tipo de archivo (CC BY 4.0, MIT, MIT-0)
CITATION.cff, CONTRIBUTING.md   cómo citarlo y cómo aportar
```

## Estado

**Versión 4.0.0.** Congelada: parches solo con una prueba que falle antes, versiones menores solo con perfiles nuevos y una mayor solo ante un problema real (ver *Versiones del kernel*). Las reglas, los perfiles y las plantillas están completos. Las configuraciones de CI listas para copiar se agregan por perfil a medida que cada uno se usa por primera vez en un proyecto real (el primero: GPEXT, con Python/Django + web).

## Publicar una versión

1. Comprueba que el cambio cabe en la política de congelación (DEC-001). Anota el cambio en `CHANGELOG.md` y sube la versión en todos los archivos, incluido `CITATION.cff` (las pruebas avisan si falta alguno).
2. Regenera las huellas: `sha256sum KERNEL.md KERNEL.en.md perfiles/*.md > SHA256SUMS`.
3. Verifica: `python3 -m unittest discover -s tests -v` (lo mismo que corre el CI).
4. Después del merge y de probarla en un proyecto real (con una etiqueta de prueba `vX.Y.Z-rc.N`), crea la etiqueta **`vX.Y.Z`, sin punto después de la v** (por ejemplo `v4.0.0`): los enlaces del kernel apuntan a ese nombre exacto.

## Autoría y licencia

© 2026 Jose Alejandro Tarazona.

- **Texto del estándar** (kernel, perfiles, guías y documentación): [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Úsalo y adáptalo citando: «Basado en AuroraTK Kernel, © 2026 Jose Alejandro Tarazona, CC BY 4.0».
- **Scripts de CI y pruebas:** [MIT](LICENSES/MIT.txt).
- **Plantillas y ejemplos:** [MIT-0](LICENSES/MIT-0.txt), cópialos sin conservar ningún aviso.

Detalle por ruta en [`REUSE.toml`](REUSE.toml); resumen en [LICENSE](LICENSE). Para citarlo: [`CITATION.cff`](CITATION.cff). ¿Quieres aportar? Lee [CONTRIBUTING.md](CONTRIBUTING.md).

# La oficina: varias sesiones de IA en paralelo

> Español · [English](oficina.en.md)
> Guía de trabajo. No cambia ninguna regla: muestra cómo cumplirlas cuando varias sesiones de IA trabajan a la vez, cada una con su especialidad.

## Cuándo conviene

Trabajar en paralelo **ahorra tiempo de reloj, pero cuesta más tokens**: cada sesión paga su propio contexto. Conviene cuando hay varias funciones independientes listas para construir y el proyecto tiene su límite de gasto escrito (R13). No conviene en un proyecto que recién empieza, ni cuando las tareas tocan los mismos archivos.

## Los roles

| Rol | Qué hace | Cuántos |
|---|---|---|
| **Analista** | Entrevista al dueño, escribe la visión y las specs con sus criterios (R01) y propone nivel y perfiles | 1, al inicio de cada fase |
| **Coordinador** | Divide el trabajo, escribe los acuerdos entre partes, asigna tareas y propone el orden de integración. **Es el único que edita `docs/ESTADO.md` y `AGENTS.md`**, y lo hace dentro del PR de cada especialista antes del merge (R12) | 1, siempre |
| **Especialista** | Construye una tarea en su propia rama y su propio PR (R02, R03) | 2 o 3 a la vez |
| **Revisor** | Revisa cada PR según R12, idealmente con otro modelo; puede revisar un grupo, anotando el commit de cada PR | 1 por grupo de PR |
| **Avance** | Cada cierto tiempo resume para el dueño qué se hizo, qué sigue y qué está bloqueado | 1 tarea programada |

Cada rol tiene su plantilla en [`plantillas/roles/`](../plantillas/roles/): se pega como instrucción al abrir la sesión.

## Cómo dividir el trabajo

- **Por función completa** (porción vertical): cada especialista hace una función de punta a punta (pantalla, lógica, datos y pruebas). Es la forma por defecto: los especialistas casi no se pisan.
- **Por capas** (frontend, backend, base de datos) solo si el proyecto ya está separado así, por ejemplo una app web que habla con una API, y el contrato de la API está escrito antes.
- **La documentación va dentro de cada PR**, no en un documentador aparte: R12 pide que `AGENTS.md`, decisiones y estado reflejen el cambio en el mismo PR.

## Las cinco reglas de la oficina

1. **Primero los acuerdos, después el paralelo.** El coordinador integra una spec o decisión corta con lo que se comparte (modelos, URLs, permisos, contrato de API). Recién entonces arrancan los especialistas.
2. **Archivos separados.** Cada tarea declara qué carpetas toca; si dos se cruzan, van una después de otra.
3. **Un solo dueño de las migraciones** por ronda, o un orden fijo para crearlas (R08).
4. **Pocos a la vez:** 2 o 3 especialistas y un tope de PR abiertos (por ejemplo, 5). Más multiplica el gasto y los conflictos.
5. **Un solo escritor** de `docs/ESTADO.md` y `AGENTS.md`: el coordinador, que sube esos cambios a la rama del PR del especialista antes del merge, para que entren en el mismo PR (R12).

## El flujo

1. **Analista:** entrevista al dueño (plantilla `analista.md`) y deja la visión y las specs. El dueño confirma.
2. **Coordinador:** integra los acuerdos y reparte las tareas, cada una con objetivo, criterios, carpetas permitidas, tope de líneas y de gasto.
3. **Especialistas:** trabajan en paralelo; cada uno abre su PR con la plantilla de PR del kernel.
4. **Revisor:** revisa cada PR según R12 (en Estándar, todos; una excepción escrita del proyecto puede ajustarlo).
5. **Coordinador:** completa `docs/ESTADO.md` y `AGENTS.md` en cada PR y propone el orden; **el dueño integra** (R12), salvo que una excepción escrita lo delegue. Luego abre la siguiente ronda.
6. **Avance:** informe periódico al dueño, en palabras simples.

## Con qué herramientas

- **Claude Code en la nube:** el coordinador puede crear otras sesiones con su tarea y su rama; los subagentes pueden trabajar en una copia aislada del repositorio; el avance es una tarea programada.
- **Cualquier otra IA o un chat:** se abre una conversación por rol y se pega su plantilla.
- **Permisos (R13):** toda sesión o subagente usa los permisos del proyecto (`.claude/settings.json`, plantilla `plantillas/claude-settings.json`) y nunca más que el coordinador; cada tarea lleva su tope de gasto.

## Chats cortos y baratos

Cada mensaje vuelve a pagar todo el chat, y una sesión parada esperando un permiso no avanza. Visto en GPEXT:

1. **Permisos fijos para lo rutinario:** los comandos de solo lectura y las pruebas van permitidos en `.claude/settings.json` (lo aprueba el dueño, R13); así ninguna sesión se queda bloqueada esperando un clic.
2. **Encargos en archivo:** cada tarea vive en `docs/tareas/<nombre>.md` y el mensaje que abre la sesión solo dice «lee y haz `docs/tareas/<nombre>.md`». Se borra en el PR que la completa.
3. **Vigilar con poco texto:** el coordinador o el lanzador revisa el estado breve de cada sesión, nunca su historial completo.
4. **Modelo según la tarea:** uno rápido y barato para lanzar y vigilar, uno intermedio para programar lo que ya tiene spec, el más capaz para specs y revisiones críticas.
5. **Cerrar al terminar:** al acabar la tarea, o si el chat se alarga, la sesión deja lo pendiente en `docs/ESTADO.md` y se archiva; la siguiente lee solo eso y su encargo.
6. **Preguntas juntas:** las decisiones del dueño van en una sola lista numerada al final, con 2–3 opciones y la recomendada primero; mientras tanto se sigue con la recomendada, marcada «por confirmar», y el dueño responde con números.

## Lo que no hace

No reemplaza al dueño: él decide la visión, el orden y qué se integra (R12). Si la oficina no ahorra tiempo frente a trabajar en secuencia, se vuelve a una sola sesión: mide sesiones, PR y conflictos por función.

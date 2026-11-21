# La oficina: varias sesiones de IA en paralelo

> Español · [English](oficina.en.md)
> Guía de trabajo. No cambia ninguna regla: muestra cómo cumplirlas cuando varias sesiones de IA trabajan a la vez, cada una con su especialidad.

## Cuándo conviene

Trabajar en paralelo **ahorra tiempo de reloj, pero cuesta más tokens**: cada sesión paga su propio contexto. Conviene cuando hay varias funciones independientes listas para construir y el proyecto tiene su límite de gasto escrito (R13). No conviene en un proyecto que recién empieza, ni cuando las tareas tocan los mismos archivos.

## Los roles

| Rol | Qué hace | Cuántos |
|---|---|---|
| **Analista** | Entrevista al dueño, escribe la visión y las specs con sus criterios (R01) y propone nivel y perfiles | 1, al inicio de cada fase |
| **Coordinador** | Divide el trabajo, escribe los acuerdos entre partes, asigna tareas, decide el orden de integración. **Es el único que edita `docs/ESTADO.md` y `AGENTS.md`** | 1, siempre |
| **Especialista** | Construye una tarea en su propia rama y su propio PR (R02, R03) | 2 o 3 a la vez |
| **Revisor** | Revisa los PR, idealmente con otro modelo (R12) | 1 por grupo de PR |
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
5. **Un solo escritor** de `docs/ESTADO.md` y `AGENTS.md`: el coordinador.

## El flujo

1. **Analista:** entrevista al dueño (plantilla `analista.md`) y deja la visión y las specs. El dueño confirma.
2. **Coordinador:** integra los acuerdos y reparte las tareas, cada una con objetivo, criterios, carpetas permitidas, tope de líneas y de gasto.
3. **Especialistas:** trabajan en paralelo; cada uno abre su PR con la plantilla de PR del kernel.
4. **Revisor:** revisa por grupo; en riesgo 3, siempre.
5. **Coordinador:** integra en el orden decidido, actualiza `docs/ESTADO.md` y abre la siguiente ronda.
6. **Avance:** informe periódico al dueño, en palabras simples.

## Con qué herramientas

- **Claude Code en la nube:** el coordinador puede crear otras sesiones con su tarea y su rama; los subagentes pueden trabajar en una copia aislada del repositorio; el avance es una tarea programada.
- **Cualquier otra IA o un chat:** se abre una conversación por rol y se pega su plantilla.

## Lo que no hace

No reemplaza al dueño: él decide la visión, el orden y qué se integra (R12). Si la oficina no ahorra tiempo frente a trabajar en secuencia, se vuelve a una sola sesión: mide sesiones, PR y conflictos por función.

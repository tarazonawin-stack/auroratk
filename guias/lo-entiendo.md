# Guía: «Con tus palabras» (R12)

> Español · [English](lo-entiendo.en.md) · Antes se llamaba «Lo entiendo».

Para quien aprueba los cambios y no programa a diario. Se lee en 3 minutos.

## Qué es

En los PR de riesgo 2 y 3 hay una sección **«Con tus palabras: ¿qué cambia con este PR?»**. Ahí dices, con pocas palabras tuyas, escritas o dictadas, **qué cambia** cuando el PR entra.

- **Es para ti:** te ayuda a notar si algo no cuadra antes de integrarlo. No es un examen ni una firma.
- **No tienes que entender cada línea de código.** Basta con entender **qué cambia y a quién afecta**. Que el código funcione lo comprueban el CI y la revisión de otra sesión.

## Cuánto te toca: lo dice el riesgo

| Riesgo | Ejemplo | Qué haces tú |
|---|---|---|
| **1 · rutina** | Actualizar `docs/ESTADO.md` | Nada |
| **2 · normal** | Una pantalla nueva | Lees el informe (está arriba, sin tecnicismos) y dices en pocas palabras qué cambia |
| **3 · crítico** | Tocar permisos, el CI o las dependencias | Lo mismo, y además «Si sale mal, ¿qué pasaría?». Si no lo tienes claro, no integres todavía: esperar no rompe nada |

El riesgo **lo calcula el CI** según los archivos y las líneas que cambia el PR. La IA puede subirlo, nunca bajarlo. No confundir: `trivial` significa que el cambio no necesita spec; el **riesgo** dice cuánto tienes que mirar tú.

## Cuatro promesas

1. **Las faltas no importan.** Nadie corrige ni califica tu redacción ni tu ortografía.
2. **Lo que puede cambiar tu decisión va arriba**, en tu parte del PR: riesgos, lo que no se deshace, datos de personas, costos. Lo de abajo («Para la revisión técnica») no necesitas leerlo.
3. **Si la explicación de la IA estaba mal, el error es de la IA y de la revisión, no tuyo.** Se anota en «Errores frecuentes de la IA aquí».
4. **Deshacer nunca te pide escribir nada.**

## ¿Ya sé qué cambia? Prueba rápida

Puedes responder **sin mirar el código**:

1. ¿Qué cambia para la persona que usa el sistema, o para el proyecto?
2. ¿Qué pasaría si este cambio tuviera un error?
3. ¿Se lo podrías contar a un colega en una frase?

Si alguna respuesta es «no sé», **pregunta antes de responder**. La sección existe precisamente para ese momento.

## Ejemplos

| ❌ No sirve | Por qué | ✅ Sirve |
|---|---|---|
| «Lo entiendo» u «ok» | No dice qué cambia | «Ahora el técnico ve sus turnos de la semana.» |
| «Actualiza dependencias» | Repite el título | «Sube Django a una versión que arregla un fallo de seguridad.» |
| «Arregla el bug» | No dice cuál | «El ticket ya no se cierra si faltan los materiales.» |

Puede ser corta, informal y con faltas. Lo importante es que diga **qué cambia** y que estés de acuerdo con ella. La IA te da 3 ejemplos: puedes elegir uno, ajustarlo o escribirla con tus propias palabras.

## Cómo pedir la explicación

- «Explícamelo en 5 líneas, como a alguien que no programa.»
- «Dame un ejemplo: antes pasaba esto, ahora pasa esto otro.»
- «¿Es grave o puedo estar tranquilo? Dame una conclusión y tu recomendación.»
- «¿Qué pasa si no lo integro?»

## Qué debe hacer la IA

- **Explicar primero y preguntar después**, una sola vez por PR, con un ejemplo y una conclusión clara («tranquilo porque…» o «esto sí preocupa porque…, recomiendo…»).
- Pegar tu respuesta **tal cual**, sin corregir faltas. Si dictas, transcribir sin cambiar la idea.
- Después de explicar, darte **3 ejemplos** de respuesta, con enfoques distintos y todos fieles al cambio (y otros 3 para «Si sale mal, ¿qué pasaría?», cuando aplica). Eliges uno, lo ajustas o escribes la tuya: las tres cosas valen. Si eliges uno, la IA lo pega tal cual.
- Si la respuesta no dice qué cambia, preguntar de otra forma, sin regañar. Si parece de otro PR, avisar una vez.
- **Si un push cambia lo que hace el PR**, aunque el riesgo no suba, volver a explicar y preguntar.
- Si se equivocó en una explicación, **decirlo y corregirlo**.

## Límites conocidos

- El CI no puede probar que la respuesta la escribiste tú: solo rechaza lo vacío, el texto de plantilla y una palabra suelta de aprobación («ok», «listo», «lo entiendo»…). Comprobar quién editó la descripción por última vez queda para una versión futura.
- En un repo privado del plan gratuito, un CI en rojo no impide integrar: integra solo con el CI en verde.

## Si el CI falla

Lee el mensaje: dice qué falta. Por ejemplo, *«Falta decir qué cambia; con pocas palabras basta. No importa la redacción ni la ortografía.»* Edita la descripción del PR y guarda; el control se vuelve a ejecutar solo. Si lo que falta es un informe o el riesgo, pídele a quien hizo el cambio que lo complete: los informes no los escribes tú.

Fuente: regla R12 del [kernel](../KERNEL.md#las-16-reglas).

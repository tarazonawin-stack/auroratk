# Guía: «Lo entiendo» (R12)

> Español · [English](lo-entiendo.en.md)

Para quien aprueba los cambios y no programa a diario. Se lee en 3 minutos.

## Qué es

Cada PR tiene una sección **«Lo entiendo»**. Ahí escribes, **en una línea y con tus palabras, qué cambia** cuando el PR entra. El CI no deja el PR en verde mientras esa línea esté vacía.

- **No es una firma ni un trámite.** Es tu prueba de que sabes qué estás aceptando.
- **No tienes que entender cada línea de código.** Basta con entender **qué cambia y a quién afecta**. Que el código funcione lo comprueban el CI y la revisión independiente.

## Por qué existe

La IA escribe rápido y se equivoca con seguridad. Si apruebas sin entender, pierdes justo la habilidad de notar cuándo algo está mal. **Avanzar lento con claridad vale más que avanzar rápido con dudas.**

## ¿Ya lo entiendo? Prueba rápida

Lo entiendes si puedes responder estas preguntas **sin mirar el código**:

1. ¿Qué cambia para la persona que usa el sistema, o para el proyecto?
2. ¿Qué pasaría si este cambio tuviera un error?
3. ¿Se lo podrías contar a un colega en una frase?

Si alguna respuesta es «no sé», **no escribas la línea todavía: pregunta.** No es un fracaso. La regla existe precisamente para ese momento.

## Ejemplos

| ❌ No sirve | Por qué | ✅ Sirve |
|---|---|---|
| «Lo entiendo» | Es el nombre de la sección, no dice qué cambia | «Ahora el técnico ve sus turnos de la semana.» |
| «OK, aprobado» | Es una firma, no una explicación | «Los PR no se integran si no escribo esta línea.» |
| «Actualiza dependencias» | Repite el título | «Sube Django a una versión que corrige un fallo de seguridad.» |
| «Arregla el bug» | No dice cuál | «El ticket ya no se cierra si faltan los materiales.» |

Puede ser corta e informal. Lo importante es que sea **tuya** y diga **qué cambia**. Si la IA te da un ejemplo, no lo copies: dilo a tu manera.

## Cómo pedir la explicación

Si no lo entiendes, pídeselo a la IA o a quien hizo el cambio. Estas preguntas funcionan:

- «Explícamelo en 5 líneas, como a alguien que no programa.»
- «Dame un ejemplo concreto: antes pasaba esto, ahora pasa esto otro.»
- «¿Es grave o puedo estar tranquilo? Dame una conclusión clara y tu recomendación.»
- «¿Qué tengo que decidir yo, y qué opciones tengo?»
- «¿Qué pasa si no lo integro?»

## Qué debe hacer la IA

- Explicar **con ejemplos y con una conclusión clara**: «puedes estar tranquilo porque…» o «esto sí preocupa porque…, recomiendo…». No dejar a la persona con dudas.
- Si se equivocó en una explicación anterior, **decirlo y corregirlo**.
- **Nunca escribir la línea por el dueño** ni presionar para avanzar. Si el dueño le dicta su frase, la pega **tal cual**.
- Puede dar **un ejemplo** para mostrar qué se pide, pero el dueño **escribe su propia frase o cambia el ejemplo a sus palabras**. Si responde «usa esa», la IA le pide que la diga a su manera: copiar el ejemplo no prueba que lo entendió.
- Si el dueño escribe solo «Lo entiendo», explicarle con calma que falta decir **qué** cambia.

## Si el CI falla

El control dice: *«Write in one line, in your own words, what this change does ('Lo entiendo')»*. Edita la descripción del PR, escribe tu línea debajo del título «Lo entiendo» y guarda. El control se vuelve a ejecutar solo, sin repetir el resto del CI.

Fuente: regla R12 del [kernel](../KERNEL.md#las-15-reglas).

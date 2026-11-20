## Informe para el dueño · Owner's report (R12)
**Riesgo · Risk:** <1, 2 o 3. El CI calcula el mínimo; se puede subir, nunca bajar · 1, 2 or 3; CI computes the minimum>
<Riesgo 1: nada más que hacer aquí · Risk 1: nothing else here. Riesgo 2 y 3: sin tecnicismos; todo lo que pueda cambiar tu decisión (riesgos, lo que no se deshace, datos de personas, costos) va aquí, no abajo.>

- **Qué cambia · What changes:** <con un ejemplo: antes pasaba esto, ahora pasa esto · with a before/after example>
- **Qué puede salir mal · What can go wrong:** <…>
- **Cómo se deshace · How to undo:** <cómo se deshace · lo que un Revert no deshace · what a Revert does not undo>
- **Recomendación · Recommendation:** <y qué pasa si no se integra · and what happens if it is not merged>

## Con tus palabras: ¿qué cambia con este PR? · In your own words: what does this PR change? (R12)
<Riesgo 2 y 3. Unas pocas palabras tuyas, escritas o dictadas; no importan la redacción ni la ortografía · A few words of your own, typed or dictated; wording and spelling don't matter.>
Si sale mal, ¿qué pasaría?: <solo riesgo 3 · risk 3 only>

---
> **Para la revisión técnica: no necesitas leerlo** · *For the technical review: you don't need to read this*

## Resumen técnico · Technical summary
<Una idea por PR, en 3 a 5 líneas · One idea per PR, 3–5 lines.> **Spec:** SPEC-<NNN> | `trivial` · **Criterios · Criteria:** AC-01, AC-02

## Informe técnico · Technical report (R12)
<Honesto y preciso, sin secretos ni datos personales (R05, R09) · Honest and precise, no secrets or personal data.>

- **Cambios · Changes:** <qué archivos cambian y por qué · which files change and why>
- **Verificado · Verified:** <comandos y su salida real, con enlace a la ejecución del CI · commands and real output, with a link to the CI run>
- **No verificado · Not verified:** <lo que no se comprobó y por qué, o «nada» · or "nothing">
- **Limitaciones · Limitations:** <deuda o casos no cubiertos, o «ninguna conocida» · or "none known">

## Lista del kernel · Kernel checklist
> Marca cada casilla, o escribe N/A al lado y márcala. El CI falla si queda alguna sin marcar, si falta el riesgo o es menor que el calculado, o si falta algo que pide ese riesgo. Haz merge solo con el CI en verde (R12).
> *Check every box, or write N/A next to it and check it. CI fails on an unchecked box, a missing or too-low risk, or anything that risk requires. Merge only with green CI (R12).*

- [ ] R01 Enlaza su spec (con cómo se podría abusar), es `trivial`, o tiene objetivo / fuera de alcance / cómo se prueba (nivel Ligero)
- [ ] R02 Una sola idea; ≤ 400 líneas; ningún archivo pasa de 400
- [ ] R03 Cada criterio tiene una prueba que verifica el resultado; los arreglos traen una prueba que fallaba antes
- [ ] R07 Dependencias nuevas: nombre exacto comprobado en el registro oficial, mantenida y aprobada; o ninguna
- [ ] R08 Migraciones reversibles y listas sin consultas N+1, o N/A
- [ ] R09 Sin datos reales de personas; datos personales nuevos justificados en la spec y cubiertos por el perfil de país
- [ ] R10 Probado con teclado y en celular, o N/A
- [ ] R11 Textos nuevos en ES y EN, o N/A
- [ ] R14 Las acciones críticas nuevas dejan registro, sin datos personales, o N/A
- [ ] R15 Estados de carga, vacío y error; flujo principal validado con una persona usuaria real (Estándar, desde la etapa 3), o N/A
- [ ] R12 `AGENTS.md`, `docs/decisiones/` y `docs/ESTADO.md` al día
- [ ] R12 Revisado por una sesión distinta a la que escribió el código (en Estricto y riesgo 3, otro modelo o herramienta): <cuál · which>, en el commit <SHA>; volvió a ejecutar lo «Verificado» y confirma en el PR que el informe técnico es fiel
- [ ] R13 Sin permisos nuevos para agentes; sin skills ni plugins nuevos sin aprobar; `AGENTS.md` cerca de la meta de 150 líneas
- [ ] Excepciones nuevas registradas con fecha, o ninguna · *New exceptions recorded with a date, or none*

## Qué cambia · What changes
<Una idea por PR. Resumen en 3–5 líneas. · One idea per PR. 3–5 line summary.>

**Spec:** SPEC-<NNN> | `trivial` · **Criterios · Criteria:** AC-01, AC-02

## Lo entiendo · I understand it (R12)
<El humano escribe aquí, en una línea y con sus palabras, qué hace este cambio. Si no puede, pide la explicación antes de aprobar.>
<The human writes here, in one line and in their own words, what this change does. If they can't, they ask for an explanation before approving.>

## Evidencia · Evidence (R12)
- Ejecución de CI · CI run: <enlace · link>

## Lista del kernel · Kernel checklist
> Marca cada casilla, o escribe N/A al lado y márcala. El CI falla si queda alguna sin marcar o si "Lo entiendo" está vacío. Haz merge solo con el CI en verde (R12).
> *Check every box, or write N/A next to it and check it. CI fails if any is left unchecked or "Lo entiendo" is empty. Merge only with green CI (R12).*

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
- [ ] R12 Revisado por una sesión distinta a la que escribió el código: <qué modelo o herramienta · which model or tool>
- [ ] R13 Sin permisos nuevos para agentes; sin skills ni plugins nuevos sin aprobar; `AGENTS.md` cerca de la meta de 150 líneas
- [ ] Excepciones nuevas registradas con fecha, o ninguna · *New exceptions recorded with a date, or none*

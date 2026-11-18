# Ejemplo de spec · Spec example

> Una spec mala y una buena para el mismo cambio. Datos inventados.
> *A bad and a good spec for the same change. Made-up data.*

## ❌ Mala · Bad

> "Agregar que el técnico pueda cerrar tickets y que se descuenten los materiales. Que sea seguro y rápido."

**Por qué falla · Why it fails:** no dice quién puede cerrar, qué pasa si se cierra dos veces, qué queda fuera ni cómo se prueba. "Seguro y rápido" no se puede comprobar. La IA rellenará los huecos a su manera.

## ✅ Buena · Good

# Spec · Cierre de ticket con descuento de materiales

- **ID:** SPEC-007 · **Fecha:** 2026-11-18 · **Estado:** aprobada · **Responsable:** <nombre>

## Objetivo
Que el técnico asignado cierre un ticket de avería registrando los materiales usados, y que el inventario se descuente solo, para que el supervisor vea el stock real sin cuadrarlo a mano.

## Fuera de alcance
- Reabrir tickets cerrados (va en SPEC-008).
- Reportes de consumo por mes.

## Criterios de aceptación
- **AC-01:** Dado un ticket abierto asignado a mí, cuando lo cierro con 30 m de fibra, entonces el ticket queda "cerrado" y el stock de fibra baja 30 m.
- **AC-02:** Dado un ticket ya cerrado, cuando alguien intenta cerrarlo otra vez, entonces se rechaza y el stock no cambia (acción idempotente, R08).
- **AC-03:** Dado un técnico que **no** tiene asignado el ticket, cuando intenta cerrarlo, entonces recibe "No tienes permiso para cerrar este ticket" y nada cambia (R06).
- **AC-04:** Dado un material sin stock suficiente, cuando cierro el ticket, entonces se rechaza con un mensaje que dice qué material falta y cuánto hay.

## Abuso
- **¿Cómo se podría abusar?** Un técnico podría cerrar tickets ajenos o inflar materiales para sacar stock. **Lo impide:** permiso validado en el servidor (AC-03) y registro de quién cerró y qué consumió (R14).

## Datos y permisos
- **Datos que toca:** ticket (estado), inventario (cantidad), registro de consumo.
- **Datos personales:** nombre del técnico que cierra (ya existe en el sistema; R09).
- **Quién puede:** el técnico asignado y el supervisor. **Quién no:** cualquier otro técnico.
- **Qué queda registrado:** cierre, quién, cuándo y materiales (R14).

## Personas
- **Estados:** botón "Cerrando…" mientras guarda; mensaje de error que dice qué hacer.
- **Validación:** un técnico de planta externa prueba el flujo en su celular antes de darlo por terminado (R15).
- **Accesibilidad:** cerrar con teclado; usable a 360 px.
- **Textos nuevos en ES y EN:** sí.

## Riesgos y preguntas abiertas
- ¿Se permite cerrar con stock negativo en emergencias? → pendiente de decidir con el supervisor.

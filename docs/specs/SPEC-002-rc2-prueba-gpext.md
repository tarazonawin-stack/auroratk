# Spec · 4.0.0-rc.2: arreglos de la prueba en GPEXT · fixes from the GPEXT trial

- **ID:** SPEC-002 · **Fecha · Date:** 2026-11-26 · **Estado · Status:** aprobada · approved (el dueño respondió «a» · *the owner answered "a"*)
- **Responsable · Owner:** Jose Alejandro Tarazona

## Objetivo · Goal
La prueba de `v4.0.0-rc.1` en GPEXT (PR #106 y #107 de GPEXT) encontró errores del kernel: adoptarlo rompía sus propias reglas. Se corrigen sin agregar reglas nuevas. Política de congelación (DEC-001): cada arreglo es un error probado en un proyecto real y trae una prueba que falla antes.
*The rc.1 trial in GPEXT found kernel bugs: adopting it broke its own rules. Fixed with no new rules, each with a failing test first.*

## Fuera de alcance · Out of scope
- Las reglas propias de GPEXT (`**/*_forms.py`, `type:ignore`): van en el `.github/riesgo.txt` de GPEXT. · *GPEXT's own risk lines stay in GPEXT.*
- Subir el nivel de GPEXT: lo decide el dueño en esa sesión. · *GPEXT's level is the owner's call there.*

## Criterios de aceptación · Acceptance criteria
- **AC-01 (R02):** `size_check.py` no cuenta los archivos de la copia del kernel (`docs/kernel/**` y los destinos fijos de `kernel_sync.py`): esa copia la vigila `check` byte a byte. Una prueba exige que las dos listas sean iguales. · *The size check skips the kernel copy; a test keeps both lists equal.*
- **AC-02 (R04, R03):** `pyproject-django.toml` deja fuera de `ruff`, `mypy` y la cobertura a los archivos del kernel copiados: se prueban en el kernel, no en el proyecto. Así no hace falta una excepción como EXC-008. · *Kernel files are excluded from the project's lint, types and coverage.*
- **AC-03 (R02):** si `scripts/size_hook.py` no existe (una rama de antes de adoptar), el *hook* no frena: no hace nada. `check` ya exige el script. · *A missing hook script is a no-op, not a block.*
- **AC-04 (R12):** en una prueba, quitar más líneas con `assert` de las que se agregan es riesgo 3, como quitar funciones de prueba. · *Removing asserts from a test is risk 3.*
- **AC-05 (R12):** `.github/riesgo.txt` acepta `quitar <texto>`: quitar una línea de código que lo contenga es riesgo 3 (GPEXT: `quitar scoped(`). · *Projects can mark removals of their own guards as risk 3.*

## Abuso · Abuse (R01)
- **Esconder código en una ruta del kernel para que no cuente en el tamaño:** esas rutas deben ser byte a byte las del kernel o `check` falla; el CI lo corre en cada PR. · *Hiding code under a kernel path fails `check`.*
- **Bajar un riesgo con el archivo del proyecto:** `.github/riesgo.txt` solo puede agregar casos de riesgo 3, nunca quitar; cambiarlo es riesgo 3. · *The risk file can only add risk-3 cases.*

## Datos y permisos · Data and permissions
- **Datos personales · Personal data:** ninguno · *none*.

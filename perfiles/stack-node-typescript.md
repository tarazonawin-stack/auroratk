# Perfil · Profile: Node / TypeScript (Express, React…)

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | ESLint (`complexity`, `max-lines`) | `npx eslint .` |
| R03 Pruebas · Tests | Vitest (o Jest) + cobertura | `npx vitest run --coverage` |
| R04 Estricto · Strict | `tsc --strict` + ESLint (typescript-eslint) + Prettier; prohibido `any` explícito y `catch` vacío | `npx tsc --noEmit && npx eslint . && npx prettier --check .` |
| R06 Seguridad · Security | Librería de autenticación mantenida, validación con esquemas (p. ej. Zod), Helmet en Express · *Maintained auth library, schema validation (e.g. Zod), Helmet on Express* | `semgrep` + pruebas de permisos por rol |
| R07 Dependencias · Dependencies | `package-lock.json` + `npm audit` | `npm ci && npm audit --audit-level=high` |
| R08 Datos · Data | ORM con migraciones (Prisma o Drizzle) | Migrar adelante y atrás en una base temporal · *Migrate up and down on a temp DB* |
| R10 Accesibilidad · Accessibility | Playwright + `@axe-core/playwright` | Ver · See [tipo-web](tipo-web.md) |
| R11 Idiomas · Languages | `i18next` o `Intl` nativo · *or native `Intl`* | Prueba de paridad de claves ES/EN · *ES/EN key parity test* |

**Notas · Notes**
- ESLint: `@typescript-eslint/no-explicit-any`, `no-empty`, `@typescript-eslint/no-floating-promises` en `error`.

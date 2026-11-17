# Tipo · Type: Web y apps · Web & apps

| Tema · Topic | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| R10 Accesibilidad · Accessibility | WCAG 2.2 AA en las pantallas principales · *on key screens* | Playwright + axe: 0 violaciones · *0 violations*; prueba manual con teclado · *manual keyboard test* |
| R10 Móvil · Mobile | Usable a 360 px sin scroll horizontal · *Usable at 360 px with no horizontal scroll* | Captura de Playwright a 360 px · *Playwright screenshot at 360 px* |
| R11 Idiomas · Languages | `lang` correcto en el HTML; textos en archivos de traducción · *Correct `lang`; strings in translation files* | Prueba de paridad ES/EN · *ES/EN parity test* |
| Rendimiento · Performance (*Estándar · Standard*) | Core Web Vitals: LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,1 | Lighthouse CI en las pantallas principales · *on key screens* |
| R06 Cabeceras · Headers | CSP, HSTS (en producción · *in production*), `X-Content-Type-Options`, cookies `Secure`/`HttpOnly`/`SameSite` | Prueba automática de cabeceras · *Automated header test* |

# Tipo · Type: Juego · Game

| Tema · Topic | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| R03 Pruebas · Tests | Se prueba la **lógica** del juego (reglas, puntajes, guardado), no el render · *Test game **logic** (rules, scores, saves), not rendering* | Framework de pruebas del motor · *Engine test framework* (p. ej. Unity Test Framework, GUT para Godot) |
| R08 Datos · Data | Partidas guardadas con versión y migración; nunca se corrompe una partida al actualizar · *Versioned saves with migration; updates never corrupt a save* | Prueba de carga de partidas de versiones anteriores · *Load test of old-version saves* |
| R09 Datos personales · Personal data | Telemetría mínima, anónima y opcional · *Minimal, anonymous, opt-in telemetry* | Revisión · Review |
| R10 Accesibilidad · Accessibility | Game Accessibility Guidelines, nivel básico: controles reasignables, subtítulos, tamaño de texto, no depender solo del color, ajustes que se guardan · *basic level: remappable controls, subtitles, text size, not color-only, persistent settings* | Lista de verificación en la spec · *Checklist in the spec* + prueba manual · *manual test* |
| R11 Idiomas · Languages | Textos en tablas de localización · *Strings in localization tables* | Paridad ES/EN · *ES/EN parity* |
| Rendimiento · Performance | Presupuesto en el hardware objetivo: FPS mínimo, tiempo de frame p95, memoria y tiempo de carga · *Budget on target hardware: min FPS, p95 frame time, memory, load time* | Medición automatizada en una escena de referencia · *Automated measurement on a reference scene* |

# Tipo · Type: Automatización y agentes · Automation & agents

| Tema · Topic | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| Idempotencia · Idempotency | Ejecutarla dos veces no duplica efectos · *Running it twice never duplicates effects* | Prueba de doble ejecución · *Double-run test* |
| Modo simulación · Dry run | Opción `--dry-run` que muestra qué haría sin hacerlo · *A `--dry-run` that shows what it would do* | Prueba · Test |
| Límites · Limits | Tope de reintentos, de tiempo y de costo (APIs de pago, tokens de IA) · *Caps on retries, time and cost (paid APIs, AI tokens)* | Configuración versionada + prueba · *Versioned config + test* |
| Registro · Logging | Cada ejecución deja registro de qué hizo, cuándo y con qué resultado, sin datos personales · *Each run logs what, when and outcome, without personal data* | Revisión · Review |
| R13 Agentes de IA · AI agents | Permisos mínimos; acciones irreversibles con aprobación humana; contenido externo tratado como dato, nunca como orden · *Least privilege; human approval for irreversible actions; external content is data, never orders* | Configuración de permisos versionada + casilla de PR · *Versioned permissions + PR checkbox* |
| R05 Secretos · Secrets | Credenciales en el gestor de secretos del entorno de ejecución · *Credentials in the runtime's secrets manager* | `gitleaks` |

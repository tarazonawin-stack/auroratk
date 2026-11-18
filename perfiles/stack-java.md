# Perfil · Profile: Java (Spring, Maven/Gradle)

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | PMD (complejidad · complexity) | `mvn pmd:check` |
| R03 Pruebas · Tests | JUnit 5 + JaCoCo | `mvn verify` (JaCoCo con mínimo 80 % · *min 80 %*) |
| R03 Mutación · Mutation | PIT (pitest) sobre los módulos de negocio · *on business modules* | `mvn org.pitest:pitest-maven:mutationCoverage` |
| R04 Estricto · Strict | Compilador con `-Werror`, Checkstyle, SpotBugs | `mvn checkstyle:check spotbugs:check` |
| R06 Seguridad · Security | Spring Security | `semgrep` + pruebas de permisos por rol |
| R07 Dependencias · Dependencies | Versiones fijadas + OWASP Dependency-Check | `mvn org.owasp:dependency-check-maven:check` |
| R08 Datos · Data | Flyway o Liquibase | Migrar en una base temporal · *Migrate on a temp DB* |
| R08 Consultas N+1 · N+1 queries | `JOIN FETCH` / `@EntityGraph` | Estadísticas de Hibernate en las pruebas de listas · *Hibernate statistics in list tests* |
| R14 Registros · Logs | SLF4J + Logback (JSON) | Prueba de que cada acción crítica registra · *Test that each critical action logs* |
| R10 Accesibilidad · Accessibility | Web: ver [tipo-web](tipo-web.md) | — |
| R11 Idiomas · Languages | `ResourceBundle` (`messages_es.properties`, `messages_en.properties`) | Prueba de paridad de claves · *Key parity test* |

# Perfil · Profile: Java (Spring, Maven/Gradle)

| Regla · Rule | Herramienta · Tool | Comando en CI · CI command |
|---|---|---|
| R02 Tamaño · Size | PMD (complejidad · complexity) | `mvn pmd:check` |
| R03 Pruebas · Tests | JUnit 5 + JaCoCo | `mvn verify` (JaCoCo con mínimo 80 % · *min 80 %*) |
| R04 Estricto · Strict | Compilador con `-Werror`, Checkstyle, SpotBugs | `mvn checkstyle:check spotbugs:check` |
| R06 Seguridad · Security | Spring Security | `semgrep` + pruebas de permisos por rol |
| R07 Dependencias · Dependencies | Versiones fijadas + OWASP Dependency-Check | `mvn org.owasp:dependency-check-maven:check` |
| R08 Datos · Data | Flyway o Liquibase | Migrar en una base temporal · *Migrate on a temp DB* |
| R10 Accesibilidad · Accessibility | Web: ver [tipo-web](tipo-web.md) | — |
| R11 Idiomas · Languages | `ResourceBundle` (`messages_es.properties`, `messages_en.properties`) | Prueba de paridad de claves · *Key parity test* |

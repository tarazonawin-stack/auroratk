# Tipo · Type: Público u open source · Public or open source

Se suma al perfil de tipo del proyecto (web, juego, librería…) cuando el repositorio es público o se publica con licencia abierta. No cambia las 15 reglas: dice cómo se cumplen en público.
*Added on top of the project's type profile (web, game, library…) when the repository is public or released under an open license. It does not change the 15 rules: it says how they are met in public.*

> **Revisado · Reviewed:** 2026-11-18 · **Revisar de nuevo · Review again:** cada 12 meses o cuando salga una versión nueva del Baseline · *every 12 months or when a new Baseline version is released*
> **Fuente · Source:** [OpenSSF OSPS Baseline 2026.08.28](https://baseline.openssf.org/versions/2026-08-28)

> ⚠️ **Licencia del kernel · Kernel license.** La [LICENSE](../LICENSE) de AuroraTK es de **uso interno**. No copies `KERNEL.md`, `KERNEL-CHAT.md`, perfiles ni plantillas a un repo público: enlázalos o resume las reglas con tus palabras en el `CONTRIBUTING.md` del proyecto, o pide permiso escrito al autor. Tu propio código sí puede llevar la licencia abierta que elijas.
> **Plantillas y scripts (`plantillas/`, `perfiles/ci/*.py`):** en un repo público, escríbelos de nuevo con tus palabras o espera a que el autor los libere con licencia abierta (p. ej. MIT). Si quien publica es el propio autor, puede incluirlos, pero esas copias deben llevar una licencia abierta y la decisión se anota en `docs/decisiones/` (R12).
> *AuroraTK's LICENSE is **internal use**. Do not copy `KERNEL.md`, `KERNEL-CHAT.md`, profiles or templates into a public repo: link to them or summarize the rules in your own words in the project's `CONTRIBUTING.md`, or ask the author for written permission. Your own code may carry any open license you choose.*
> *Templates and scripts: in a public repo, rewrite them in your own words or wait until the author releases them under an open license (e.g. MIT). The author may include them, but those copies must carry an open license, recorded in `docs/decisiones/` (R12).*

## 1. OSPS Baseline nivel 1 · Level 1 (24 controles · *controls*)

Obligatorio en todos los niveles del kernel. "Al publicar una versión" = desde el primer release o tag. · *Mandatory at every kernel level. "On release" = from the first release or tag.*

**Acceso · Access (AC)**
- [ ] **AC-01.01** MFA (verificación en dos pasos) obligatoria para quien tenga permisos de escritura o de administración · *MFA required for anyone with write or admin access* — cada persona lo activa en Settings → Password and authentication; para **exigirlo** a otros hace falta una organización (Organization → Settings → Authentication security) · *each person enables it in their own settings; **requiring** it of others needs an organization*
- [ ] **AC-02.01** Colaboradores nuevos con el mínimo permiso; ninguno recibe permisos automáticamente · *New collaborators get least privilege; no automatic grants* — revisar Settings → Collaborators
- [ ] **AC-03.01** Nadie puede hacer push directo a la rama principal · *No direct pushes to the primary branch* — protección de rama o ruleset · *branch protection or ruleset*
- [ ] **AC-03.02** No se puede borrar la rama principal sin confirmación explícita · *The primary branch cannot be deleted without explicit confirmation* — mismo ruleset con "Restrict deletions" · *same ruleset*

**Construcción y publicación · Build & release (BR)**
- [ ] **BR-01.01** El CI valida y limpia los datos no confiables (títulos de PR, nombres de rama, comentarios) antes de usarlos · *CI sanitizes untrusted metadata (PR titles, branch names, comments) before use* — nunca `${{ github.event.* }}` directo en `run:` · *never inline in `run:`*; pásalo por `env:`
- [ ] **BR-01.03** El código de un PR externo no accede a secretos ni a credenciales con privilegios · *Untrusted PR code cannot reach privileged secrets or credentials* — ver sección 3 · *see section 3*
- [ ] **BR-03.01** La web, el repo y los canales oficiales solo por canales cifrados (HTTPS o SSH) · *Website, repo and official channels over encrypted channels only (HTTPS or SSH)*
- [ ] **BR-03.02** Las descargas oficiales salen de canales autenticados (GitHub Releases, registro oficial) · *Official downloads come from authenticated channels (GitHub Releases, official registry)*
- [ ] **BR-07.01** Ningún secreto sin cifrar en el repositorio (R05) · *No unencrypted secret in the repository* — `gitleaks` + `.gitignore` con `.env`

**Documentación · Documentation (DO)** — al publicar una versión · *on release*
- [ ] **DO-01.01** Guía de uso de las funciones básicas (el README sirve) · *User guide for basic functionality (README is enough)*
- [ ] **DO-02.01** Cómo reportar errores · *How to report defects* — sección en `CONTRIBUTING.md` + plantilla de issue · *issue template*

**Gobierno · Governance (GV)**
- [ ] **GV-02.01** Un canal público para discutir cambios y dudas · *A public channel to discuss changes and questions* — Issues o Discussions activados · *enabled*
- [ ] **GV-03.01** El proceso de contribución explicado · *Contribution process explained* — `CONTRIBUTING.md`

**Licencia · Legal (LE)**
- [ ] **LE-02.01** Licencia del código aprobada por OSI o FSF · *Source license approved by OSI or FSF*
- [ ] **LE-02.02** Lo que se publica (paquetes, binarios) tiene licencia aprobada por OSI o FSF · *Released assets licensed under OSI- or FSF-approved terms*
- [ ] **LE-03.01** La licencia está en `LICENSE`, `COPYING` o `LICENSES/` del repositorio · *License kept in `LICENSE`, `COPYING` or `LICENSES/`*
- [ ] **LE-03.02** Cada versión publicada incluye su licencia · *Each release ships with its license*

**Calidad · Quality (QA)**
- [ ] **QA-01.01** Repositorio legible por cualquiera en una URL fija · *Repository publicly readable at a static URL*
- [ ] **QA-01.02** Historial público de cambios: qué, quién y cuándo (sin reescribir la rama principal) · *Public change history: what, who, when (no rewriting the primary branch)*
- [ ] **QA-02.01** Si el lenguaje tiene gestor de paquetes, lista de dependencias directas (`requirements.txt`, `package.json`, `pom.xml`…) · *If the language has a package manager, a direct dependency list*
- [ ] **QA-04.01** Si hay varios repositorios, el README los lista · *If there are several repositories, the README lists them* (o N/A · *or N/A*)
- [ ] **QA-05.01** Sin ejecutables generados en el repositorio (`.exe`, `.jar`, `dist/`) · *No generated executables in the repository*
- [ ] **QA-05.02** Sin binarios que no se puedan revisar · *No unreviewable binaries* — no se admiten aunque se documenten; las imágenes, el audio y similares no cuentan como binarios a revisar · *not allowed even if documented; images, audio and similar media are excluded*

**Vulnerabilidades · Vulnerability management (VM)**
- [ ] **VM-02.01** Contacto de seguridad publicado · *Security contact published* — `SECURITY.md`

## 2. Archivos de gobierno · Governance files

| Archivo · File | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| `LICENSE` | Licencia aprobada por OSI ([lista](https://opensource.org/licenses)); para código, MIT o Apache-2.0 son simples. Elegirla y escribirla en `docs/decisiones/` (R12) · *OSI-approved license; MIT or Apache-2.0 are simple for code. Record the choice* | GitHub detecta la licencia en la portada · *GitHub shows the license*; Scorecard `License` |
| `CONTRIBUTING.md` | Cómo proponer cambios, reportar errores y qué exige el CI (resumen propio de las reglas del kernel, sin copiarlo) · *How to propose changes, report bugs and what CI requires (own summary of kernel rules, not a copy)* | Existe y lo enlaza el README · *Exists and is linked from README* |
| `CODE_OF_CONDUCT.md` | Contributor Covenant 2.1 con un correo real de contacto · *with a real contact email* | Existe; el correo responde · *Exists; the email works* |
| `SECURITY.md` | Cómo reportar en privado (GitHub *Private vulnerability reporting*), plazo de respuesta, versiones con soporte · *Private reporting, response time, supported versions* | Settings → Advanced Security → Private vulnerability reporting activado · *enabled* |
| `GOVERNANCE.md` o · *or* `MAINTAINERS.md` | Quién decide y quién integra; con una sola persona basta `MAINTAINERS.md` con un nombre y un contacto · *Who decides and merges; a solo project only needs `MAINTAINERS.md` with one name and contact* | Existe · *Exists* |
| DCO o · *or* CLA | **DCO** (recomendado, gratis): cada commit lleva `Signed-off-by:` (`git commit -s`). CLA solo si piensas cambiar de licencia o venderla, y requiere abogado · *DCO recommended (free); CLA only if you plan to relicense, needs a lawyer* | App comunitaria DCO o DCO2 (no es de GitHub) instalada en el repo · *Community DCO or DCO2 app (not made by GitHub) installed on the repo* |

## 3. Qué cambia al ser público · What changes when public

| Tema · Topic | Exigencia · Requirement | Cómo se mide · How it is measured |
|---|---|---|
| R12 Gobierno · Governance | La protección de rama es gratis en repos públicos: R12 se cumple **por máquina**. Ruleset en la rama principal: PR obligatorio, CI en verde obligatorio, sin push directo ni borrado · *Branch protection is free on public repos: R12 becomes **machine-enforced**. Ruleset: PR required, green CI required, no direct push or deletion* | Settings → Rules; un push directo de prueba es rechazado · *a test direct push is rejected* |
| CI gratis · Free CI | GitHub Actions es gratis en repos públicos con los runners estándar: todos los chequeos del perfil de stack corren en cada PR. El límite de gasto de R13 sigue para runners pagados y para la IA · *Actions is free on public repos with standard runners; R13 spending cap still applies to paid runners and AI* | Pestaña Actions · *Actions tab* |
| R05 Secretos · Secrets (más crítico · *more critical*) | El historial es público y se copia en minutos: un secreto subido **una vez** está filtrado aunque se borre. Se revoca y se cambia de inmediato; borrar el commit no basta. Antes de publicar un repo privado, revisar **todo** el historial · *A secret pushed **once** is leaked even if deleted: revoke and rotate at once. Scan the **whole** history before making a private repo public* | `gitleaks detect` sobre todo el historial · *over full history*; *Secret scanning* y *Push protection* activados · *enabled* |
| CI seguro · Safe CI (PRs de desconocidos · *from strangers*) | Los PRs externos se prueban con `pull_request` (sin secretos, token de solo lectura). **No** usar `pull_request_target` ni `workflow_run` para ejecutar código del PR: corren con secretos y permisos de escritura. Desde el 2026-12-02 GitHub bloquea `pull_request_target` por defecto en repos públicos salvo que una política de eventos de Actions lo permita: no lo reactives. `permissions: contents: read` por defecto; acciones fijadas por SHA; en Settings → Actions → General, exigir aprobación manual para **todos** los que contribuyen por primera vez (por defecto solo aplica a cuentas nuevas de GitHub) · *Test external PRs with `pull_request`. **Never** run PR code under `pull_request_target` or `workflow_run`. Default read-only permissions; pin actions by SHA; require approval for **all** first-time contributors (the default only covers new GitHub accounts). Since 2026-12-02 GitHub blocks `pull_request_target` by default in public repos unless an Actions event policy allows it: do not re-enable it* | Revisión de `.github/workflows/`; Scorecard `Dangerous-Workflow`, `Token-Permissions`, `Pinned-Dependencies` |
| OpenSSF Scorecard (*Estándar · Standard*) | `ossf/scorecard-action` semanal y en la rama principal; nota ≥ 7 en Estándar, ≥ 8 en Estricto; cada chequeo bajo 5 se arregla o se registra en `EXCEPCIONES.md` · *Weekly and on the primary branch; score ≥ 7 Standard, ≥ 8 Strict; each check below 5 fixed or recorded as an exception* | Resultado del workflow y pestaña Security · *Workflow result and Security tab* |
| R09 Datos · Data | Ningún dato real de personas en issues, pruebas ni capturas: lo ve todo el mundo · *No real personal data in issues, tests or screenshots: everyone can see it* | Revisión del PR · *PR review* |

# AuroraTK Kernel

> English · [Español](README.md)

**A personal, universal, bilingual quality standard for building software with AI, where nothing is declared "done" without evidence.**

## Mission

AI writes fast, but it is wrong with full confidence. This kernel exists so that **every project starts with clear rules, machine evidence and a human who decides**, regardless of language, kind of software, or which AI is used.

## What it is and isn't

| It is | It isn't |
|---|---|
| 16 checkable rules, each with its reason and official source. | An application or a service. |
| Profiles that map the rules to tools per language and project type. | A certification or an audit. |
| Templates ready to copy into every new project. | A replacement for experienced professionals. |
| AI-agnostic: works with Claude, other AIs, or people. | Something that forces you to use paid tools. |

## What to expect

- **Projects that start right:** each one begins with its spec, tests, CI and limits from the first commit.
- **Fewer surprises:** passwords in code, silenced errors, giant files or duplicated data are caught by a machine before they get in.
- **An AI that behaves the same in every session,** because the rules and the project map are written in the repo, not in anyone's memory.
- **Judging without being an expert:** green CI plus independent review means you have evidence; otherwise you know exactly what is missing.
- **If you use an app built with the kernel:** it works with a keyboard and on a 360 px phone, comes in Spanish with English ready, every screen shows when it is loading, empty or failing (with messages that say what to do), and your personal data is kept for a written purpose and period.
- **What not to expect:** zero bugs. The kernel reduces errors and makes them visible; it does not eliminate them. It is also not a certification, an audit or a legal review.

## Who it is for: the three levels

Each project declares its level in its `AGENTS.md`. When the software starts being used with external clients or companies, it moves up to Strict.

| Level | What for | Examples |
|---|---|---|
| **Light** | Experiments and personal tools, with nobody else's data. | A script, a prototype, an exercise. |
| **Standard** | Software other people use, including employee data for internal use. | An internal app, a published game, a library. |
| **Strict** | Sensitive data (health, identity documents, finances), external clients or users, or money. | Production with clients, payments. |

## The 16 rules in plain words

The detail (what each requires, how it is checked, why, and its source) is in [KERNEL.en.md](KERNEL.en.md).

| ID | Rule | What it means |
|---|---|---|
| R01 | Spec before code | Every change starts from a note with a goal, limits and how it could be abused. |
| R02 | Small and readable | One change is one idea: up to 400 lines of code and 200 of documentation; files warn at 300. |
| R03 | Tests that really test | Every criterion has a test that checks the result, not just that it "didn't fail". |
| R04 | No hidden errors | Swallowing an error is forbidden: it is handled, logged or shown. |
| R05 | Zero secrets in the repo | Keys and passwords only in environment variables. No exceptions. |
| R06 | Security with proven parts | Login, permissions and encryption from mature libraries; permissions checked on the server. |
| R07 | Dependencies under control | A new library is verified in the official registry and approved by a human. |
| R08 | Reliable data | Migrations, nothing deleted without confirmation, backups proven by restoring. |
| R09 | Personal data with care | Only the minimum, with a legal basis, people's rights and a country profile. |
| R10 | Accessible | Usable with a keyboard and on a 360 px phone (WCAG 2.2 AA). |
| R11 | Bilingual | No interface text hard-coded; Spanish base, English ready. |
| R12 | Whoever builds does not approve | Green CI, independent review and your merge; depending on the change's risk, you say in your own words what changes. Everything written down and reversible. |
| R13 | AI with limits | Short instructions for the AI, least-privilege permissions and a spending cap. |
| R14 | Logs that alert | Errors and critical actions are logged, without personal data, and a serious error raises an alert. |
| R15 | Clear for the people who use it | Loading, empty and error states on every screen, and a real person validates the main flow. |
| R16 | Deploy without fear and roll back | CI releases with your approval, a check runs after deploying, and going back to the previous version is tested. |

## How to use it in a new project

1. **Pick the level:** Light, Standard or Strict (see [KERNEL.en.md](KERNEL.en.md#levels)).
2. **Pick your profiles** in [`perfiles/`](perfiles/): one stack, one type, and one per country where you will have users.
3. **Copy the kernel with one command** (`perfiles/ci/kernel_sync.py sync`): it writes `docs/kernel/`, the scripts, the R12 workflow, the skills and any missing templates, with the version pinned in `.github/kernel.txt`. CI runs `check` so nobody edits the copy. Steps, what can be customized and how to migrate from your own process: [Adopting guide](guias/adoptar.en.md).
4. **Set up CI in stages** with your profiles' commands (see *Staged activation* in the kernel) and turn on main-branch protection if your GitHub plan allows it (a free private repo does not: merge only with green CI).
5. **Work like this, every time:** spec → small change with its test → CI → independent review → depending on the risk, you say in your own words what changes → your approval → `docs/ESTADO.md` up to date. Unsure about «Con tus palabras» (in your own words)? Read the [guide](guias/lo-entiendo.en.md). Several AI sessions at once? Read [The office](guias/oficina.en.md).

**No repository?** In a chat such as Google AI Studio, paste [`KERNEL-CHAT.en.md`](KERNEL-CHAT.en.md) into the system instructions.

## FAQ

- **Do I need to know how to program?** You do not need to be an expert, but you do need to understand enough to say in your own words what changes in risk 2 and 3 changes (routine ones ask nothing of you). The AI explains the reason behind each decision.
- **What is CI?** An automatic checker that runs on every change and blocks it if anything fails.
- **What if a rule does not fit?** It can be broken only with a written exception in `docs/excepciones.md`, with reason, risk, owner and expiry date. R05 and the core of R06 allow no exceptions.
- **Which country does it cover?** The first country profile is Peru (Law 29733 and its 2024 Regulation). For another country, its profile is created before production.

## Layout

```
KERNEL.md / KERNEL.en.md     the standard (16 rules, levels, exceptions, versions)
KERNEL-CHAT.md / .en.md      short version to paste into a chat with no repository
perfiles/                    rules → tools per stack, project type and country
plantillas/                  files to copy into each project
ejemplos/                    examples of what done right looks like
guias/                       guides: Adopting, «Con tus palabras» (for approvers) and «La oficina» (parallel sessions)
plantillas/roles/            per-role instructions: analyst, coordinator, specialist, reviewer and progress
tests/                       tests of the CI scripts and of the kernel's consistency
SHA256SUMS                   checksums of the files copied into docs/kernel/
CHANGELOG.md                 kernel version history
LICENSE, LICENSES/, REUSE.toml  licenses by kind of file (CC BY 4.0, MIT, MIT-0)
CITATION.cff, CONTRIBUTING.md   how to cite it and how to contribute
```

## Status

**Version 4.0.0.** Released 2026-11-26 (tag `v4.0.0`) after a trial in GPEXT: the `v4.0.0-rc.1` trial tag found four kernel bugs, fixed with tests before release (SPEC-002). Frozen: patches only with a test that fails first, minors only with new profiles, a major only for a real product problem (see *Kernel versions*). Rules, profiles and templates are complete. Ready-to-copy CI configurations are added per profile the first time each one is used in a real project (first up: GPEXT, with Python/Django + web).

## Publishing a version

1. Check that the change fits the freeze policy (DEC-001). Record the change in `CHANGELOG.md` and bump the version in every file, `CITATION.cff` included (the tests warn if one is missing).
2. Regenerate the checksums: `sha256sum KERNEL.md KERNEL.en.md perfiles/*.md > SHA256SUMS`.
3. Verify: `python3 -m unittest discover -s tests -v` (the same as CI).
4. After merging and trying it in a real project (with a trial tag `vX.Y.Z-rc.N`), create the tag **`vX.Y.Z`, with no dot after the v** (for example `v4.0.0`): the kernel links point to that exact name.
5. **A published tag is never moved or deleted:** projects pin it in `.github/kernel.txt`. A later fix is a new version (`v4.0.1`), with a test that fails first (DEC-001). `v4.0.0` was recreated once, minutes after it was created and before any project used it; that is not repeated.

## Authorship and license

© 2026 Jose Alejandro Tarazona.

- **Text of the standard** (kernel, profiles, guides and docs): [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Use and adapt it with credit: "Based on AuroraTK Kernel, © 2026 Jose Alejandro Tarazona, CC BY 4.0".
- **CI scripts and tests:** [MIT](LICENSES/MIT.txt).
- **Templates and examples:** [MIT-0](LICENSES/MIT-0.txt), copy them without keeping any notice.

Per-path detail in [`REUSE.toml`](REUSE.toml); summary in [LICENSE](LICENSE). To cite it: [`CITATION.cff`](CITATION.cff). Want to contribute? Read [CONTRIBUTING.md](CONTRIBUTING.md).

# AuroraTK Kernel

> English · [Español](README.md)

**A personal, universal, bilingual quality standard for building software with AI, where nothing is declared "done" without evidence.**

## Mission

AI writes fast, but it is wrong with full confidence. This kernel exists so that **every project starts with clear rules, machine evidence and a human who decides**, regardless of language, kind of software, or which AI is used.

## What it is and isn't

| It is | It isn't |
|---|---|
| 15 checkable rules, each with its reason and official source. | An application or a service. |
| Profiles that map the rules to tools per language and project type. | A certification or an audit. |
| Templates ready to copy into every new project. | A replacement for experienced professionals. |
| AI-agnostic: works with Claude, other AIs, or people. | Something that forces you to use paid tools. |

## What to expect

- **Projects that start right:** each one begins with its spec, tests, CI and limits from the first commit.
- **Fewer surprises:** passwords in code, silenced errors, giant files or duplicated data are caught by a machine before they get in.
- **An AI that behaves the same in every session,** because the rules and the project map are written in the repo, not in anyone's memory.
- **Judging without being an expert:** green CI plus independent review means you have evidence; otherwise you know exactly what is missing.
- **What not to expect:** zero bugs. The kernel reduces errors and makes them visible; it does not eliminate them.

## How to use it in a new project

1. **Pick the level:** Light, Standard or Strict (see [KERNEL.en.md](KERNEL.en.md#levels)).
2. **Pick your profiles** in [`perfiles/`](perfiles/): one stack, one type, and one per country where you will have users.
3. **Copy the templates** into the project:
   - `plantillas/AGENTS.md` → `AGENTS.md` (root), then fill it in.
   - `plantillas/CLAUDE.md` → `CLAUDE.md` (root).
   - `plantillas/PULL_REQUEST_TEMPLATE.md` → `.github/PULL_REQUEST_TEMPLATE.md`.
   - `KERNEL.md`, `KERNEL.en.md` and `SHA256SUMS` → `docs/kernel/`, and the chosen profiles → `docs/kernel/perfiles/`, so the AI can see them. Copy them unedited: the profile's CI compares each file with `SHA256SUMS` and fails if any changed.
   - `plantillas/dependabot.yml` → `.github/dependabot.yml`.
   - `plantillas/ESTADO.md` → `docs/ESTADO.md`.
   - `plantillas/claude-settings.json` → `.claude/settings.json` (least-privilege agent permissions, R13).
   - Your profile's CI, if any (e.g. `perfiles/ci/python-django.yml` → `.github/workflows/ci.yml`, and the scripts in `perfiles/ci/` → `scripts/`).
   - Create `docs/specs/`, `docs/decisiones/` and `docs/excepciones.md` (from `plantillas/EXCEPCIONES.md`).
4. **Set up CI in stages** with your profiles' commands (see *Staged activation* in the kernel) and turn on main-branch protection if your GitHub plan allows it (a free private repo does not: merge only with green CI).
5. **Work like this, every time:** spec → small change with its test → CI → independent review → you write one line on what it does → your approval → `docs/ESTADO.md` up to date.

**No repository?** In a chat such as Google AI Studio, paste [`KERNEL-CHAT.en.md`](KERNEL-CHAT.en.md) into the system instructions.

## Layout

```
KERNEL.md / KERNEL.en.md     the standard (15 rules, levels, exceptions, versions)
KERNEL-CHAT.md / .en.md      short version to paste into a chat with no repository
perfiles/                    rules → tools per stack, project type and country
plantillas/                  files to copy into each project
ejemplos/                    examples of what done right looks like
tests/                       tests of the CI scripts and of the kernel's consistency
SHA256SUMS                   checksums of the files copied into docs/kernel/
CHANGELOG.md                 kernel version history
```

## Status

**Version 2.1.0.** Rules, profiles and templates are complete. Ready-to-copy CI configurations are added per profile the first time each one is used in a real project (first up: GPEXT, with Python/Django + web).

## Publishing a version

1. Record the change in `CHANGELOG.md` and bump the version in every file (the tests warn if one is missing).
2. Regenerate the checksums: `sha256sum KERNEL.md KERNEL.en.md perfiles/*.md > SHA256SUMS`.
3. Verify: `python3 -m unittest discover -s tests -v` (the same as CI).
4. After merging, create the tag **`vX.Y.Z`, with no dot after the v** (for example `v2.1.0`): the kernel links point to that exact name.

## Authorship and license

© 2026 Jose Alejandro Tarazona. Internal use. See [LICENSE](LICENSE).

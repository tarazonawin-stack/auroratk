# AuroraTK Kernel

> English · [Español](README.md)

**A personal, universal, bilingual quality standard for building software with AI, where nothing is declared "done" without evidence.**

## Mission

AI writes fast, but it is wrong with full confidence. This kernel exists so that **every project starts with clear rules, machine evidence and a human who decides**, regardless of language, kind of software, or which AI is used.

## What it is and isn't

| It is | It isn't |
|---|---|
| 13 checkable rules, each with its reason and official source. | An application or a service. |
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
2. **Pick two profiles:** one stack and one type, in [`perfiles/`](perfiles/).
3. **Copy the templates** into the project:
   - `plantillas/AGENTS.md` → `AGENTS.md` (root), then fill it in.
   - `plantillas/CLAUDE.md` → `CLAUDE.md` (root).
   - `plantillas/PULL_REQUEST_TEMPLATE.md` → `.github/PULL_REQUEST_TEMPLATE.md`.
   - `KERNEL.md` → `docs/kernel/KERNEL.md`.
   - Create `docs/specs/`, `docs/decisiones/` and `docs/excepciones.md` (from `plantillas/EXCEPCIONES.md`).
4. **Set up CI** with your profiles' commands and turn on main-branch protection.
5. **Work like this, every time:** spec → small change with its test → CI → independent review → your approval.

## Layout

```
KERNEL.md / KERNEL.en.md     the standard (13 rules, levels, exceptions, versions)
perfiles/                    rules → tools per stack and project type
plantillas/                  files to copy into each project
CHANGELOG.md                 kernel version history
```

## Status

**Version 1.0.0.** Rules, profiles and templates are complete. Ready-to-copy CI configurations are added per profile the first time each one is used in a real project (first up: GPEXT, with Python/Django + web).

## Authorship and license

© 2026 Jose Alejandro Tarazona. Internal use. See [LICENSE](LICENSE).

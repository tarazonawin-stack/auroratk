# The office: several AI sessions in parallel

> English · [Español](oficina.md)
> A working guide. It changes no rule: it shows how to follow them when several AI sessions work at once, each with its own specialty.

## When it pays off

Working in parallel **saves wall-clock time but costs more tokens**: every session pays for its own context. It pays off when several independent features are ready to build and the project has its spending cap written down (R13). It does not pay off in a project that is just starting, or when tasks touch the same files.

## The roles

| Role | What it does | How many |
|---|---|---|
| **Analyst** | Interviews the owner, writes the vision and the specs with their criteria (R01), proposes level and profiles | 1, at the start of each phase |
| **Coordinator** | Splits the work, writes the agreements between parts, assigns tasks, decides the merge order. **The only one who edits `docs/ESTADO.md` and `AGENTS.md`** | 1, always |
| **Specialist** | Builds one task in its own branch and PR (R02, R03) | 2 or 3 at a time |
| **Reviewer** | Reviews the PRs, ideally with another model (R12) | 1 per group of PRs |
| **Progress** | Every so often, summarizes for the owner what was done, what is next and what is blocked | 1 scheduled task |

Each role has a template in [`plantillas/roles/`](../plantillas/roles/), pasted as the instruction when the session opens.

## How to split the work

- **By complete feature** (vertical slice): each specialist builds one feature end to end (screen, logic, data and tests). The default: specialists barely overlap.
- **By layer** (frontend, backend, database) only if the project is already split that way, e.g. a web app talking to an API, and the API contract is written first.
- **Documentation goes inside each PR**, not in a separate documenter: R12 requires `AGENTS.md`, decisions and state to reflect the change in the same PR.

## The five office rules

1. **Agreements first, then parallel work.** The coordinator merges a short spec or decision with what is shared (models, URLs, permissions, API contract). Only then do specialists start.
2. **Separate files.** Each task declares which folders it touches; if two overlap, they go one after the other.
3. **One owner of migrations** per round, or a fixed order to create them (R08).
4. **Few at a time:** 2 or 3 specialists and a cap on open PRs (e.g. 5). More multiplies cost and conflicts.
5. **One writer** of `docs/ESTADO.md` and `AGENTS.md`: the coordinator.

## The flow

1. **Analyst:** interviews the owner (template `analista.md`) and leaves the vision and specs. The owner confirms.
2. **Coordinator:** merges the agreements and hands out tasks, each with goal, criteria, allowed folders, line cap and spending cap.
3. **Specialists:** work in parallel; each opens its PR with the kernel's PR template.
4. **Reviewer:** reviews by group; at risk 3, always.
5. **Coordinator:** merges in the decided order, updates `docs/ESTADO.md` and opens the next round.
6. **Progress:** a periodic plain-language report to the owner.

## Tools

- **Claude Code in the cloud:** the coordinator can create other sessions with their task and branch; subagents can work in an isolated copy of the repository; progress is a scheduled task.
- **Any other AI or a chat:** open one conversation per role and paste its template.

## What it does not do

It does not replace the owner: they decide the vision, the order and what gets merged (R12). If the office does not save time compared with working in sequence, go back to a single session: measure sessions, PRs and conflicts per feature.

# The office: several AI sessions in parallel

> English · [Español](oficina.md)
> A working guide. It changes no rule: it shows how to follow them when several AI sessions work at once, each with its own specialty.

## When it pays off

Working in parallel **saves wall-clock time but costs more tokens**: every session pays for its own context. It pays off when several independent features are ready to build and the project has its spending cap written down (R13). It does not pay off in a project that is just starting, or when tasks touch the same files.

## The roles

| Role | What it does | How many |
|---|---|---|
| **Analyst** | Interviews the owner, writes the vision and the specs with their criteria (R01), proposes level and profiles | 1, at the start of each phase |
| **Coordinator** | Splits the work, writes the agreements between parts, assigns tasks and proposes the merge order. **The only one who edits `docs/ESTADO.md` and `AGENTS.md`**, inside each specialist's PR before merge (R12) | 1, always |
| **Specialist** | Builds one task in its own branch and PR (R02, R03) | 2 or 3 at a time |
| **Reviewer** | Reviews each PR per R12, ideally with another model; may review a group, noting each PR's commit | 1 per group of PRs |
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
5. **One writer** of `docs/ESTADO.md` and `AGENTS.md`: the coordinator, who pushes those changes to the specialist's PR branch before merge, so they land in the same PR (R12).

## The flow

1. **Analyst:** interviews the owner (template `analista.md`) and leaves the vision and specs. The owner confirms.
2. **Coordinator:** merges the agreements and hands out tasks, each with goal, criteria, allowed folders, line cap and spending cap.
3. **Specialists:** work in parallel; each opens its PR with the kernel's PR template.
4. **Reviewer:** reviews each PR per R12 (at Standard, all of them; a written project exception may adjust it).
5. **Coordinator:** completes `docs/ESTADO.md` and `AGENTS.md` in each PR and proposes the order; **the owner merges** (R12), unless a written exception delegates it. Then opens the next round.
6. **Progress:** a periodic plain-language report to the owner.

## Tools

- **Claude Code in the cloud:** the coordinator can create other sessions with their task and branch; subagents can work in an isolated copy of the repository; progress is a scheduled task.
- **Any other AI or a chat:** open one conversation per role and paste its template.
- **Permissions (R13):** every session or subagent uses the project's permissions (`.claude/settings.json`, template `plantillas/claude-settings.json`) and never more than the coordinator; each task has its spending cap.

## Short, cheap chats

Every message pays for the whole chat again, and a session waiting for a permission makes no progress. Seen in GPEXT:

1. **Fixed permissions for routine work:** read-only commands and tests are allowed in `.claude/settings.json` (approved by the owner, R13), so no session sits blocked waiting for a click.
2. **Tasks in files:** each task lives in `docs/tareas/<name>.md` and the message that opens the session only says "read and do `docs/tareas/<name>.md`". It is deleted in the PR that completes it.
3. **Monitor with little text:** the coordinator or launcher checks each session's short status, never its full history.
4. **Model per task:** a fast, cheap one to launch and monitor, a mid one to code what already has a spec, the most capable one for specs and critical reviews.
5. **Close when done:** when the task ends, or the chat grows long, the session leaves what is pending in `docs/ESTADO.md` and is archived; the next one reads only that and its task.
6. **Questions together:** the owner's decisions go in a single numbered list at the end, with 2–3 options and the recommended one first; meanwhile work goes on with the recommended one, marked "to be confirmed", and the owner answers with numbers.

## What it does not do

It does not replace the owner: they decide the vision, the order and what gets merged (R12). If the office does not save time compared with working in sequence, go back to a single session: measure sessions, PRs and conflicts per feature.

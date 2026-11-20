# Guide: "In your own words" (R12)

> [Español](lo-entiendo.md) · English · Formerly called «Lo entiendo» ("I understand it").

For whoever approves changes and doesn't code every day. A 3-minute read.

## What it is

Risk 2 and 3 PRs have a section **«Con tus palabras: ¿qué cambia con este PR?»** ("In your own words: what does this PR change?"). There you say, in a few words of your own, typed or dictated, **what changes** when the PR is merged.

- **It is for you:** it helps you notice when something doesn't add up before merging. It is not a test or a signature.
- **You don't need to understand every line of code.** Understanding **what changes and who it affects** is enough. CI and the review by another session check that the code works.

## How much is on you: the risk says

| Risk | Example | What you do |
|---|---|---|
| **1 · routine** | Updating `docs/ESTADO.md` | Nothing |
| **2 · normal** | A new screen | Read the report (at the top, no jargon) and say in a few words what changes |
| **3 · critical** | Touching permissions, CI or dependencies | The same, plus "If it goes wrong, what would happen?". If unclear, don't merge yet: waiting breaks nothing |

**CI computes the risk** from the files the PR touches. The AI may raise it, never lower it. Don't mix them up: `trivial` means the change needs no spec; the **risk** says how much you need to look.

## Four promises

1. **Spelling doesn't matter.** Nobody corrects or grades your wording or spelling.
2. **What could change your decision is at the top**, in your part of the PR: risks, what can't be undone, personal data, costs. What's below ("For the technical review") you don't need to read.
3. **If the AI's explanation was wrong, the mistake belongs to the AI and the review, not to you.** It is recorded under "Frequent AI mistakes here".
4. **Undoing never asks you to write anything.**

## Do I know what changes? Quick test

You can answer **without looking at the code**:

1. What changes for the people who use the system, or for the project?
2. What would happen if this change had a bug?
3. Could you tell a colleague in one sentence?

If any answer is "I don't know", **ask before answering**. The section exists precisely for that moment.

## Examples

| ❌ Not enough | Why | ✅ Good |
|---|---|---|
| "I understand it" or "ok" | Doesn't say what changes | "Technicians now see their shifts for the week." |
| "Update dependencies" | Repeats the title | "Bumps Django to a version that fixes a security bug." |
| "Fix the bug" | Doesn't say which one | "A ticket can no longer be closed without its materials." |

It can be short, informal and misspelled. What matters is that it's **yours** and says **what changes**. If the AI gives you an example, don't copy it: say it your way.

## How to ask for an explanation

- "Explain it in 5 lines, as if I didn't code."
- "Give me an example: before, this happened; now, this happens."
- "Is this serious or can I relax? Give me a conclusion and your recommendation."
- "What happens if I don't merge it?"

## What the AI must do

- **Explain first and ask afterwards**, once per PR, with an example and a clear conclusion ("you can relax because…" or "this is a concern because…, I recommend…").
- Paste your answer **as is**, without fixing spelling. If you dictate, transcribe without changing the idea.
- It may offer **an example** of what is asked, but you say it your way. If you answer "use that one", it asks you to say it in your own words.
- If the answer doesn't say what changes, ask again in another way, without scolding. If it seems to belong to another PR, say so once.
- **If a push changes what the PR does**, even without raising the risk, explain and ask again.
- If it got an explanation wrong, **say so and correct it**.

## Known limits

- CI cannot prove that you wrote the answer: it only rejects empty text, template text and a lone approval word ("ok", "listo", "lo entiendo"…). At the Strict level, who last edited the description can also be checked.
- On a private repo on GitHub's free plan, a red CI does not block merging: merge only with green CI.

## If CI fails

Read the message: it says what is missing. For example, *«Falta decir qué cambia; con pocas palabras basta. No importa la redacción ni la ortografía.»* ("Say what changes; a few words are enough. Wording and spelling don't matter.") Edit the PR description and save; the check re-runs on its own. If a report or the risk is missing, ask whoever made the change to fill it in: you don't write the reports.

Source: rule R12 of the [kernel](../KERNEL.en.md#the-15-rules).

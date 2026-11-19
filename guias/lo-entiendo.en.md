# Guide: «Lo entiendo» / "I understand it" (R12)

> [Español](lo-entiendo.md) · English

For whoever approves changes and doesn't code every day. A 3-minute read.

## What it is

Every PR has a **«Lo entiendo» (I understand it)** section. There you write, **in one line and in your own words, what changes** when the PR is merged. CI keeps the PR red while that line is empty.

- **It is not a signature or a formality.** It is your proof that you know what you are accepting.
- **You don't need to understand every line of code.** Understanding **what changes and who it affects** is enough. CI and the independent review check that the code works.

## Why it exists

AI writes fast and is confidently wrong. If you approve without understanding, you lose exactly the skill of noticing when something is off. **Moving slowly with clarity beats moving fast with doubts.**

## Do I understand it? Quick test

You understand it if you can answer these **without looking at the code**:

1. What changes for the people who use the system, or for the project?
2. What would happen if this change had a bug?
3. Could you tell a colleague in one sentence?

If any answer is "I don't know", **don't write the line yet: ask.** That's not a failure. The rule exists precisely for that moment.

## Examples

| ❌ Not enough | Why | ✅ Good |
|---|---|---|
| "I understand it" | That's the section name; it doesn't say what changes | "Technicians now see their shifts for the week." |
| "OK, approved" | A signature, not an explanation | "PRs can't be merged unless I write this line." |
| "Update dependencies" | Repeats the title | "Bumps Django to a version that fixes a security bug." |
| "Fix the bug" | Doesn't say which one | "A ticket can no longer be closed without its materials." |

It can be short and informal. What matters is that it's **yours** and says **what changes**. If the AI gives you an example, don't copy it: say it your way.

## How to ask for an explanation

If you don't understand it, ask the AI or whoever made the change. These questions work:

- "Explain it in 5 lines, as if I didn't code."
- "Give me a concrete example: before, this happened; now, this happens."
- "Is this serious or can I relax? Give me a clear conclusion and your recommendation."
- "What do I need to decide, and what are my options?"
- "What happens if I don't merge it?"

## What the AI must do

- Explain **with examples and a clear conclusion**: "you can relax because…" or "this is a concern because…, I recommend…". Don't leave the person in doubt.
- If an earlier explanation was wrong, **say so and correct it**.
- **Never write the line for the owner** or push them to move faster. If the owner dictates their sentence, paste it **as is**.
- It may offer **an example** to show what is asked, but the owner **writes their own sentence or rewrites the example in their own words**. If they answer "use that one", the AI asks them to say it their way: copying the example doesn't prove they understood.
- If the owner writes only "I understand it", calmly explain that it still needs to say **what** changes.

## If CI fails

The check says: *"Write in one line, in your own words, what this change does ('Lo entiendo')"*. Edit the PR description, write your line under the «Lo entiendo» heading and save. The check re-runs on its own, without repeating the rest of CI.

Source: rule R12 of the [kernel](../KERNEL.en.md#the-15-rules).

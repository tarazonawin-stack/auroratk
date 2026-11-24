# Adopting the kernel

> [Español](adoptar.md) · English
> Working guide. A project uses the kernel as is: it copies a pinned version, customizes only where allowed, and lets CI watch the copy.

## How to adopt (new or existing project)

1. **Get the kernel at the version you will use**, outside your project:
   `git clone --depth 1 --branch v4.0.0 https://github.com/tarazonawin-stack/auroratk ../auroratk`
2. **Copy it into the project**, from the project folder:
   `python3 ../auroratk/perfiles/ci/kernel_sync.py sync --from ../auroratk --ci python-django`
   It writes `docs/kernel/`, `scripts/`, the R12 workflow, the skills and `.github/kernel.txt` with the version. Templates (`AGENTS.md`, `ci.yml`, `.claude/settings.json`…) are created only when missing.
3. **Fill in** `AGENTS.md` (level, profiles, countries and commands; 450-word cap) and merge `perfiles/ci/pyproject-django.toml` into your `pyproject.toml`.
4. **Check:** `python3 ../auroratk/perfiles/ci/kernel_sync.py check --from ../auroratk`. CI repeats it on every PR, using the kernel it fetches, not your copy.
5. **Turn on CI in stages** (`KERNEL_STAGE`) and branch protection if your plan allows it.
6. **Merge it all in one risk-3 PR**, with independent review.

**Trial before the final tag:** the owner creates a trial tag (`v4.0.0-rc.1`), you clone that tag and use `--ref v4.0.0-rc.1` in step 2. CI accepts tags only, not branches or commits.
**Already have `.claude/settings.json`?** `sync` leaves it alone; add the template's `hooks` block and `deny` rules by hand (`check` tells you what is missing). Nobody checks `.claude/settings.local.json`: don't use it to loosen rules.
**Stacked PRs:** the hook measures against `origin/main`. If a PR starts from another branch, declare its base: `git config branch.<branch>.kernelbase <base>`.

## What can be customized and what cannot

| The kernel's: not edited (`check` watches it) | The project's: customize it |
|---|---|
| `docs/kernel/**` (rules and profiles) | `AGENTS.md`, within the 450-word cap |
| Kernel `scripts/`: `risk.py`, `pr_check.py`, `pr_meta.py`, `size_check.py`, `size_hook.py`, `mutation_threshold.py`, `kernel_sync.py` | `.github/workflows/ci.yml`: **add** steps; the level's steps stay |
| `.github/workflows/pr-description.yml` (R12) | `.github/riesgo.txt`: only **add** risk-3 paths and words |
| Kernel skills in `.claude/skills/` | Your own skills, in other folders of `.claude/skills/` |
| The size hook and the `deny` rules in `.claude/settings.json` | `allow`, `ask` and extra `deny` rules in that same file |
| | Your own analysis rules (e.g. `.semgrep/`), tests, `docs/` |
| | Breaking a rule: only with a dated exception in `docs/excepciones.md` |

Something in the kernel doesn't fit? Don't change it in the project: open an issue on the kernel. If it is a bug with a failing test, it goes into a patch (DEC-001).

## Upgrading to another version

1. Read the new version's `CHANGELOG.md`.
2. Run `sync` again from the new kernel: it replaces the kernel's files and removes the ones that no longer exist in `docs/kernel/`.
3. Review template changes by hand, because `sync` doesn't touch yours.
4. Open a risk-3 PR. Upgrading is the owner's decision, never automatic.

## Migrating from a local process (the GPEXT case)

When a project invented its own process, each local piece is swapped for the kernel's. What the kernel doesn't cover stays as an allowed customization.

| Local piece | What to do |
|---|---|
| Green/yellow/red lanes (`scripts/lane.py`) | Remove: `risk.py`'s risk 1/2/3 does that job from the main branch |
| `scripts/check_size.py` (400 code + 200 docs) | Remove: `size_check.py` measures the same |
| Hook `.claude/hooks/size-after-commit.sh` | Remove: `size_hook.py` replaces it; add the template's `hooks` block to your `.claude/settings.json` |
| Long `AGENTS.md`, or short with detail in skills | Rebuild it from the template; your own skills stay |
| URL isolation test | Keep it, or start from `ejemplos/test_aislamiento_django.py` |
| Own semgrep rule (e.g. `scoped(...)`) | Keep it: the kernel doesn't cover it |
| Edited copy of `docs/kernel/` or `scripts/` | `sync` replaces it; the intended change goes to a kernel issue |

Recommended order: one PR that removes the duplicates and runs `sync`, and another for the customizations. Both are risk 3. Before the version tag is created, the project's CI must pass with the new kernel.

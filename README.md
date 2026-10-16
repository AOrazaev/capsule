# Capsule

A lightweight multi-repo task workspace convention for Copilot CLI. Each Capsule workspace has its own directory, independent Git worktrees, instructions, decision log, and local skills.

## Example layout

```text
~/code/
  repos/                         # permanent clones
    api/
    frontend/
  tasks/
    fix-auth/
      AGENTS.md                  # agent instructions
      CURRENT_TASK.md            # objective, scope, progress
      WORKLOG.md                 # decisions, blockers, approvals
      .github/skills/            # task-local skills
      src/
        api/                     # Git worktree
        frontend/                # Git worktree
```

## Create a Capsule workspace

```bash
python3 scripts/create_capsule.py fix-auth \
  --workspace-root ~/code/tasks \
  --repo api=~/code/repos/api \
  --repo frontend=~/code/repos/frontend \
  --base main
cd ~/code/tasks/fix-auth
copilot
```

`--base` defaults to `HEAD`; select a deliberate base for reproducibility. The script prompts before making changes; `--yes` bypasses the prompt. It creates worktrees under `<workspace>/src/<alias>` on `task/fix-auth` in each repository and fails safely if a branch already exists. Instructions and task notes stay at the workspace root; task-local skills go in `.github/skills/<name>/SKILL.md`.

## Load the bootstrap skill

The `create-capsule` bootstrap skill lives in `.github/skills/create-capsule/SKILL.md`. In Copilot CLI, use `/add-dir` with the **Capsule repository root**, not its `skills` directory. For example, for a checkout at `C:\src\capsule`:

```text
/add-dir C:\src\capsule
/skills
```

`/add-dir` grants file access and loads the added directory's `.github` skills and agents as trusted configuration. Check `/skills` for `create-capsule`. For a task worktree, add its actual repository root instead (for example, `C:\caps\fix-capsule\src\capsule`).

Keep the full repository accessible: this skill uses the accompanying `scripts/create_capsule.py` and `template/` directory. Copying only the skill directory does not provide those dependencies. Workspace-root instruction discovery is separate; verify that the installed CLI loads `AGENTS.md`, or provide it explicitly as context.

## Multi-repository coordination

For tasks spanning multiple repositories, the main agent should prefer one repository-scoped subagent per involved repository. Subagents handle repository-level investigation, implementation, and validation, returning concise outcomes and blockers rather than low-level transcripts. The main agent keeps responsibility for planning, dependencies, approvals, integration validation, and workspace notes. Independent repository tasks can run in parallel; dependent work is sequenced. Single-repository tasks may be handled directly.

## Hand off a Capsule workspace

The `capsule-handoff` skill lives in `.github/skills/capsule-handoff/SKILL.md`. Load the Capsule repository as described above, then ask the outgoing agent to "prepare a capsule handoff".

The skill writes an onboarding packet under the **task workspace root**, not the Capsule repository:

```text
docs/
  handoffs/
    handoff_YYYYMMDD/
      HANDOFF.md                 # read first: objective, decisions, next steps
      REPOSITORIES.md            # per-repo commits, dirty state, remaining work
      VALIDATION.md              # checks, environment, services, known failures
```

The outgoing agent updates `CURRENT_TASK.md` and `WORKLOG.md` and returns the packet path. Existing same-day packets are preserved; the agent asks before updating one or choosing a suffixed directory. No automatic commits or cleanup occur.

## Onboard to an existing Capsule workspace

The incoming counterpart is `.github/skills/capsule-onboard/SKILL.md`. Ask the next agent to "capsule onboard" and provide the packet's `HANDOFF.md` path. Without a path, it inspects `docs/handoffs` for the latest relevant packet and asks if the choice is ambiguous.

The skill reads workspace instructions, task notes, and the handoff, then reconciles repository commits, uncommitted changes, and relevant environment state. It preserves the historical packet, records discrepancies and a continuation plan in `CURRENT_TASK.md` and `WORKLOG.md`, and identifies pending approvals before work resumes. Ask to "onboard and resume" to continue implementation; onboarding alone stops after orientation.

## Decision policy

Routine coding decisions are logged when meaningful, without interrupting you. Architectural or contract changes require approval first. Unexpected changes made to get tests passing are not silently accepted. No automatic commits, pushes, cleanup, or skill promotion.

## Cleanup (manual)

After code is merged and only when you choose, from the source clone run `git worktree remove /path/to/tasks/fix-auth/src/api` for each repo. Delete the task branch only when no longer needed. Archive or delete the workspace notes separately. Do not delete worktree directories directly before detaching them through Git.

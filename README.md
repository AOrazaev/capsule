# Copilot CLI task workspaces

A lightweight multi-repo workspace convention. Each task has its own directory, independent Git worktrees, instructions, decision log, and local skills.

## Example layout

```text
~/code/
  repos/                         # permanent clones
    api/
    frontend/
  tasks/
    fix-auth/
      AGENTS.md                  # agent instructions
      TASK.md                    # objective, scope, progress
      WORKLOG.md                 # decisions, blockers, approvals
      .github/skills/            # task-local skills
      api/                       # Git worktree
      frontend/                  # Git worktree
```

## Create a workspace

```bash
python3 scripts/create_workspace.py fix-auth \
  --workspace-root ~/code/tasks \
  --repo api=~/code/repos/api \
  --repo frontend=~/code/repos/frontend \
  --base main
cd ~/code/tasks/fix-auth
copilot
```

`--base` defaults to `HEAD`; select a deliberate base for reproducibility. The script prompts before making changes; `--yes` bypasses the prompt. It creates `task/fix-auth` in each repository and fails safely if a branch already exists. Task-local skills go in `.github/skills/<name>/SKILL.md`.

## Install the bootstrap skill

Place `skills/create-task-workspace/` in a skills directory supported by your Copilot CLI installation, or provide the SKILL.md to Copilot as context. CLI skill discovery and root-level AGENTS.md behavior can vary by version: verify discovery with your installed version before relying on it. The skill references the accompanying script, so keep the full package accessible when installing it.

## Decision policy

Routine coding decisions are logged when meaningful, without interrupting you. Architectural or contract changes require approval first. Unexpected changes made to get tests passing are not silently accepted. No automatic commits, pushes, cleanup, or skill promotion.

## Cleanup (manual)

After code is merged and only when you choose, from the source clone run `git worktree remove /path/to/tasks/fix-auth/api` for each repo. Delete the task branch only when no longer needed. Archive or delete the workspace notes separately. Do not delete worktree directories directly before detaching them through Git.

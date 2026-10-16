---
name: create-capsule
description: Create a Capsule task workspace with isolated multi-repository Git worktrees, task instructions, a decision work log, and task-local Copilot skills.
---

# Create a Capsule workspace

When asked to create a Capsule workspace or bootstrap a task workspace:

1. Ask for a short task name, destination workspace parent directory, and which existing local Git clones should be included. Ask only for missing information. Each clone needs a short alias. Ask which base ref to use (default HEAD) and whether any repos require a different base; the bundled script supports one shared ref name, so use manual worktree commands for mixed bases.
2. Inspect each clone and its Git status. Confirm the intended base branch/ref; note that HEAD may be a feature branch. If there are uncommitted changes, explain that new worktrees will start from the selected commit and won't include those edits.
3. Show the user the proposed workspace path, worktree paths under `<workspace>/src/<alias>`, repository aliases, and new task branch names. Request confirmation before filesystem or Git changes.
4. Locate the package root three parent directories above this skill directory (`.github/skills/create-capsule/`); the bundled script is `<package-root>/scripts/create_capsule.py`. Run:

   `python3 scripts/create_capsule.py TASK --workspace-root /absolute/workspaces --repo api=/absolute/repos/api --repo web=/absolute/repos/web --base main --yes`

   Run from the package root or use an absolute path to the script. The script refuses existing destinations and branches, creates worktrees under `<workspace>/src/<alias>`, and initializes `AGENTS.md`, `CURRENT_TASK.md`, `WORKLOG.md`, and `.github/skills/` at the workspace root. When using manual commands for mixed bases, use the same `src/<alias>` layout.
5. Ask the user for the task objective and constraints; fill in CURRENT_TASK.md. Do not assume a goal beyond the user's description.
6. Explain how to `cd` into the workspace and launch `copilot`. Verify whether the installed Copilot CLI loads parent workspace instructions and skills from this layout. If not, explicitly pass the workspace `AGENTS.md` as context or configure the CLI's supported instruction mechanism. Do not claim automatic discovery without verification.
7. Never automatically delete a completed workspace, push branches, or promote a task-local skill. The user decides at completion.

## Shared and local skills

Create new skills in `<workspace>/.github/skills/<skill-name>/SKILL.md` with YAML frontmatter. Keep them local while evolving. Promote to a shared skill collection only after user approval; avoid copying over existing skills. Shared skills may be linked or referenced if supported by the installed Copilot CLI.

## Safety

Do not overwrite an existing task directory, reuse an occupied branch, or modify a repository's current checkout. Worktrees share Git object storage with their source clones; avoid deleting source clones while worktrees are attached. On partial failure, inspect worktrees and branches before retrying.

---
name: capsule-handoff
description: Prepare a Capsule handoff when an outgoing agent finishes or transfers work to another agent. Write onboarding Markdown under the workspace root's docs/handoffs/handoff_YYYYMMDD directory with current state, repository details, validation, and next steps.
---

# Capsule handoff

Use when asked for a "capsule handoff" or to prepare a Capsule workspace for the next agent. Create a durable, actionable onboarding packet, not a conversation transcript. Creating this skill is not itself a request to generate a handoff.

## Locate the workspace and destination

1. Identify the Capsule workspace root (`ROOT`) using the active task context, `AGENTS.md`, `CURRENT_TASK.md`, and its repository list. If working inside `src/<alias>`, locate the containing workspace. The repository containing this skill is not necessarily the workspace root. If the target is ambiguous, ask before writing.
2. Read the workspace instructions, current task, work log, and relevant task-local skills. Follow repository instructions when inspecting each worktree. Use the task's repository list rather than assuming every directory is a repository.
3. Use the current local date, formatted as eight digits `YYYYMMDD`, and create `ROOT\docs\handoffs\handoff_YYYYMMDD`. For example, on October 16, 2026, use `docs\handoffs\handoff_20261016`. Adapt path separators to the host OS.
4. If the destination already exists, do not overwrite it or silently merge packets. Ask whether to update that packet or create a separate suffixed directory such as `handoff_20261016_02`. Preserve existing material unless the user explicitly approves replacing it.

## Gather and reconcile state

- Update `CURRENT_TASK.md` with actual progress, remaining acceptance criteria, blockers, and pending user decisions. Append a concise handoff entry to `WORKLOG.md`; do not rewrite earlier decisions.
- For multi-repository work, prefer repository-scoped subagents for repository details and local verification. Have them return concise reports; the main agent owns the integrated packet and cross-repository dependencies.
- In each involved worktree, record its workspace-relative path, branch or detached HEAD, full HEAD commit, and staged, unstaged, and untracked files. Inspect relevant diffs to explain unfinished work, without changing or committing it. Use non-interactive Git commands such as `git status --short --branch`, `git rev-parse HEAD`, `git diff --stat`, and `git diff --cached --stat` from that repository.
- Distinguish verified observations from assumptions and historical reports. Record when evidence was collected. Do not rerun expensive suites solely for a handoff; record prior commands, results, and their tested commit or working-tree state when known. Mark stale or missing verification explicitly.
- Capture active agent work and task-owned processes that affect continuation: status, ownership, working directory, launch command, specific PID/session identifier when known, and readiness evidence. Do not assume they survive the outgoing session; give restart instructions and prerequisites. Do not stop or restart services just to prepare the packet.

## Write the onboarding packet

Create these Markdown files in the selected handoff directory. Fill them with task-specific information; explicitly mark unknown or inapplicable items rather than leaving placeholders.

### HANDOFF.md

The entry point for the incoming agent:

- Creation timestamp with timezone, resolved workspace root, and a short description of the handoff scope.
- Read order: workspace `AGENTS.md`, `CURRENT_TASK.md`, relevant `WORKLOG.md` entries, then this packet's `REPOSITORIES.md` and `VALIDATION.md`. Include working relative links to those files and any necessary local skills or design notes.
- User objective, constraints and non-goals, acceptance criteria, completed work, and outstanding work. Distinguish handing off from completing the task.
- Important decisions, approved versus proposed changes, rejected approaches and why they failed, unresolved questions, blockers, and known risks. Link to detailed evidence instead of duplicating the work log.
- An ordered continuation plan, including cross-repository dependencies, the first concrete action, required user approvals, and the conditions for considering the task complete.

### REPOSITORIES.md

For each involved repository:

- Alias, workspace-relative path, branch, HEAD commit, and source clone/base ref if known.
- Purpose in this task, changed files and behavior, relevant entry points, and repository-specific instructions.
- Committed work versus staged, unstaged, and untracked work; identify anything that must be preserved. A commit alone does not prove it was pushed; record push/PR state only when verified, otherwise mark it unknown.
- Remaining repository-local work, dependencies on other repositories, and any compatibility or integration concerns.

Keep the summary concise. Do not copy full diffs or source trees into the packet; the existing worktrees are the source of truth.

### VALIDATION.md

- Exact build, test, lint, and integration commands already used, their working directories, outcomes, and the tested revision/state and time if known. Clearly label not-run, failed, blocked, or potentially stale checks.
- Reproduction steps for unresolved failures, useful error summaries, and relevant non-sensitive evidence paths.
- Environment and tool prerequisites, configuration variable names without values, task-owned services and their lifecycle/restart details, and any required manual validation.
- The smallest remaining checks needed to verify the outstanding acceptance criteria, including cross-repository integration checks.

## Verify and deliver

1. Read back the documents. Check that files and links resolve, the packet matches the workspace notes and observed repository state, and the incoming agent has a concrete next action without relying on this conversation or ephemeral agent memory.
2. Do not claim success for missing evidence. Record incomplete collection or unresolved inconsistencies plainly. Never invent commits, approvals, test results, or process readiness.
3. Keep secrets, credentials, personal data, and sensitive logs out of the packet. Record configuration names and safe evidence locations instead of copying values.
4. Do not commit, push, open PRs, change branches, clean up worktrees, or discard edits as part of a handoff without explicit user instruction. The packet remains at the workspace root, outside the repository worktrees.
5. Record the packet path and any limitations in `CURRENT_TASK.md` and `WORKLOG.md`. Return its resolved path, point the next agent to `HANDOFF.md`, and state outstanding blockers or decisions briefly.

## Incoming counterpart

Use [capsule-onboard](../capsule-onboard/SKILL.md) to pick up a handoff. Give the incoming agent the selected packet's `HANDOFF.md` path; that skill handles reading, current-state reconciliation, and readiness to resume.

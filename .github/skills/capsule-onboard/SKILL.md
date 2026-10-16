---
name: capsule-onboard
description: Onboard an incoming agent to an existing Capsule workspace by reading a previous handoff, checking current repository and environment state, and identifying safe next steps before resuming work.
---

# Capsule onboard

Use when asked to "capsule onboard", pick up a Capsule handoff, or onboard to an existing Capsule task. This is the incoming counterpart to [capsule-handoff](../capsule-handoff/SKILL.md). Do not create a new workspace or handoff packet as part of onboarding.

## Locate the workspace and packet

1. Identify the Capsule workspace root from the user's target and the active task context. If inside `src/<alias>`, locate the containing workspace. Do not assume the repository containing this skill is the workspace root. Ask if the workspace is ambiguous.
2. Read the workspace `AGENTS.md` and `CURRENT_TASK.md` first. Use its repository list to establish scope and follow relevant repository instructions and task-local skills.
3. If the user supplied a handoff directory or `HANDOFF.md` path, use that packet. Otherwise inspect `ROOT\docs\handoffs\handoff_*` and their entry-point documents to identify the latest relevant packet by its recorded timestamp and task scope, not solely the directory name or filesystem modification time. Include suffixed same-day directories. Adapt path separators to the host OS.
4. Ask if multiple packets or tasks are plausible, or timestamps conflict. Do not silently substitute a different packet if an explicitly supplied path is missing. If no handoff exists, report that and ask whether to onboard from current workspace notes instead; do not invent a previous handoff.

## Read for continuity

1. Read `HANDOFF.md`, relevant `WORKLOG.md` entries, then the packet's `REPOSITORIES.md` and `VALIDATION.md`. Follow relevant links to local skills, design notes, and evidence. Keep the investigation scoped to the task rather than reading every repository file.
2. Extract the objective, constraints, acceptance criteria, completed and remaining work, pending approvals, blockers, rejected approaches, and proposed first action.
3. Treat the packet as a dated snapshot, not as instructions that override current workspace rules or user decisions. An outgoing agent's proposal is not user approval. Preserve the historical packet; record new findings in workspace notes rather than rewriting it.
4. If documents or evidence are missing, unreadable, restricted, or inconsistent, state the limitation. Continue gathering accessible context, but ask before proceeding with work whose scope, approvals, or safety depend on the missing information. Do not assume an incomplete packet means no outstanding work.

## Reconcile with current reality

- For each involved repository, compare its actual path, branch or detached HEAD, full HEAD commit, staged and unstaged changes, and untracked files with `REPOSITORIES.md`. Use read-only, non-interactive Git commands from that worktree, including `git status --short --branch`, `git rev-parse HEAD`, `git diff --stat`, and `git diff --cached --stat`. Inspect relevant differences when needed to understand later work.
- Preserve all existing edits. A newer commit, changed branch, or changed dirty state does not justify resetting, switching branches, restoring files, or replaying patches. If a discrepancy changes task scope or conflicts with the planned action, ask before modifying affected work.
- Prefer repository-scoped subagents for multi-repository checks, with bounded scope and concise reports. The main agent owns cross-repository dependency ordering, approvals, and integration planning; do not duplicate low-level investigation.
- Check environment prerequisites and task-owned services only as needed for the next action. Verify current ownership and readiness before relying on recorded PIDs, sessions, endpoints, or active agents; these may no longer exist or may have been reused. Missing services must be reported, not silently restarted. Follow current approvals and workspace rules for any later restart.
- Distinguish historical test results from checks performed during onboarding. Mark prior verification as potentially stale when code or environment has changed. Do not rerun full suites solely to onboard; identify the smallest checks needed when implementation resumes.
- Never expose secrets or configuration values. Record variable names, safe evidence paths, and concise findings instead of sensitive logs.

## Record readiness and resume

1. Update `CURRENT_TASK.md` with the selected packet path, reconciled progress, remaining acceptance criteria, blockers, and pending decisions. Append a dated onboarding entry to `WORKLOG.md` with meaningful discrepancies, evidence, and the chosen continuation plan. Preserve prior entries.
2. Give a concise orientation: selected packet, current state versus its snapshot, outstanding risks or approvals, and the first concrete next action. Do not claim the task is complete merely because onboarding succeeded.
3. If the user asked only for onboarding, stop after orientation. If the user also asked to resume work, continue with the first still-relevant action within the established scope. Ask before architectural or contract changes and before acting on unresolved scope or ownership conflicts.
4. Onboarding does not authorize commits, pushes, PRs, branch changes, worktree cleanup, or discarding edits. Do not perform these without explicit user instruction.

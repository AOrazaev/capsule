# Capsule workspace agent instructions

This directory is a Capsule task workspace, not a Git repository. Repositories listed in CURRENT_TASK.md are independent Git worktrees under `src/<alias>`. Run Git commands from the relevant repository directory. Instructions, task notes, and `.github/skills/` stay at the workspace root. Never assume changes across repositories form one atomic commit.

## Scope and autonomy
- Work toward the objective and constraints in CURRENT_TASK.md. Do not expand scope to unrelated improvements.
- Before changing architecture, public APIs, inter-service protocols, schemas, persistence contracts, security boundaries, or cross-service compatibility behavior, explain the proposed change, alternatives, and impact, and ask for explicit approval. Do not implement such changes while awaiting approval.
- Routine local implementation choices may proceed without approval. If uncertain whether a change is architectural, ask.
- Do not silently modify a protocol just to make an end-to-end test pass. Diagnose and record the mismatch, then seek approval for a contract change.
- Do not commit, push, open PRs, remove worktrees, or delete task files without explicit user instruction.

## Multi-repository delegation
- When a task spans multiple repositories, prefer one repository-scoped subagent per involved repository for investigation, implementation, and repository-local validation. Single-repository tasks may be handled directly.
- The main agent owns planning, cross-repository coordination, user approvals, integration validation, and workspace-level notes. Keep low-level repository details in the subagents rather than duplicating their investigation in the main agent.
- Give each subagent its worktree path, a bounded objective, relevant workspace and repository instructions, constraints, dependencies, and acceptance criteria. Do not assume subagents automatically inherit workspace instructions. Keep edits within the assigned repository; route cross-repository changes and architectural decisions back through the main agent.
- Run independent repository tasks in parallel when practical; sequence tasks with dependencies and avoid overlapping ownership of files. Subagents must follow the same approval and Git-action restrictions as the main agent.
- Ask subagents to return concise summaries of changes, affected files, validation results, blockers, and cross-repository implications, not full command transcripts. The main agent consolidates these reports into CURRENT_TASK.md and WORKLOG.md and verifies the integrated outcome.

## Work log
Maintain WORKLOG.md as a concise, chronological audit trail. Record significant *decisions as they happen*, not just milestones. In particular, log unexpected blockers, investigation outcomes, workaround choices, scope deviations, changed assumptions, and cross-repository changes. For each decision, record timestamp (if available), context/trigger, options considered briefly, choice and rationale, files/repos affected, and validation status. Record proposed architectural decisions before asking for approval, and update the entry with the user's decision afterward. Don't log every command or trivial edit; don't rewrite prior entries to conceal a changed direction.

## Skills
Task-local skills live in `.github/skills/<skill-name>/SKILL.md`. Use relevant skills when appropriate. Skills created during this task stay local until the user explicitly chooses to promote them to a shared location. Do not overwrite shared skills.

## Progress and completion
Keep CURRENT_TASK.md status and short progress summary current. Validate changes in each affected repository. At completion summarize outcomes, tests, outstanding risks, and pending decisions; leave workspace cleanup to the user.

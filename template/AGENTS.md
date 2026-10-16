# Task workspace agent instructions

This directory is a task workspace, not a Git repository. Child directories listed in TASK.md are independent Git worktrees. Run Git commands from the relevant child repository. Never assume changes across repositories form one atomic commit.

## Scope and autonomy
- Work toward the objective and constraints in TASK.md. Do not expand scope to unrelated improvements.
- Before changing architecture, public APIs, inter-service protocols, schemas, persistence contracts, security boundaries, or cross-service compatibility behavior, explain the proposed change, alternatives, and impact, and ask for explicit approval. Do not implement such changes while awaiting approval.
- Routine local implementation choices may proceed without approval. If uncertain whether a change is architectural, ask.
- Do not silently modify a protocol just to make an end-to-end test pass. Diagnose and record the mismatch, then seek approval for a contract change.
- Do not commit, push, open PRs, remove worktrees, or delete task files without explicit user instruction.

## Work log
Maintain WORKLOG.md as a concise, chronological audit trail. Record significant *decisions as they happen*, not just milestones. In particular, log unexpected blockers, investigation outcomes, workaround choices, scope deviations, changed assumptions, and cross-repository changes. For each decision, record timestamp (if available), context/trigger, options considered briefly, choice and rationale, files/repos affected, and validation status. Record proposed architectural decisions before asking for approval, and update the entry with the user's decision afterward. Don't log every command or trivial edit; don't rewrite prior entries to conceal a changed direction.

## Skills
Task-local skills live in `.github/skills/<skill-name>/SKILL.md`. Use relevant skills when appropriate. Skills created during this task stay local until the user explicitly chooses to promote them to a shared location. Do not overwrite shared skills.

## Progress and completion
Keep TASK.md status and short progress summary current. Validate changes in each affected repository. At completion summarize outcomes, tests, outstanding risks, and pending decisions; leave workspace cleanup to the user.

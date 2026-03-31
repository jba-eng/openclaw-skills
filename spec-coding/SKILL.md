---
name: Spec Coding
slug: spec-coding
version: 4.0.0
description: Execute ONE task from tasks.md. Read specs.md and design.md for context. Update task status. Exit. Designed for heartbeat-driven execution.
metadata: {"requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}
---

## When to Use

Execute one coding task from a project's tasks.md. Called by coding-agent heartbeat.

## Workflow (One Task Per Invocation)

### 1. Find Next Task

Scan tasks.md for first task with:
- `**Status:** planned` → execute
- `**Status:** failed` → retry once
- `**Status:** in-progress` → mark failed (shouldn't exist between runs)

If none found: exit with "No pending tasks"

### 2. Read Context (Minimal)

Only read what's needed:
- Task's done_when conditions
- Relevant sections from specs.md
- Relevant sections from design.md

Don't read entire files if not needed.

### 3. Execute Task

- Mark status: `in-progress`
- Implement code
- Validate done_when conditions
- Mark status: `done` or `failed`

### 4. Exit

Exit immediately. Next heartbeat will pick up next task.

## Context Management

### Minimize Context Bloat

- Read only relevant file sections
- Don't load entire specs.md if task is small
- Use file line ranges when possible
- Keep session focused on ONE task

### Continuation Between Heartbeats

Each heartbeat is independent:
- Reads tasks.md to find next pending task
- No state carried between heartbeats
- Progress tracked via task status in tasks.md
- If task fails, next heartbeat retries or skips

### Session Isolation

Each heartbeat creates new session:
- No context from previous heartbeat
- Fresh start each time
- Only tasks.md status persists

## Task Status Format

```markdown
### T1: Task Name
**Status:** planned
**Dependencies:** None
**Done When:**
1. Condition 1
2. Condition 2
```

Status values: `planned`, `in-progress`, `done`, `failed`

## File Locations

```
workspace/software-projects/{PROJECT}/
├── specs.md          ← Read for context
├── design.md         ← Read for context
├── tasks.md          ← Read and update status
├── src/              ← Create/modify
└── tests/            ← Create/modify
```

## Core Rules

1. ONE task per invocation
2. Minimize context - read only what's needed
3. Update tasks.md status before exiting
4. Never modify specs.md or design.md
5. Exit after one task - don't loop

## Related Skills

- **autocoder** - Orchestrates nightly execution
- **spec-creation** - Creates specifications

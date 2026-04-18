---
name: executing-plans
description: Use when running a multi-step implementation plan. Executes plans in batches with human review checkpoints between phases.
---

# Executing Plans

## Overview

Execute implementation plans in batches with review checkpoints. Each batch contains 2-5 related tasks. After each batch, show progress and wait for review before continuing.

## Process

1. **Read the plan** completely before starting
2. **Group tasks** into logical batches (2-5 tasks each)
3. **Execute batch 1** - complete all tasks in order
4. **Show progress** - what was done, test results, git status
5. **Wait for review** - user confirms before next batch
6. **Repeat** until plan complete

## Batch Execution

For each task in batch:
- Complete all steps in order
- Run tests after each step
- Commit after each task
- Track progress with todowrite

## Checkpoint Output

After each batch, show:

```markdown
## Batch N Complete

**Tasks completed:**
- [x] Task 1: Description
- [x] Task 2: Description

**Tests run:** [pass/fail]
**Commits:** [list commit SHAs]

**Next batch:** [task numbers]
```

Wait for user confirmation before proceeding.

## Error Handling

If a task fails:
1. Debug using systematic-debugging skill
2. Fix the issue
3. Re-run tests
4. Only continue after tests pass

Do NOT skip failing tests or rationalize why they're "not important."
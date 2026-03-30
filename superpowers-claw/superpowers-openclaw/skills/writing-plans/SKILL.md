---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code. Creates detailed implementation plans with exact file paths, code snippets, and verification steps.
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything: which files to touch, code, testing, how to test it.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Scope Check

If the spec covers multiple independent subsystems, break into separate plans—one per subsystem. Each plan should produce working, testable software.

## File Structure

Map which files will be created or modified and what each is responsible for.

- Design units with clear boundaries and well-defined interfaces
- Prefer smaller, focused files over large ones
- Files that change together should live together

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use subagent-driven-development or executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Spec Reference:** `docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.md`

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**id:** TASK-NNN
**dependencies:** [TASK-XXX, TASK-YYY] or []
**spec_ref:** REQ-001 (reference to requirement in spec.md)

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

**done_when:**
- [ ] Tests pass
- [ ] Acceptance criteria from REQ-001 met
- [ ] Code committed
```

## No Placeholders

Never write:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" (show the code)
- "Write tests for the above" (show the test code)
- Steps that describe what without showing how

## Self-Review

After writing the complete plan:
1. **Spec coverage:** Can you point to a task for each spec requirement? Every REQ-XXX should have a task
2. **Placeholder scan:** Search for red flags (TBD, TODO, implement later)
3. **Type consistency:** Do names match across tasks?
4. **Dependencies:** Are task dependencies properly tracked?
5. **Done conditions:** Does every task have clear done_when criteria?

## Execution Handoff

After saving the plan:

> "Plan complete. Two execution options:
> 1. **Subagent-Driven (recommended)** - Fresh subagent per task + two-stage review
> 2. **Inline Execution** - Execute tasks in this session with checkpoints
> Which approach?"

If Subagent-Driven: Use subagent-driven-development skill
If Inline Execution: Use executing-plans skill
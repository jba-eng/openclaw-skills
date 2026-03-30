---
name: subagent-driven-development
description: Use when dispatching subagents to implement tasks. Enforces two-stage review: spec compliance then code quality.
---

# Subagent-Driven Development

## Overview

Dispatch fresh subagents to implement each task. Enforce two-stage review after each task: (1) spec compliance, (2) code quality.

## Process

For each task in the plan:

### Stage 1: Dispatch Subagent

Dispatch a subagent with:
- The task description
- Relevant spec sections
- File paths to create/modify
- Test requirements

### Stage 2: Spec Compliance Review

After subagent completes:
- Verify all spec requirements are addressed
- Check that implementation matches spec exactly
- Flag any deviations

### Stage 3: Code Quality Review

After spec compliance passes:
- Check code style consistency
- Verify error handling
- Check test coverage
- Look for code smells

### Stage 4: Integration

- Run full test suite
- Verify no regressions
- Commit with descriptive message

## Subagent Prompt Template

```
Implement Task N: [title]

**Goal:** [what this task accomplishes]

**Files:**
- Create: [path]
- Modify: [path]

**Requirements from spec:**
- [requirement 1]
- [requirement 2]

**Tests:** Write tests in [test path]

**Process:**
1. Write failing test
2. Run to verify failure
3. Write minimal implementation
4. Run to verify pass
5. Commit

Show all test output in your response.
```

## Review Checklist

### Spec Compliance
- [ ] All spec requirements implemented
- [ ] No extra features added (YAGNI)
- [ ] Types/signatures match spec

### Code Quality
- [ ] Code follows project patterns
- [ ] Error handling present
- [ ] Tests are meaningful
- [ ] No obvious bugs

## Two-Stage Review Output

After each task:

```markdown
## Task N Review

### Spec Compliance: PASS/FAIL
- [criterion]: PASS/FAIL

### Code Quality: PASS/FAIL
- [criterion]: PASS/FAIL

### Tests: PASS/FAIL
- Test output included: yes/no

**Decision:** [approve/revise/reject]
```
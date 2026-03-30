---
name: systematic-debugging
description: Use when diagnosing unexpected behavior, errors, or test failures. Enforces 4-phase process: root-cause tracing → pattern analysis → hypothesis testing → implementation.
---

# Systematic Debugging

## Overview

Debug systematically using evidence, not guesses. Follow the 4-phase process.

## 4-Phase Process

### Phase 1: Gather Evidence

- Read error messages completely
- Check logs, stack traces
- Reproduce the issue consistently
- Identify what's different from expected

### Phase 2: Form Hypothesis

Based on evidence:
- What could cause this?
- What's the most likely cause?
- What evidence would confirm/reject?

### Phase 3: Test Hypothesis

- Design a test to confirm/reject
- Run the test
- Analyze results
- Refine hypothesis if needed

### Phase 4: Implement Fix

- Fix the root cause, not symptoms
- Write regression test
- Verify fix works
- Commit

## Debugging Rules

1. **Never guess** - Always have evidence
2. **One variable at a time** - Change one thing, test
3. **Reproduce first** - Must be able to reproduce consistently
4. **Check assumptions** - What do you think is true that might not be?
5. **Rubber duck** - Explain the problem out loud

## Output Template

```markdown
## Debug Session

### Phase 1: Evidence
- Error: [exact error]
- Expected: [what should happen]
- Actual: [what happened]
- Reproduction: [steps]

### Phase 2: Hypothesis
- Hypothesis: [what I think is wrong]
- Confidence: [high/medium/low]
- Evidence: [why I think this]

### Phase 3: Testing
- Test: [what I ran]
- Result: [what happened]
- Conclusion: [confirm/reject/refine]

### Phase 4: Fix
- Root cause: [what was actually wrong]
- Fix: [what I changed]
- Verification: [test output]
```

## Anti-Patterns

- Changing things randomly hoping it works
- "It should work" without evidence
- Fixing symptoms not root cause
- Skipping reproduction steps
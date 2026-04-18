---
name: verification-before-completion
description: Use when you believe work is complete. Must run tests and show actual output before claiming done.
---

# Verification Before Completion

## The Rule

**Never claim work is done without proof.** You must show actual test output.

## Checklist

- [ ] All tests pass (show output)
- [ ] Manual testing done (show results)
- [ ] No linting errors
- [ ] No type errors
- [ ] Documentation updated
- [ ] Code follows style guide

## Verification Output

For each item, show actual command output:

```markdown
## Verification

### Tests
```
$ npm test
PASS src/utils.test.js
PASS src/api.test.js
Test Suites: 2 passed, 2 total
```

### Lint
```
$ npm run lint
✓ No linting errors
```

### Type Check
```
$ npm run typecheck
✓ No type errors
```

## What NOT To Say

- "Tests should pass" (show they do)
- "It works locally" (show it)
- "I tested manually" (show what you tested)
- "Linting looks fine" (run it and show)

## If Tests Fail

1. Don't claim completion
2. Debug using systematic-debugging
3. Fix the issues
4. Re-run verification
5. Only then claim done
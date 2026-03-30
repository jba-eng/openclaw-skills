---
name: requesting-code-review
description: Use before any PR or merge. Enforces pre-review checklist and structured review process.
---

# Requesting Code Review

## Pre-Review Checklist

Before requesting review, verify:

- [ ] All tests pass locally
- [ ] Code follows project style
- [ ] No console.log or debug code left
- [ ] Commit history is clean (rebase if needed)
- [ ] PR description is complete
- [ ] Screenshots/video if UI changes

## PR Description Template

```markdown
## Summary
[One sentence describing what this PR does]

## Changes
- [change 1]
- [change 2]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing done
- [ ] Screenshots for UI changes

## Notes
[Any context reviewers need]
```

## Requesting Review

1. Push branch: `git push -u origin feature/my-feature`
2. Create PR with description
3. Request specific reviewers
4. Link related issues

## What Reviewers Look For

- Correctness (does it work?)
- Design (is it well-structured?)
- Tests (are they adequate?)
- Style (does it match project patterns?)
- Comments (are they clear?)

## During Review

- Be responsive to feedback
- Don't take comments personally
- Explain your reasoning
- Make changes requested
- Re-request review after changes
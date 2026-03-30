---
name: receiving-code-review
description: Use when handling code review feedback. Structured process for addressing comments with technical rigor.
---

# Receiving Code Review

## Overview

Handle code review feedback systematically. Every comment deserves a response, either action or explanation.

## Process

### 1. Read All Comments First

Don't respond immediately. Read all feedback to understand the full picture.

### 2. Categorize Comments

For each comment, determine:
- **Must fix**: Actual bug, security issue, test failure
- **Should fix**: Style, clarity, improvement
- **Nice to have**: Future improvement, optional
- **No change needed**: Explain why current approach is correct

### 3. Address Each Comment

**For must/should fix:**
- Make the change
- Comment "Done" with commit SHA

**For no change needed:**
- Explain your reasoning clearly
- Be respectful but firm if you disagree

### 4. Respond to All Comments

Never ignore a comment. Even "I disagree" is a response.

## Response Template

```markdown
## Review Response

### Must Fix
- [comment]: Done - [commit SHA]
- [comment]: Done - [commit SHA]

### Should Fix
- [comment]: Done - [commit SHA]
- [comment]: I see it differently because [reason]. Let's discuss.

### Nice to Have
- [comment]: Created issue #123 for follow-up

### No Change Needed
- [comment]: Current approach is correct because [explanation]
```

## Re-Request Review

After addressing all comments:
1. Push changes
2. Re-request review
3. Highlight what changed

## If You Disagree

- Explain your reasoning with facts
- Show alternative approaches considered
- Ask for clarification if unclear
- Accept final decision gracefully
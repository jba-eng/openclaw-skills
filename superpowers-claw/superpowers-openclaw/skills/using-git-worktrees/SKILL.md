---
name: using-git-worktrees
description: Use when starting any new feature or bug fix. Isolates each piece of work in its own git worktree with clean test baseline.
---

# Using Git Worktrees

## Overview

Isolate each feature or bug fix in its own git worktree. This keeps work clean and allows parallel development.

## Process

1. **Check current state** - git status, current branch
2. **Create worktree** for new work
3. **Verify clean baseline** - tests pass in worktree
4. **Create branch** with descriptive name
5. **Start work** in the worktree

## Commands

```bash
# Check current state
git status
git branch -a

# Create worktree (feature)
git worktree add ../myproject-feature feature
cd ../myproject-feature

# Or create worktree with new branch
git worktree add -b feature/my-new-feature ../myproject-feature main

# Verify clean baseline
npm test  # or your test command
```

## Branch Naming

Use descriptive names:
- `feature/add-user-authentication`
- `bugfix/fix-login-redirect`
- `refactor/improve-api-error-handling`

## Worktree Management

```bash
# List worktrees
git worktree list

# Remove worktree when done
git worktree remove ../myproject-feature
git branch -d feature/my-new-feature
```

## Clean Baseline

Before starting work, verify:
- [ ] Tests pass on current branch
- [ ] No uncommitted changes
- [ ] Worktree is clean

If baseline isn't clean, fix first or discuss with user.
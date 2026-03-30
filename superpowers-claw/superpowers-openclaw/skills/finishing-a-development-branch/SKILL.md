---
name: finishing-a-development-branch
description: Use when completing a feature or bug fix and deciding what to do with the branch. Handles merge/PR decisions and worktree cleanup.
---

# Finishing a Development Branch

## Overview

When a feature or bug fix is complete, decide what to do with the branch and clean up worktrees.

## Decision Tree

```
Is work complete and verified?
├── NO → Continue working
└── YES → Are there tests?
    ├── NO → Write tests first
    └── YES → Is there a PR/merge request?
        ├── NO → Create PR
        └── YES → Is it approved?
            ├── NO → Address feedback
            └── YES → Merge and cleanup
```

## Options

### Option 1: Merge (if ready)
```bash
git checkout main
git pull
git merge feature/my-feature
git push
git branch -d feature/my-feature
```

### Option 2: Create PR (if code review needed)
```bash
git push -u origin feature/my-feature
# Then create PR via GitHub/GitLab UI
```

### Option 3: Keep branch (if work is paused)
- Leave branch for later
- Document what's left to do

### Option 4: Discard (if abandoning)
```bash
git checkout main
git worktree remove ../myproject-feature
git branch -D feature/my-feature
```

## Worktree Cleanup

```bash
# List all worktrees
git worktree list

# Remove worktree
git worktree remove ../myproject-feature
```

## Pre-Merge Checklist

- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Branch is up to date with target
# Quick Reference - Spec Coding Skill

Fast lookup for common operations.

## Python Utilities

### Task Manager
```bash
# Discover project and verify specs
python scripts/task_manager.py discover "project-name"

# Get task status overview
python scripts/task_manager.py status .specifications/tasks.md

# Find next planned task
python scripts/task_manager.py next .specifications/tasks.md

# Update task status (returns content, doesn't write)
python scripts/task_manager.py update .specifications/tasks.md T1 in_progress
python scripts/task_manager.py update .specifications/tasks.md T1 done
```

### Task Validator
```bash
# Check specific task readiness
python scripts/task_validator.py check .specifications/tasks.md T1

# List all tasks with status
python scripts/task_validator.py list .specifications/tasks.md
```

## Workflow Stages

1. **Discover** → `task_manager.py discover`
2. **Load State** → `task_manager.py status`
3. **Announce** → Show task ID and description
4. **Mark In-Progress** → Update status, show diff, get approval
5. **Implement** → Code in src/, tests in tests/
6. **Validate** → Check all done_when conditions
7. **Mark Done** → Update status, show diff, get approval

## Task Status Values

- `planned` - Not started
- `in_progress` - Currently working
- `done` - Completed
- `blocked` - Waiting on dependencies
- `deferred` - Postponed

## Core Rules

1. Sequential execution (T1 → T2 → T3)
2. One task at a time
3. All done_when must pass
4. Show diffs before writes
5. Get approval for status changes
6. Never modify spec.md or design.md
7. Read context before coding

## Token Savings

| Operation | Manual | With Scripts | Savings |
|-----------|--------|--------------|---------|
| Discovery | ~300 | ~50 | 250 |
| Status Parse | ~250 | ~50 | 200 |
| Update | ~200 | ~50 | 150 |
| Validation | ~300 | ~50 | 250 |
| **Per Task** | ~1050 | ~200 | **850** |

## Common Commands

### Start Coding Session
```bash
# 1. Discover and verify
python scripts/task_manager.py discover "my-app"

# 2. Check what's next
python scripts/task_manager.py next .specifications/tasks.md

# 3. Validate task
python scripts/task_validator.py check .specifications/tasks.md T1
```

### During Task Execution
```bash
# Mark in-progress
python scripts/task_manager.py update .specifications/tasks.md T1 in_progress

# Check conditions
python scripts/task_validator.py check .specifications/tasks.md T1

# Mark done
python scripts/task_manager.py update .specifications/tasks.md T1 done
```

### Check Progress
```bash
# Overall status
python scripts/task_manager.py status .specifications/tasks.md

# List all tasks
python scripts/task_validator.py list .specifications/tasks.md
```

## done_when Conditions

### Good Examples
✅ "API endpoint returns 200"
✅ "Unit tests pass"
✅ "File exists: src/api.ts"
✅ "Error displays for invalid input"

### Bad Examples
❌ "Code is good"
❌ "Feature works"
❌ "Implement properly"

## File Safety

### Allowed
- Create/modify files in `src/`
- Create/modify files in `tests/`
- Update `tasks.md` status field only

### Forbidden
- Modify `spec.md`
- Modify `design.md`
- Delete files (unless task requires it)
- Modify other task fields in `tasks.md`

## Error Handling

### "Specs incomplete"
→ Run spec-creation skill first

### "No planned tasks"
→ All tasks done! Check status

### "Task not found"
→ Verify task ID format (T1, T2, etc.)

### "Blocked on unclear requirement"
→ Ask user for clarification

## Integration

### From spec-creation
After specs are created:
```
"Ready to start implementation? Type 'yes' to activate spec-coding"
```

### To spec-testing
After all tasks done:
```
"All tasks complete! Run spec-testing to validate implementation"
```

## Typical Session

```
1. Discover: "my-app" → Ready ✓
2. Status: 5 tasks, 2 done, 3 planned
3. Next: T3 "Build search API"
4. Mark in-progress → Approved ✓
5. Implement code
6. Validate: All conditions pass ✓
7. Show diff → Approved ✓
8. Mark done → Approved ✓
9. Continue to T4? → Yes
```

## Output Format

### Discovery
```json
{
  "project": "my-app",
  "ready": true,
  "files": {"spec.md": true, "design.md": true, "tasks.md": true}
}
```

### Status
```json
{
  "stats": {"total": 5, "done": 2, "planned": 3},
  "next_task": {"id": "T3", "description": "..."}
}
```

### Validation
```json
{
  "ready": true,
  "conditions": [
    {"condition": "API returns 200", "status": "pending"}
  ]
}
```

---

**Need help?** See README.md for detailed documentation.

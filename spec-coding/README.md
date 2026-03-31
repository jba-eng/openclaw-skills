# Spec Coding Skill

Sequential task execution engine for implementing code from specifications with strict validation and approval workflow.

## Overview

This skill is a disciplined executor of predefined specifications. It executes tasks from `tasks.md` ONE AT A TIME in strict sequential order, validating each task against its `done_when` conditions before proceeding.

## Features

- 🎯 **Sequential Execution** - Tasks run in order (T1 → T2 → T3), never skipped
- ✅ **Strict Validation** - All done_when conditions must pass
- 🔒 **State Management** - Tracks task status (planned → in_progress → done)
- 📊 **Progress Tracking** - Shows completion statistics
- 💬 **Approval Workflow** - User approves each task completion
- 🤖 **Token Efficient** - Python utilities save 30-40% tokens per task
- 🛡️ **Spec Protection** - Never modifies spec.md or design.md

## Prerequisites

This skill requires existing specifications created by the `spec-creation` skill:
- `.specifications/spec.md` - Requirements and acceptance criteria
- `.specifications/design.md` - Architecture and components
- `.specifications/tasks.md` - Implementation tasks

## Quick Start

### Using with OpenClaw Agent

Trigger the skill:
```
"coding skill"
"run tasks"
"execute tasks"
"/code"
```

The agent will:
1. Discover your project
2. Verify spec files exist
3. Find the next planned task
4. Execute it with validation
5. Get your approval
6. Move to the next task

### Direct CLI Usage

```bash
# Discover project and verify specs
python scripts/task_manager.py discover "my-project"

# Get task status
python scripts/task_manager.py status .specifications/tasks.md

# Find next task
python scripts/task_manager.py next .specifications/tasks.md

# Validate task conditions
python scripts/task_validator.py check .specifications/tasks.md T1
```

## Python Utilities

### 1. Task Manager (`task_manager.py`)

Manages task state and execution flow.

```bash
# Discover project
python scripts/task_manager.py discover "my-app"

# Get status overview
python scripts/task_manager.py status .specifications/tasks.md

# Find next planned task
python scripts/task_manager.py next .specifications/tasks.md

# Update task status (returns updated content, doesn't write)
python scripts/task_manager.py update .specifications/tasks.md T1 in_progress
```

**Output**: JSON with task information and statistics

### 2. Task Validator (`task_validator.py`)

Validates done_when conditions.

```bash
# Check specific task
python scripts/task_validator.py check .specifications/tasks.md T1

# List all tasks with readiness
python scripts/task_validator.py list .specifications/tasks.md
```

**Output**: JSON with condition validation results

## Workflow

### Stage 1: Project Discovery

```bash
python scripts/task_manager.py discover "my-project"
```

Verifies:
- Project exists
- `.specifications/` directory exists
- Required files present (spec.md, design.md, tasks.md)

### Stage 2: Load Task State

```bash
python scripts/task_manager.py status .specifications/tasks.md
```

Shows:
- Total tasks
- Completed count
- In-progress tasks
- Next planned task

### Stage 3: Execute Task

For each task:

1. **Announce**: "Starting T1: Build search API"
2. **Mark in-progress**: Update status with approval
3. **Read context**: Review spec.md and design.md
4. **Implement**: Create/modify code in src/ and tests/
5. **Validate**: Check all done_when conditions
6. **Show diff**: Display all changes
7. **Get approval**: User reviews and approves
8. **Mark done**: Update status with approval
9. **Continue**: Ask if user wants next task

## Task Format

Tasks in `tasks.md` follow this structure:

```markdown
## T1: Build search API

**Status**: planned

**Dependencies**: None

**Done When**: 
- GET /api/search endpoint returns 200
- Query parameter validation works
- Unit tests pass with 80% coverage
- Error handling for empty queries

**Estimated Effort**: 4 hours
```

## done_when Conditions

The `done_when` field defines completion criteria. ALL conditions must be satisfied.

### Good Conditions

✅ "API endpoint returns 200 status"
✅ "Unit tests pass"
✅ "File src/api/search.ts exists"
✅ "Error message displays for invalid input"

### Bad Conditions

❌ "Code is good" (not testable)
❌ "Implement feature" (not specific)
❌ "Make it work" (not measurable)

## Core Rules

1. **Sequential only** - Never skip tasks
2. **One at a time** - Never batch multiple tasks
3. **done_when is law** - All conditions must pass
4. **Show diffs** - Always display changes before writing
5. **Get approval** - User must approve each completion
6. **Protect specs** - Never modify spec.md or design.md
7. **Read context** - Always review specs before coding

## Token Savings

| Operation | Manual | With Scripts | Savings |
|-----------|--------|--------------|---------|
| Task Discovery | ~300 | ~50 | 250 |
| Status Parsing | ~250 | ~50 | 200 |
| Status Update | ~200 | ~50 | 150 |
| Validation | ~300 | ~50 | 250 |
| **Total per task** | ~1050 | ~200 | **850** |

## File Structure

```
spec-coding/
├── SKILL.md                    # Core skill instructions
├── README.md                   # This file
├── scripts/
│   ├── task_manager.py         # Task state management
│   └── task_validator.py       # Condition validation
└── templates/
    └── task_template.md        # Task format template
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
- Existing specifications from spec-creation skill

## Examples

### Example Workflow

```bash
# 1. Discover project
python scripts/task_manager.py discover "my-app"

# Output:
# {
#   "project": "my-app",
#   "ready": true,
#   "files": {
#     "spec.md": true,
#     "design.md": true,
#     "tasks.md": true
#   }
# }

# 2. Check status
python scripts/task_manager.py status .specifications/tasks.md

# Output:
# {
#   "stats": {
#     "total": 5,
#     "planned": 3,
#     "in_progress": 0,
#     "done": 2
#   },
#   "next_task": {
#     "id": "T3",
#     "description": "Build search API",
#     "status": "planned"
#   }
# }

# 3. Validate task
python scripts/task_validator.py check .specifications/tasks.md T3

# Output:
# {
#   "task": {...},
#   "ready": true,
#   "conditions": [
#     {"condition": "API returns 200", "status": "pending"},
#     {"condition": "Tests pass", "status": "pending"}
#   ]
# }
```

### Example Task Execution

```
Agent: "Starting T3: Build search API"

Agent: "Marking T3 as in-progress..."
[Shows diff of tasks.md]
User: "yes"

Agent: [Implements code in src/api/search.ts]
Agent: [Creates tests in tests/search.test.ts]

Agent: "Validating done_when conditions:"
✓ GET /api/search returns 200
✓ Query validation works
✓ Unit tests pass
✓ Error handling implemented

Agent: [Shows code diff]
Agent: "All conditions satisfied. Approve completion?"
User: "yes"

Agent: "Marking T3 as done..."
[Shows diff of tasks.md]
User: "yes"

Agent: "Task T3 complete ✅ Proceed to T4?"
```

## Best Practices

1. **Review specs first** - Always read spec.md and design.md before coding
2. **Validate thoroughly** - Check each done_when condition explicitly
3. **Show your work** - Display diffs before any file writes
4. **Test as you go** - Run tests after implementation
5. **One task focus** - Complete current task before thinking about next
6. **Ask when blocked** - Don't guess if requirements are unclear

## Troubleshooting

### "Specs incomplete"

Run the spec-creation skill first to create required files.

### "No planned tasks remaining"

All tasks are complete! Check status:
```bash
python scripts/task_manager.py status .specifications/tasks.md
```

### "Task not found"

Verify task ID exists in tasks.md. Task IDs must be in format: T1, T2, T3, etc.

### "done_when conditions unclear"

Ask the user for clarification. Never guess what a condition means.

## Integration

### After spec-creation

The spec-creation skill will offer to start spec-coding automatically:

```
Specs complete! Ready to start implementation?
- Type 'yes' to activate spec-coding skill
```

### Before spec-testing

After all tasks are complete, you can run spec-testing skill to validate the implementation.

## Contributing

This skill is part of the OpenClaw ecosystem. Contributions welcome!

## License

MIT License - See LICENSE file for details

## Author

Jonathan (OpenClaw)

## Version

1.0.0

---

**Ready to code?** Trigger the skill and let's execute those tasks!

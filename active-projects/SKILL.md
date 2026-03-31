---
name: Active Projects
slug: active-projects
version: 1.0.0
description: Manages the list of active projects for autocoder nightly execution. Add/remove projects and track execution state.
metadata: {"requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}
---

## When to Use

Manage which projects are active for overnight autocoder execution. This skill maintains the master list that the nightly orchestrator checks.

## Core Purpose

This skill is the central registry for autocoder. It:
- Maintains `active_projects.json` - the master list
- Provides commands to add/remove projects
- Tracks last check time and settings
- Stores global run state

## File Location

**Important**: The autocoder nightly orchestrator reads from:
`workspace/skills/active-projects/active_projects.json`

This is the single source of truth for which projects should run overnight.

## Commands

### List Active Projects

```bash
python -c "import json; print('\n'.join(json.load(open('workspace/skills/active-projects/active_projects.json'))['active_projects']))"
```

Or simply:
```bash
cat workspace/skills/active-projects/active_projects.json
```

### Add Project

```bash
python -c "
import json
from pathlib import Path

file = Path('workspace/skills/active-projects/active_projects.json')
data = json.loads(file.read_text())

project = 'PROJECT_NAME'
if project not in data['active_projects']:
    data['active_projects'].append(project)
    file.write_text(json.dumps(data, indent=2))
    print(f'✓ Added {project}')
else:
    print(f'✗ {project} already active')
"
```

### Remove Project

```bash
python -c "
import json
from pathlib import Path

file = Path('workspace/skills/active-projects/active_projects.json')
data = json.loads(file.read_text())

project = 'PROJECT_NAME'
if project in data['active_projects']:
    data['active_projects'].remove(project)
    file.write_text(json.dumps(data, indent=2))
    print(f'✓ Removed {project}')
else:
    print(f'✗ {project} not in active list')
"
```

### Check Project Status

```bash
python -c "
import json
from pathlib import Path

file = Path('workspace/skills/active-projects/active_projects.json')
data = json.loads(file.read_text())

project = 'PROJECT_NAME'
if project in data['active_projects']:
    print(f'✓ {project} is ACTIVE')
else:
    print(f'✗ {project} is NOT active')
"
```

## File Structure

### active_projects.json

```json
{
  "active_projects": [
    "Archivera",
    "MyProject"
  ],
  "last_check": "2026-03-27T01:00:00",
  "settings": {
    "check_interval_minutes": 30,
    "max_tasks_per_run": 2,
    "auto_mark_complete": true,
    "validate_tasks": true,
    "check_dependencies": true,
    "create_quality_files": true
  }
}
```

**Fields**:
- `active_projects` - Array of project names (must match folder names in `workspace/software-projects/`)
- `last_check` - ISO timestamp of last orchestrator run
- `settings` - Configuration for task execution

### RUN_STATE.json

Global run state tracking all projects:

```json
{
  "last_run": "2026-03-27T01:00:00Z",
  "projects_checked": 2,
  "projects_with_work": 1,
  "total_tasks_tonight": 5
}
```

## Integration with Autocoder

The autocoder nightly orchestrator:
1. Reads `workspace/skills/active-projects/active_projects.json`
2. For each project in `active_projects` array
3. Checks if project exists in `workspace/software-projects/{PROJECT}/`
4. Checks if project has pending tasks in `tasks.md`
5. Spawns executor for projects with work

## Workflow

### Adding a New Project

1. Create project in `workspace/software-projects/`:
   ```bash
   mkdir -p workspace/software-projects/MyProject
   ```

2. Create specifications:
   ```bash
   cd workspace/software-projects/MyProject
   python -m openclaw.skills.spec_creation
   ```

3. Add to active list:
   ```bash
   # Edit active_projects.json or use command above
   ```

4. That's it! Next 1:00 AM run will pick it up.

### Removing a Project

1. Remove from active list:
   ```bash
   # Edit active_projects.json or use command above
   ```

2. Project files remain in `workspace/software-projects/` but won't be executed.

### Temporarily Disabling All Projects

Set `active_projects` to empty array:
```json
{
  "active_projects": []
}
```

Orchestrator will exit immediately with "No active projects found."

## Settings

### check_interval_minutes
How often to check for new tasks (not currently used by orchestrator)

### max_tasks_per_run
Maximum tasks to execute per project per run (not currently enforced)

### auto_mark_complete
Automatically mark tasks as done when done_when conditions pass

### validate_tasks
Validate task format before execution

### check_dependencies
Check task dependencies before execution

### create_quality_files
Create quality assurance files during execution

## Monitoring

### Check Last Run

```bash
cat workspace/skills/active-projects/RUN_STATE.json
```

### Check Active Projects

```bash
cat workspace/skills/active-projects/active_projects.json
```

### View All Project States

```bash
for project in workspace/software-projects/*/; do
  echo "=== $(basename $project) ==="
  cat "$project/.run_state.json" 2>/dev/null || echo "No state"
  echo
done
```

## File Locations

```
workspace/skills/active-projects/
├── SKILL.md (this file)
├── active_projects.json          ← Master list (read by orchestrator)
├── RUN_STATE.json                ← Global run state
└── ACTIVE-PROJECTS.md            ← Documentation
```

## Related Skills

- **autocoder** - Reads this skill's active_projects.json for nightly execution
- **spec-creation** - Creates specifications for new projects
- **spec-coding** - Executes tasks from project's tasks.md

## Core Rules

1. **Single source of truth** - Only `active_projects.json` in this skill determines what runs
2. **Project names must match** - Names in array must match folder names in `workspace/software-projects/`
3. **No duplicates** - Each project should appear only once in array
4. **Valid JSON** - File must be valid JSON or orchestrator will fail
5. **Atomic updates** - Always read, modify, write to avoid corruption

## Troubleshooting

### Project not running?

1. Check it's in active list:
   ```bash
   grep "PROJECT_NAME" workspace/skills/active-projects/active_projects.json
   ```

2. Check project folder exists:
   ```bash
   ls workspace/software-projects/PROJECT_NAME/
   ```

3. Check project has pending tasks:
   ```bash
   grep "**Status:** planned" workspace/software-projects/PROJECT_NAME/tasks.md
   ```

### JSON parse error?

Validate JSON:
```bash
python -m json.tool workspace/skills/active-projects/active_projects.json
```

### Want to disable all overnight runs?

Set empty array:
```json
{
  "active_projects": []
}
```

## Version History

- 1.0.0 - Initial version with active_projects.json management

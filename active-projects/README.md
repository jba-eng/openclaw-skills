# Active-Projects Skill - Complete Guide

## Overview

Manages the master list of active projects for autocoder nightly execution. This skill is the single source of truth for which projects should run overnight.

**Version**: 1.0.0

---

## Quick Start

### Check Active Projects

```bash
cat workspace/skills/active-projects/active_projects.json
```

### Add Project

Edit `active_projects.json`:
```json
{
  "active_projects": [
    "Archivera",
    "MyNewProject"
  ]
}
```

Or use Python:
```bash
python -c "
import json
from pathlib import Path

file = Path('workspace/skills/active-projects/active_projects.json')
data = json.loads(file.read_text())

project = 'MyNewProject'
if project not in data['active_projects']:
    data['active_projects'].append(project)
    file.write_text(json.dumps(data, indent=2))
    print(f'✓ Added {project}')
"
```

### Remove Project

Edit `active_projects.json` or use Python:
```bash
python -c "
import json
from pathlib import Path

file = Path('workspace/skills/active-projects/active_projects.json')
data = json.loads(file.read_text())

project = 'MyNewProject'
if project in data['active_projects']:
    data['active_projects'].remove(project)
    file.write_text(json.dumps(data, indent=2))
    print(f'✓ Removed {project}')
"
```

---

## File Structure

### active_projects.json

**Location**: `workspace/skills/active-projects/active_projects.json`

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

**Location**: `workspace/skills/active-projects/RUN_STATE.json`

Global run state tracking all projects:

```json
{
  "last_run": "2026-03-27T01:00:00Z",
  "projects_checked": 2,
  "projects_with_work": 1,
  "total_tasks_tonight": 5
}
```

---

## Integration with Autocoder

The autocoder nightly orchestrator:
1. Reads `workspace/skills/active-projects/active_projects.json`
2. For each project in `active_projects` array
3. Checks if project exists in `workspace/software-projects/{PROJECT}/`
4. Checks if project has pending tasks in `tasks.md`
5. Spawns executor for projects with work

---

## Workflow

### Adding a New Project

1. **Create project** in `workspace/software-projects/`:
   ```bash
   mkdir -p workspace/software-projects/MyProject
   ```

2. **Create specifications** (use spec-creation skill):
   ```bash
   cd workspace/software-projects/MyProject
   # Run spec-creation skill
   ```

3. **Add to active list**:
   ```bash
   # Edit active_projects.json or use Python command above
   ```

4. **Done!** Next 1:00 AM run will pick it up.

### Removing a Project

1. **Remove from active list**:
   ```bash
   # Edit active_projects.json or use Python command above
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

---

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

---

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

---

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

---

## Related Skills

- **autocoder** - Reads this skill's active_projects.json for nightly execution
- **spec-creation** - Creates specifications for new projects
- **spec-coding** - Executes tasks from project's tasks.md

---

## Version History

- **1.0.0** - Initial version with active_projects.json management

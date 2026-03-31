---
name: Autocoder
slug: autocoder
version: 4.0.0
description: Simplified autonomous overnight coding via heartbeat. Main agent writes coding-agent's HEARTBEAT.md nightly. Coding-agent executes tasks every 30 minutes overnight.
metadata: {"requires":{"bins":["python3"],"skills":["active-projects","spec-coding"]},"os":["linux","darwin","win32"]}
---

## When to Use

Autonomous overnight task execution. Simplified architecture using agent heartbeats instead of complex cron orchestration.

## Architecture (Simplified)

### Two-Agent Heartbeat Pattern

```
1:00 AM - Main agent cron job fires
    ↓
nightly_heartbeat_writer.py
    ├─ Reads: workspace/skills/active-projects/active_projects.json
    ├─ Checks each project for pending tasks
    └─ Writes: workspace/subagents/coding-agent/HEARTBEAT.md
        ↓
Coding-agent heartbeat (every 30 min overnight)
    ├─ Reads its own HEARTBEAT.md
    ├─ Executes ONE task from ONE project
    ├─ Updates project's tasks.md status
    └─ Exits (waits for next heartbeat)
```

**Key simplification**: No lock files, no state files, no orchestrators. Just heartbeat-driven execution.

## Configuration

### Main Agent Cron Job

**Location**: `cron/jobs.json`

```json
{
  "id": "autocoder-nightly-heartbeat",
  "name": "Autocoder Nightly Heartbeat Writer",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 1 * * *",
    "tz": "America/Toronto"
  },
  "payload": {
    "kind": "shellCommand",
    "command": "cd /home/jonathan/.openclaw && python3 workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py"
  }
}
```

### Coding-Agent Heartbeat

**Location**: `openclaw.json` → `agents.list` → coding-agent

```json
{
  "id": "coding-agent",
  "workspace": "/home/jonathan/.openclaw/workspace/subagents/coding-agent",
  "heartbeat": {
    "every": "30m",
    "target": "last",
    "prompt": "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK."
  }
}
```

## How It Works

### 1. Nightly Setup (1:00 AM)

Main agent cron job runs `nightly_heartbeat_writer.py`:

1. Reads `workspace/skills/active-projects/active_projects.json`
2. For each active project, checks if `tasks.md` has pending tasks
3. Writes `workspace/subagents/coding-agent/HEARTBEAT.md` with:
   - List of projects with pending work
   - Instructions for coding-agent
   - Task format and rules

### 2. Overnight Execution (Every 30 min)

Coding-agent heartbeat fires:

1. Reads its own `HEARTBEAT.md`
2. If projects listed:
   - Picks first project with pending tasks
   - Reads `specs.md`, `design.md`, `tasks.md`
   - Executes ONE task
   - Updates task status in `tasks.md`
   - Exits
3. If no projects or no pending tasks:
   - Replies with `HEARTBEAT_OK`
   - Exits

### 3. Morning Review

Check what happened overnight:

```bash
# View coding-agent's instructions
cat workspace/subagents/coding-agent/HEARTBEAT.md

# Check project task status
grep "**Status:**" workspace/software-projects/Archivera/tasks.md

# View coding-agent's session history
cat agents/coding-agent/sessions/sessions.json
```

## File Locations

### Active Projects (from active-projects skill)
```
workspace/skills/active-projects/
├── active_projects.json           ← Master list (read by heartbeat writer)
└── SKILL.md
```

### Coding-Agent Workspace
```
workspace/subagents/coding-agent/
├── HEARTBEAT.md                   ← Written by main agent nightly
├── AGENTS.md
├── TOOLS.md
└── memory/
```

### Project Files (per project)
```
workspace/software-projects/{PROJECT}/
├── specs.md                       ← Requirements
├── design.md                      ← Architecture
├── tasks.md                       ← Task queue (updated by coding-agent)
├── src/
└── tests/
```

### Autocoder Skill
```
workspace/skills/autocoder/
├── SKILL.md (this file)
├── README.md
└── scripts/
    └── nightly_heartbeat_writer.py
```

## Task Format

Tasks use status field format:

```markdown
### T1: Project Structure & Dependencies
**Status:** planned
**Dependencies:** None
**Done When:**
1. Project directory structure created
2. requirements.txt with all dependencies
3. config.yaml template created
```

**Status values**:
- `planned` - Ready to execute
- `in-progress` - Currently being worked on
- `done` - Completed successfully
- `failed` - Execution failed

## Workflow

### Setup (One-time)

1. Add project to active list (use active-projects skill)
2. Create project specifications (use spec-creation skill)
3. Cron job already configured in `cron/jobs.json`
4. Coding-agent heartbeat already configured in `openclaw.json`

### Nightly Execution

```
1:00 AM
  ↓
Main agent cron fires
  ↓
nightly_heartbeat_writer.py
  ├─ Checks active_projects.json
  ├─ Finds Archivera has pending tasks
  └─ Writes coding-agent/HEARTBEAT.md with Archivera listed
      ↓
1:30 AM - Coding-agent heartbeat fires
  ├─ Reads HEARTBEAT.md
  ├─ Sees Archivera listed
  ├─ Executes task 1 from Archivera
  └─ Updates tasks.md status to "done"
      ↓
2:00 AM - Coding-agent heartbeat fires
  ├─ Reads HEARTBEAT.md (still has Archivera)
  ├─ Executes task 2 from Archivera
  └─ Updates tasks.md status to "done"
      ↓
... continues every 30 min until all tasks done or morning
```

### Morning Review

```bash
# Check what coding-agent was told to do
cat workspace/subagents/coding-agent/HEARTBEAT.md

# Check Archivera's task progress
grep "**Status:**" workspace/software-projects/Archivera/tasks.md

# View coding-agent's last session
# (check agents/coding-agent/sessions/sessions.json for latest session ID)
```

## Dependencies

### Required Skills
- **active-projects** - Provides master list of active projects
- **spec-coding** - Task execution guidelines (coding-agent follows these)

### Required Files
- `workspace/skills/active-projects/active_projects.json` - Must exist
- `workspace/software-projects/{PROJECT}/tasks.md` - Must exist per project
- `cron/jobs.json` - Must have heartbeat writer job configured
- `openclaw.json` - Must have coding-agent with heartbeat configured

## Core Rules

1. **Single nightly cron** - One job at 1:00 AM writes HEARTBEAT.md
2. **Heartbeat-driven** - Coding-agent executes via 30-min heartbeat
3. **One task per heartbeat** - Each heartbeat executes one task
4. **Active project detection** - Only runs projects in active-projects skill
5. **Status tracking** - Progress tracked in tasks.md status field
6. **No lock files** - Heartbeat mechanism prevents concurrent runs
7. **No state files** - HEARTBEAT.md is the only coordination file
8. **Minimal context** - HEARTBEAT.md references spec-coding skill, doesn't repeat instructions
9. **Session isolation** - Each heartbeat is independent, no context bloat

## Context Management

### Why Minimal HEARTBEAT.md?

The HEARTBEAT.md is intentionally tiny (5 lines):
- Lists active projects
- References spec-coding skill
- No repeated instructions
- Prevents context bloat

### How Continuation Works

Each heartbeat is independent:
1. Coding-agent reads HEARTBEAT.md (5 lines)
2. Uses spec-coding skill (references skill, doesn't load full instructions)
3. Reads tasks.md to find next pending task
4. Executes ONE task
5. Updates task status
6. Exits (session ends, context cleared)

Next heartbeat starts fresh:
- No context from previous heartbeat
- Only tasks.md status persists
- Naturally continues from where it stopped

### Preventing Context Bloat

- HEARTBEAT.md: ~5 lines (was ~50 lines)
- Spec-coding skill: Referenced, not loaded in full
- Each session: Independent, no accumulation
- Task context: Read only what's needed for current task

## Safety Features

- **Active project check** - Only runs if project is in active list
- **Pending task check** - Only runs if project has pending tasks
- **Heartbeat isolation** - Each heartbeat is independent
- **Status persistence** - Progress tracked in tasks.md
- **Error isolation** - One task failure doesn't affect others
- **Simple coordination** - Just HEARTBEAT.md, no complex state

## Expected Behavior

### Normal Night (Archivera has 5 pending tasks)

```
1:00 AM  Heartbeat writer checks active_projects.json → finds Archivera
1:00 AM  Writes coding-agent/HEARTBEAT.md with Archivera listed
1:30 AM  Coding-agent heartbeat: task 1 executed
2:00 AM  Coding-agent heartbeat: task 2 executed
2:30 AM  Coding-agent heartbeat: task 3 executed
3:00 AM  Coding-agent heartbeat: task 4 executed
3:30 AM  Coding-agent heartbeat: task 5 executed
4:00 AM  Coding-agent heartbeat: no pending tasks, replies HEARTBEAT_OK
```

### Multiple Projects

```
1:00 AM  Heartbeat writer finds Archivera and MyProject both have work
1:00 AM  Writes HEARTBEAT.md listing both projects
1:30 AM  Coding-agent picks Archivera task 1
2:00 AM  Coding-agent picks Archivera task 2 (or MyProject task 1)
         ... continues alternating or prioritizing
```

### No Active Projects

```
1:00 AM  Heartbeat writer checks active_projects.json → empty array
1:00 AM  Writes HEARTBEAT.md: "No active coding tasks at this time"
1:30 AM  Coding-agent reads HEARTBEAT.md → replies HEARTBEAT_OK
```

## Monitoring

### Check Current Instructions

```bash
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

### Check Project Progress

```bash
grep "**Status:**" workspace/software-projects/Archivera/tasks.md
```

### Check Active Projects

```bash
cat workspace/skills/active-projects/active_projects.json
```

## Troubleshooting

### No tasks executing?

1. Check HEARTBEAT.md was written:
   ```bash
   cat workspace/subagents/coding-agent/HEARTBEAT.md
   ```

2. Check active_projects.json:
   ```bash
   cat workspace/skills/active-projects/active_projects.json
   ```

3. Check project has pending tasks:
   ```bash
   grep "**Status:** planned" workspace/software-projects/Archivera/tasks.md
   ```

4. Check coding-agent heartbeat is enabled in openclaw.json

### HEARTBEAT.md not being written?

1. Check cron job enabled:
   ```bash
   grep -A 5 "autocoder-nightly-heartbeat" cron/jobs.json | grep enabled
   ```

2. Check cron job ran:
   ```bash
   grep "lastRunAtMs" cron/jobs.json
   ```

### Coding-agent not responding to heartbeat?

1. Check openclaw.json has coding-agent with heartbeat configured
2. Check coding-agent workspace path is correct
3. Restart OpenClaw to reload configuration

## Advantages Over Previous Architecture

### Old (Complex)
- Multiple cron jobs 15 minutes apart
- Lock files per project
- State files per project
- Orchestrator + executor scripts
- Complex coordination logic

### New (Simple)
- Single cron job nightly
- No lock files needed
- No state files needed
- Single heartbeat writer script
- Heartbeat handles coordination

**Result**: 80% less code, 90% less complexity, same functionality.

## Related Skills

- **active-projects** - Manages master list of active projects (required)
- **spec-creation** - Creates specifications in project folder
- **spec-coding** - Task execution guidelines (coding-agent follows these)

## Version History

- 4.0.0 - Simplified to heartbeat-driven architecture
- 3.0.0 - Master orchestrator pattern with active-projects integration
- 2.0.0 - Restructured with per-project state files
- 1.0.0 - Initial version

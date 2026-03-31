# Autocoder Skill

Simplified autonomous overnight coding via agent heartbeats.

## Overview

Autocoder enables overnight autonomous coding using a two-agent heartbeat pattern:

1. **Main agent** (1 cron job nightly) → checks active projects → writes coding-agent's HEARTBEAT.md
2. **Coding-agent** (heartbeat every 30min) → reads HEARTBEAT.md → executes one task → updates tasks.md

No lock files. No state files. No complex orchestration. Just heartbeats.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1:00 AM - Main Agent Cron Job                              │
│                                                             │
│ nightly_heartbeat_writer.py                                │
│   ├─ Read: active_projects.json                           │
│   ├─ Check: each project's tasks.md for pending work      │
│   └─ Write: coding-agent/HEARTBEAT.md                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Every 30 min - Coding-Agent Heartbeat                      │
│                                                             │
│ Coding-Agent                                               │
│   ├─ Read: HEARTBEAT.md (in its workspace)                │
│   ├─ If projects listed:                                  │
│   │   ├─ Pick first project with pending tasks           │
│   │   ├─ Read: specs.md, design.md, tasks.md             │
│   │   ├─ Execute: ONE task                               │
│   │   └─ Update: tasks.md status field                   │
│   └─ If no work: reply HEARTBEAT_OK                       │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Add a Project

```bash
# Add to active projects list
cd workspace/skills/active-projects
# Edit active_projects.json, add "MyProject" to array
```

### 2. Create Specifications

```bash
# Create project folder
mkdir -p workspace/software-projects/MyProject

# Create specs (use spec-creation skill)
# This creates: specs.md, design.md, tasks.md
```

### 3. Done!

That's it. Next 1:00 AM:
- Main agent checks active projects
- Finds MyProject has pending tasks
- Writes coding-agent/HEARTBEAT.md
- Coding-agent starts executing tasks every 30 min

## Configuration

### Main Agent Cron Job

File: `cron/jobs.json`

```json
{
  "id": "autocoder-nightly-heartbeat",
  "schedule": {
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

File: `openclaw.json` → `agents.list` → coding-agent

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

## File Structure

```
workspace/
├── skills/
│   ├── active-projects/
│   │   └── active_projects.json          ← Master list
│   └── autocoder/
│       ├── SKILL.md
│       ├── README.md (this file)
│       └── scripts/
│           └── nightly_heartbeat_writer.py
│
├── subagents/
│   └── coding-agent/
│       └── HEARTBEAT.md                  ← Written nightly by main agent
│
└── software-projects/
    └── {PROJECT}/
        ├── specs.md                      ← Requirements
        ├── design.md                     ← Architecture
        ├── tasks.md                      ← Task queue (updated by coding-agent)
        ├── src/
        └── tests/
```

## How It Works

### Nightly (1:00 AM)

Main agent cron job runs `nightly_heartbeat_writer.py`:

1. Reads `active_projects.json`
2. For each project, checks if `tasks.md` has pending tasks
3. Writes `coding-agent/HEARTBEAT.md` with:
   - List of projects with work
   - Instructions for coding-agent
   - Task format and rules

Example HEARTBEAT.md:

```markdown
# HEARTBEAT.md

Active projects: Archivera, MyProject

Use spec-coding skill to execute ONE task from ONE project.

If no pending tasks, reply: HEARTBEAT_OK

---
2026-03-27T01:00:00
```

**Why so minimal?**
- Prevents context bloat
- References spec-coding skill instead of repeating instructions
- Coding-agent loads skill on-demand
- Each heartbeat session is independent

### Overnight (Every 30 min)

Coding-agent heartbeat fires:

1. Reads its own `HEARTBEAT.md` (5 lines)
2. If projects listed:
   - Uses spec-coding skill (referenced, not fully loaded)
   - Picks first project with pending tasks
   - Reads context (only what's needed for current task)
   - Executes ONE task
   - Updates task status
   - Exits (session ends, context cleared)
3. If no work:
   - Replies `HEARTBEAT_OK`
   - Exits

**Context Management**: Each heartbeat is independent. No context accumulation between sessions. Only tasks.md status persists.

### Morning

Check what happened:

```bash
# View instructions
cat workspace/subagents/coding-agent/HEARTBEAT.md

# Check progress
grep "**Status:**" workspace/software-projects/Archivera/tasks.md

# View session history
cat agents/coding-agent/sessions/sessions.json
```

## Task Format

Tasks in `tasks.md` use status field format:

```markdown
### T1: Build login endpoint
**Status:** planned
**Dependencies:** None
**Done When:**
1. Endpoint responds to POST /login
2. Returns JWT token on success
3. Tests passing

### T2: Add password validation
**Status:** done
**Dependencies:** T1
**Done When:**
1. Password length >= 8 characters
2. Contains uppercase, lowercase, number
3. Tests passing
```

Status values:
- `planned` - Ready to execute
- `in-progress` - Currently being worked on
- `done` - Completed successfully
- `failed` - Execution failed

## Monitoring

### Check Current Instructions

```bash
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

### Check Active Projects

```bash
cat workspace/skills/active-projects/active_projects.json
```

### Check Project Progress

```bash
# View all task statuses
grep "**Status:**" workspace/software-projects/Archivera/tasks.md

# Count completed tasks
grep "**Status:** done" workspace/software-projects/Archivera/tasks.md | wc -l

# Count pending tasks
grep "**Status:** planned" workspace/software-projects/Archivera/tasks.md | wc -l
```

### Check Coding-Agent Sessions

```bash
# List recent sessions
cat agents/coding-agent/sessions/sessions.json

# View specific session
cat agents/coding-agent/sessions/{SESSION_ID}.jsonl
```

## Troubleshooting

### No tasks executing?

**Check 1**: HEARTBEAT.md was written
```bash
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

**Check 2**: Active projects configured
```bash
cat workspace/skills/active-projects/active_projects.json
```

**Check 3**: Project has pending tasks
```bash
grep "**Status:** planned" workspace/software-projects/Archivera/tasks.md
```

**Check 4**: Coding-agent heartbeat enabled
```bash
grep -A 10 "coding-agent" openclaw.json | grep heartbeat
```

### HEARTBEAT.md not being written?

**Check 1**: Cron job enabled
```bash
grep -A 5 "autocoder-nightly-heartbeat" cron/jobs.json | grep enabled
```

**Check 2**: Cron job ran
```bash
grep "lastRunAtMs" cron/jobs.json
```

**Check 3**: Script exists
```bash
ls -la workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py
```

### Coding-agent not responding?

**Check 1**: Heartbeat configured in openclaw.json
```bash
grep -A 10 "coding-agent" openclaw.json
```

**Check 2**: Workspace path correct
```bash
ls -la workspace/subagents/coding-agent/
```

**Check 3**: Restart OpenClaw
```bash
# Restart to reload configuration
```

## Advantages

### Old Architecture (Complex)
- Multiple cron jobs 15 minutes apart
- Lock files per project
- State files per project  
- Orchestrator + executor scripts
- Complex coordination logic
- ~500 lines of code

### New Architecture (Simple)
- Single cron job nightly
- No lock files
- No state files
- Single heartbeat writer script
- Heartbeat handles coordination
- ~100 lines of code

**Result**: 80% less code, 90% less complexity, same functionality.

## Context Management

### Problem: Context Bloat

Long-running agents accumulate context:
- Previous task details
- Old file contents
- Repeated instructions
- Session history

This can cause:
- Incomplete task execution
- Token limit issues
- Slower responses

### Solution: Session Isolation

Each heartbeat creates a fresh session:

1. **Minimal HEARTBEAT.md** (5 lines)
   - Lists active projects
   - References spec-coding skill
   - No repeated instructions

2. **Independent Sessions**
   - Each heartbeat = new session
   - No context from previous heartbeat
   - Only tasks.md status persists

3. **On-Demand Skill Loading**
   - Spec-coding skill referenced, not embedded
   - Loaded only when needed
   - Instructions not repeated in HEARTBEAT.md

4. **Focused Task Context**
   - Read only what's needed for current task
   - Don't load entire specs.md if not needed
   - Minimal file reading

### How Continuation Works

**Question**: If each session is independent, how does it continue?

**Answer**: Task status in tasks.md

```markdown
### T1: Build login
**Status:** done

### T2: Add validation
**Status:** done

### T3: Create database
**Status:** planned  ← Next heartbeat picks this up

### T4: Add tests
**Status:** planned
```

Each heartbeat:
1. Reads tasks.md
2. Finds first `planned` or `failed` task
3. Executes it
4. Updates status to `done` or `failed`
5. Exits

Next heartbeat repeats, picking up where it left off.

## Testing

### Test Heartbeat Writer

```bash
# Run manually
cd /home/jonathan/.openclaw
python3 workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py

# Check output
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

### Test Coding-Agent

```bash
# Via Telegram (if configured)
# Send message to coding-agent: "Check HEARTBEAT.md and execute one task"

# Or manually trigger heartbeat
# (depends on OpenClaw CLI commands)
```

### Test End-to-End

1. Add test project to active_projects.json
2. Create test project with one simple task
3. Run heartbeat writer manually
4. Trigger coding-agent heartbeat
5. Check task status updated

## Related Skills

- **active-projects** - Manages master list (required)
- **spec-creation** - Creates project specifications
- **spec-coding** - Task execution guidelines

## Version History

- 4.0.0 - Simplified to heartbeat-driven architecture
- 3.0.0 - Master orchestrator pattern
- 2.0.0 - Per-project state files
- 1.0.0 - Initial version

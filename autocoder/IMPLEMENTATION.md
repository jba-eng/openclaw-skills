# Autocoder Implementation Guide

Version 4.0.0 | 2026-03-27

## Overview

Simple heartbeat-driven autonomous coding. One cron job writes HEARTBEAT.md nightly, coding-agent executes tasks every 30 minutes.

## Architecture

```
1:00 AM - Main agent cron
    ↓
nightly_heartbeat_writer.py
    ├─ Read: active_projects.json
    ├─ Check: tasks.md for pending work
    └─ Write: coding-agent/HEARTBEAT.md (7 lines)
        ↓
Every 30 min - Coding-agent heartbeat
    ├─ Read: HEARTBEAT.md (50 tokens)
    ├─ Use: spec-coding skill (on-demand)
    ├─ Execute: ONE task
    ├─ Update: tasks.md status
    └─ Exit (context cleared)
        ↓
6:00 AM - Morning cleanup cron
    └─ Clear: coding-agent/HEARTBEAT.md (stop overnight execution)
```

## What Changed from v3.0

### Eliminated
- ❌ Multiple cron jobs (was 4-16, now 2: start + cleanup)
- ❌ Lock files per project
- ❌ State files per project
- ❌ Nightly logs per project
- ❌ 5 complex scripts (~500 lines)

### Kept
- ✅ Two cron jobs (1:00 AM start, 6:00 AM cleanup)
- ✅ Single coordination file (HEARTBEAT.md, 7 lines)
- ✅ Single script (nightly_heartbeat_writer.py, ~100 lines)
- ✅ Heartbeat mechanism (built-in)

**Result**: 80% less code, 90% less complexity

## Context Management

### The Problem
Long-running agents accumulate context → incomplete tasks, token limits, slow responses

### The Solution
Each heartbeat = independent session. No context accumulation.

### HEARTBEAT.md (Minimal)

```markdown
# HEARTBEAT.md

Active projects: Archivera

Use spec-coding skill to execute ONE task from ONE project.

If no pending tasks, reply: HEARTBEAT_OK

---
2026-03-27T01:00:00
```

**Token cost**: ~50 tokens (was ~500)

**Why minimal?**
- References spec-coding skill (not embedded)
- No repeated instructions
- No task/project details
- Loaded on-demand by coding-agent

### Session Isolation

```
Heartbeat 1 (1:30 AM)
├─ Read HEARTBEAT.md (50 tokens)
├─ Load spec-coding skill (on-demand)
├─ Find next task in tasks.md
├─ Execute task 1
├─ Update status → done
└─ Exit (context cleared)

Heartbeat 2 (2:00 AM)
├─ Read HEARTBEAT.md (50 tokens)
├─ Load spec-coding skill (on-demand)
├─ Find next task in tasks.md
├─ Execute task 2
├─ Update status → done
└─ Exit (context cleared)
```

**Key**: No context carried between heartbeats. Only tasks.md status persists.

### Continuation

Progress tracked in tasks.md:

```markdown
### T1: Build login
**Status:** done  ← Completed

### T2: Add validation
**Status:** planned  ← Next heartbeat picks this up
```

Each heartbeat:
1. Reads tasks.md
2. Finds first `planned` or `failed` task
3. Executes it
4. Updates status
5. Exits

## Configuration

### Cron Jobs (cron/jobs.json)

**1. Nightly Heartbeat Writer (1:00 AM)**

```json
{
  "id": "autocoder-nightly-heartbeat",
  "schedule": {
    "expr": "0 1 * * *",
    "tz": "America/Toronto"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the nightly heartbeat writer: python workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py"
  }
}
```

**2. Morning Cleanup (6:00 AM)**

```json
{
  "id": "autocoder-morning-cleanup",
  "schedule": {
    "expr": "0 6 * * *",
    "tz": "America/Toronto"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Clear the coding-agent HEARTBEAT.md: echo '# HEARTBEAT.md\n\nNo active coding tasks.\n\nReply: HEARTBEAT_OK' > workspace/subagents/coding-agent/HEARTBEAT.md"
  },
  "delivery": {
    "mode": "silent"
  }
}
```

### Coding-Agent Heartbeat (openclaw.json)

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
│       ├── README.md
│       ├── IMPLEMENTATION.md (this file)
│       └── scripts/
│           └── nightly_heartbeat_writer.py
│
├── subagents/
│   └── coding-agent/
│       └── HEARTBEAT.md                  ← Written nightly (7 lines)
│
└── software-projects/
    └── {PROJECT}/
        ├── specs.md                      ← Requirements
        ├── design.md                     ← Architecture
        ├── tasks.md                      ← Task queue (updated by coding-agent)
        ├── src/
        └── tests/
```

## Testing

### Test Heartbeat Writer

```bash
python workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

Expected output:
```
============================================================
Nightly Heartbeat Writer
============================================================

📋 Active projects: 1

🔍 Checking Archivera...
   ✓ Has pending tasks

📝 Writing HEARTBEAT.md...
✓ Wrote HEARTBEAT.md for coding-agent
  Projects with work: 1
    - Archivera

============================================================
✓ Complete
============================================================
```

### Test Coding-Agent

Via Telegram:
```
Send to coding-agent: "Check HEARTBEAT.md and execute one task"
```

## Monitoring

### Check Current Instructions
```bash
cat workspace/subagents/coding-agent/HEARTBEAT.md
```

### Check Progress
```bash
grep "**Status:**" workspace/software-projects/Archivera/tasks.md
```

### Check Active Projects
```bash
cat workspace/skills/active-projects/active_projects.json
```

## Troubleshooting

### No tasks executing?

1. Check HEARTBEAT.md written:
   ```bash
   cat workspace/subagents/coding-agent/HEARTBEAT.md
   ```

2. Check active projects:
   ```bash
   cat workspace/skills/active-projects/active_projects.json
   ```

3. Check pending tasks:
   ```bash
   grep "**Status:** planned" workspace/software-projects/Archivera/tasks.md
   ```

4. Check coding-agent heartbeat enabled in openclaw.json

### Tasks not completing?

**Symptom**: Status stays `in-progress`

**Possible cause**: Context too large

**Solution**:
1. Verify HEARTBEAT.md is minimal (~7 lines)
2. Check spec-coding skill is concise
3. Break large tasks into smaller ones

### Agent repeating work?

**Symptom**: Same task executed multiple times

**Possible cause**: Status not being updated

**Solution**:
1. Check tasks.md status field format
2. Ensure agent updates status before exiting
3. Check file write permissions

## Best Practices

### For HEARTBEAT.md
✅ List active projects
✅ Reference skills (don't embed)
✅ Keep under 10 lines

❌ Don't repeat skill instructions
❌ Don't include task details
❌ Don't add workflow steps

### For Tasks
✅ Clear done_when conditions
✅ One focused goal per task
✅ Update status immediately

❌ Don't make tasks too large
❌ Don't skip status updates
❌ Don't modify specs.md

## Comparison

| Metric | v3.0 | v4.0 | Improvement |
|--------|------|------|-------------|
| Cron jobs | 4-16 | 2 | 50-88% fewer |
| Scripts | 6 | 1 | 83% fewer |
| Lines of code | ~500 | ~100 | 80% less |
| State files | Per project | 0 | 100% eliminated |
| Lock files | Per project | 0 | 100% eliminated |
| HEARTBEAT.md | 50 lines | 7 lines | 86% smaller |
| Context per heartbeat | ~4000 tokens | ~2000 tokens | 50% less |

## Version History

- v4.0 (2026-03-27) - Heartbeat-driven, minimal context
- v3.0 (2026-03-26) - Master orchestrator pattern
- v2.0 (2026-03-25) - Per-project state files
- v1.0 (2026-03-23) - Initial version

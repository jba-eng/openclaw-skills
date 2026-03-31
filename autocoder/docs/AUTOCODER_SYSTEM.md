# Autocoder System - Complete Setup Guide

This document explains the three-skill system for autonomous overnight coding and how to set it up.

## System Overview

Three skills work together to automate coding tasks:

1. **spec-creation** → Takes a user idea, writes SPEC.md + TASKS.md
2. **spec-coding** → Executes one task per invocation, updates TASKS.md status
3. **autocoder** → Overnight scheduler that drives spec-coding via cron jobs (15 min apart, 1:00 AM - 4:45 AM)

## Key Differences from Previous Version

### Problem Solved
The old system had no state persistence. Each cron invocation started from scratch instead of resuming where the previous run left off.

### Solution
- **spec-coding** now executes ONE task per run and updates TASKS.md status before exiting
- **autocoder** manages a lock file to prevent concurrent runs
- **RUN_STATE.json** tracks progress across runs
- **NIGHTLY_LOG.md** logs every execution for morning review

## Workflow

### 1. Create Specifications (One-time)

Run spec-creation skill:
```bash
python -m openclaw.skills.spec_creation
```

This creates:
- `spec.md` - Requirements and acceptance criteria
- `design.md` - Architecture and components
- `TASKS.md` - Task list with status checkboxes

### 2. Set Up Cron Schedule

Add to your system cron (NOT HEARTBEAT.md):

```bash
# Every 15 minutes from 1:00 AM to 4:45 AM
*/15 1-4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

Or with explicit times:
```bash
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

### 3. Overnight Execution

Each cron invocation:
1. Checks `.autocoder.lock` (prevents concurrent runs)
2. Reads TASKS.md to find next pending task
3. Calls spec-coding skill to execute that one task
4. Updates TASKS.md status
5. Updates RUN_STATE.json
6. Appends entry to NIGHTLY_LOG.md
7. Releases lock file

## Data Files

All data files are located in the **project root** (same directory as spec.md and design.md):

### TASKS.md
Main task queue. Location: `./TASKS.md`. Format:
```markdown
## Tasks

- [ ] T1: Build login endpoint
- [x] T2: Add password validation
- [!] T3: Create user database (error: connection timeout)
```

Status meanings:
- `[ ]` = pending (ready to execute)
- `[~]` = in_progress (should not exist between runs)
- `[x]` = done (completed successfully)
- `[!]` = failed (with error note inline)

### RUN_STATE.json
Current execution state (updated after each task). Location: `./RUN_STATE.json`.
```json
{
  "last_run": "2026-03-27T01:15:00Z",
  "last_task": "Build login endpoint",
  "last_status": "done",
  "tasks_completed_tonight": 3,
  "tasks_remaining": 8
}
```

### NIGHTLY_LOG.md
Execution log (append-only). Location: `./NIGHTLY_LOG.md`. Example entries:
```markdown
[2026-03-27 01:15] task: "Build login endpoint" → status: done (12m 3s)
[2026-03-27 01:30] task: "Add password validation" → status: done (8m 15s)
[2026-03-27 01:45] Lock file active, skipping run
[2026-03-27 02:00] task: "Create user database" → status: failed (error: connection timeout)
[2026-03-27 04:45] Queue empty, no tasks pending
```

### .autocoder.lock
Runtime lock file (created/deleted by autocoder). Location: `./autocoder.lock`. Contains ISO timestamp:
```
2026-03-27T01:15:00Z
```

## Expected Behavior

### Normal Night (All Tasks Complete)
```
1:00 AM  cron fires → lock created → task 1 executed → lock released → log written
1:15 AM  cron fires → no lock → task 2 executed → lock released → log written
1:30 AM  cron fires → no lock → task 3 executed → lock released → log written
1:45 AM  cron fires → no lock → task 4 executed → lock released → log written
2:00 AM  cron fires → no lock → task 5 executed → lock released → log written
...
4:45 AM  cron fires → no lock → queue empty → exits → log written
```

### Slow Task (Takes >15 minutes)
```
1:00 AM  cron fires → lock created → task 1 starts (slow)
1:15 AM  cron fires → sees active lock (recent) → logs "Lock active, skipping" → exits
1:30 AM  task 1 finishes → lock released
1:30 AM  cron fires → no lock → task 2 executed → lock released → log written
```

### Stale Lock (Crash Recovery)
```
1:00 AM  cron fires → lock created → task 1 starts
1:00 AM  process crashes → lock remains
1:15 AM  cron fires → sees lock older than 20 min → deletes it → continues
1:15 AM  task 2 executed → lock released → log written
```

## Safety Features

1. **Lock file prevents concurrent runs** - If a task takes >15 min, next cron sees active lock and exits
2. **Stale lock detection** - Locks older than 20 minutes are considered stale and deleted
3. **State tracking** - RUN_STATE.json lets you check progress without reading logs
4. **Comprehensive logging** - Every run logged with timestamp, task, and result
5. **Error isolation** - One task failure doesn't stop future runs
6. **One task per run** - No looping; next cron handles next task

## Monitoring

### Check Progress in the Morning

1. **Quick status**: Read `RUN_STATE.json`
   ```json
   {
     "last_run": "2026-03-27T04:45:00Z",
     "last_task": "Write tests",
     "last_status": "done",
     "tasks_completed_tonight": 8,
     "tasks_remaining": 0
   }
   ```

2. **Detailed log**: Read `NIGHTLY_LOG.md`
   ```markdown
   [2026-03-27 01:15] task: "Build login endpoint" → status: done (12m 3s)
   [2026-03-27 01:30] task: "Add password validation" → status: done (8m 15s)
   ...
   ```

3. **Task status**: Read `TASKS.md`
   ```markdown
   - [x] T1: Build login endpoint
   - [x] T2: Add password validation
   - [x] T3: Create user database
   ```

## Troubleshooting

### Tasks Not Running
1. Check cron is installed and running: `crontab -l`
2. Verify cron schedule is correct (should be 1:00 AM - 4:45 AM)
3. Check TASKS.md has pending tasks with `[ ]` status
4. Check logs: `tail -f NIGHTLY_LOG.md`

### Lock File Stuck
If `.autocoder.lock` exists and is older than 20 minutes:
```bash
rm .autocoder.lock
```

The next cron run will detect the stale lock and delete it automatically.

### Task Failed
Check NIGHTLY_LOG.md for error message. Task will be marked as `[!]` in TASKS.md with error note:
```markdown
- [!] T3: Create user database (error: connection timeout)
```

Fix the issue and change status back to `[ ]` to retry:
```markdown
- [ ] T3: Create user database
```

## Integration with Your Workflow

### Manual Testing
You can test the system manually:

```bash
# Test one task execution
python -m openclaw.skills.spec_coding

# Test autocoder cycle
python -m openclaw.skills.autocoder
```

### Daytime Development
During the day, you can:
1. Manually run spec-coding to execute tasks
2. Update TASKS.md to add new tasks
3. Modify spec.md or design.md as needed
4. Cron will resume overnight execution

### Monitoring
Check progress anytime:
```bash
# Quick status
cat RUN_STATE.json

# Full log
cat NIGHTLY_LOG.md

# Task list
cat TASKS.md
```

## Files Created

- `workspace/skills/spec-creation/SKILL.md` - Spec creation skill (updated)
- `workspace/skills/spec-coding/SKILL.md` - Spec coding skill (updated)
- `workspace/skills/autocoder/SKILL.md` - Autocoder skill (updated)
- `TASKS.md` - Task queue template
- `NIGHTLY_LOG.md` - Execution log
- `RUN_STATE.json` - Current state
- `AUTOCODER_SYSTEM.md` - This file

## Next Steps

1. Copy the updated skill files to your user-level skills directory:
   ```bash
   cp workspace/skills/spec-creation/SKILL.md ~/.openclaw/workspace/skills/spec-creation/
   cp workspace/skills/spec-coding/SKILL.md ~/.openclaw/workspace/skills/spec-coding/
   cp workspace/skills/autocoder/SKILL.md ~/.openclaw/workspace/skills/autocoder/
   ```

2. Set up your cron schedule (see "Set Up Cron Schedule" above)

3. Create your first spec using spec-creation skill

4. Test manually with spec-coding skill

5. Let cron run overnight and check results in the morning

## Questions?

Refer to the individual SKILL.md files for detailed documentation:
- `workspace/skills/spec-creation/SKILL.md` - Spec creation workflow
- `workspace/skills/spec-coding/SKILL.md` - Task execution workflow
- `workspace/skills/autocoder/SKILL.md` - Orchestration and cron setup

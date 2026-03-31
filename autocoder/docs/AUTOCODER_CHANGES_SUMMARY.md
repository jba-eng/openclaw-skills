# Autocoder System - Changes Summary

## Problem Statement

The old autocoder system had no state persistence. Each cron invocation started from scratch instead of resuming where the previous run left off. This meant:
- No way to track which tasks were completed
- No way to resume after a failure
- No visibility into overnight execution
- Tasks could be executed multiple times or skipped

## Solution Overview

Three skills now work together with proper state management:

1. **spec-creation** - Creates specifications (one-time)
2. **spec-coding** - Executes ONE task per invocation
3. **autocoder** - Orchestrates overnight execution via cron

## Fix 1: Task Status Tracking (spec-coding)

### Before
- No status field in tasks
- No way to know which tasks were done
- Skill looped through all tasks in one run

### After
- Each task has checkbox status: `[ ]` `[~]` `[x]` `[!]`
- Status persisted in TASKS.md
- Skill executes ONE task per invocation
- Status updated before exiting

### Implementation
```markdown
## Tasks

- [ ] T1: Build login endpoint
- [x] T2: Add password validation
- [!] T3: Create database (error: connection timeout)
```

**spec-coding workflow:**
1. Read TASKS.md
2. Find first task with `[ ]` or `[!]` status
3. Execute that ONE task
4. Update status to `[x]` or `[!]`
5. Exit (don't loop)

## Fix 2: Lock File Guard (autocoder)

### Before
- No lock file
- Concurrent runs could happen
- No way to prevent overlapping execution

### After
- `.autocoder.lock` file prevents concurrent runs
- 20-minute stale timeout for crash recovery
- Lock created on startup, deleted on exit

### Implementation
```bash
# On startup
if [ -f .autocoder.lock ]; then
  TIMESTAMP=$(cat .autocoder.lock)
  AGE_MINUTES=$(( ($(date +%s) - $(date -d "$TIMESTAMP" +%s)) / 60 ))
  if [ $AGE_MINUTES -gt 20 ]; then
    rm .autocoder.lock  # Stale, delete
  else
    exit 0  # Active, skip this run
  fi
fi

# Create lock
date -u +%Y-%m-%dT%H:%M:%S > .autocoder.lock

# On exit (always)
rm .autocoder.lock
```

## Fix 3: Cron-Only, No Heartbeat (autocoder)

### Before
- Used HEARTBEAT.md (continuous polling)
- No time restrictions
- Could run anytime

### After
- Cron-only execution (scheduled jobs)
- Time-gated: 1:00 AM - 4:45 AM only
- 15-minute intervals
- No heartbeat mode

### Implementation
```bash
# Add to system cron (NOT HEARTBEAT.md)
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

## Fix 4: Run Log (autocoder)

### Before
- No logging
- No visibility into execution
- No way to debug issues

### After
- NIGHTLY_LOG.md (append-only)
- One-line entry per run
- Timestamp, task, status, duration

### Implementation
```markdown
# NIGHTLY_LOG.md

[2026-03-27 01:15] task: "Build login endpoint" → status: done (12m 3s)
[2026-03-27 01:30] task: "Add password validation" → status: done (8m 15s)
[2026-03-27 01:45] Lock file active, skipping run
[2026-03-27 02:00] task: "Create database" → status: failed (error: connection timeout)
[2026-03-27 04:45] Queue empty, no tasks pending
```

## Fix 5: Run State (autocoder)

### Before
- No state tracking
- No way to check progress without reading logs
- No summary of overnight execution

### After
- RUN_STATE.json (updated after each task)
- Quick status check
- Progress tracking

### Implementation
```json
{
  "last_run": "2026-03-27T01:15:00Z",
  "last_task": "Build login endpoint",
  "last_status": "done",
  "tasks_completed_tonight": 3,
  "tasks_remaining": 8
}
```

## Files Created

### Skill Files (Updated)
- `workspace/skills/spec-creation/SKILL.md` - Updated with task status format
- `workspace/skills/spec-coding/SKILL.md` - Rewritten for one-task-per-run
- `workspace/skills/autocoder/SKILL.md` - Rewritten for cron orchestration

### Data Files (New)
- `TASKS.md` - Task queue template
- `NIGHTLY_LOG.md` - Execution log
- `RUN_STATE.json` - Current state

### Documentation (New)
- `AUTOCODER_SYSTEM.md` - Complete setup guide
- `AUTOCODER_QUICK_START.md` - 5-minute setup
- `AUTOCODER_CHANGES_SUMMARY.md` - This file

## Expected Behavior After Fixes

### Normal Night
```
1:00 AM  cron fires → lock created → task 1 executed → lock released → log written
1:15 AM  cron fires → no lock → task 2 executed → lock released → log written
1:30 AM  cron fires → no lock → task 3 executed → lock released → log written
...
4:45 AM  cron fires → no lock → queue empty → exits → log written
```

### Slow Task (>15 minutes)
```
1:00 AM  cron fires → lock created → task 1 starts (slow)
1:15 AM  cron fires → sees active lock → logs "Lock active, skipping" → exits
1:30 AM  task 1 finishes → lock released
1:30 AM  cron fires → no lock → task 2 executed → lock released → log written
```

### Crash Recovery
```
1:00 AM  cron fires → lock created → task 1 starts
1:00 AM  process crashes → lock remains
1:15 AM  cron fires → sees stale lock (>20 min) → deletes it → continues
1:15 AM  task 2 executed → lock released → log written
```

## Key Improvements

1. **State Persistence** - Tasks tracked in TASKS.md with status
2. **Concurrency Control** - Lock file prevents overlapping runs
3. **Crash Recovery** - Stale lock detection (20-minute timeout)
4. **Visibility** - NIGHTLY_LOG.md and RUN_STATE.json for monitoring
5. **One Task Per Run** - No looping; cron handles sequencing
6. **Time-Gated** - Runs only 1:00 AM - 4:45 AM via cron
7. **Error Handling** - Failed tasks marked with error notes
8. **Retry Logic** - Failed tasks can be retried by changing status back to `[ ]`

## Migration Path

1. Copy updated skill files to user-level skills directory
2. Set up cron schedule (4 lines for 1-4 AM)
3. Create first spec with spec-creation skill
4. Test manually with spec-coding skill
5. Let cron run overnight
6. Check progress in morning with RUN_STATE.json and NIGHTLY_LOG.md

## Backward Compatibility

- Old TASKS.md format still works (will be converted to checkbox format)
- Old spec.md and design.md files unchanged
- No breaking changes to spec-creation workflow
- spec-coding now requires one-task-per-run discipline

## Testing

### Manual Test
```bash
# Test one task execution
python -m openclaw.skills.spec_coding

# Test autocoder cycle
python -m openclaw.skills.autocoder
```

### Verify Files
```bash
# Check task status
cat TASKS.md

# Check execution log
cat NIGHTLY_LOG.md

# Check current state
cat RUN_STATE.json

# Check for lock file (should not exist between runs)
ls -la .autocoder.lock
```

## Questions?

See:
- `AUTOCODER_SYSTEM.md` - Complete documentation
- `AUTOCODER_QUICK_START.md` - 5-minute setup
- Individual SKILL.md files - Detailed workflows

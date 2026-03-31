# Autocoder System - Complete Documentation

## What is Autocoder?

Autocoder is a three-skill system for autonomous overnight coding. It automatically executes coding tasks from a specification, one task per 15-minute interval, between 1:00 AM and 4:45 AM.

## Problem Solved

The old system had no state persistence. Each cron invocation started from scratch instead of resuming where the previous run left off. This meant:
- No way to track which tasks were completed
- No way to resume after a failure
- No visibility into overnight execution
- Tasks could be executed multiple times or skipped

## Solution

Three skills work together with proper state management:

1. **spec-creation** - Creates specifications (one-time)
2. **spec-coding** - Executes ONE task per invocation
3. **autocoder** - Orchestrates overnight execution via cron

## Quick Start (5 Minutes)

### 1. Copy Updated Skills
```bash
cp workspace/skills/spec-creation/SKILL.md ~/.openclaw/workspace/skills/spec-creation/
cp workspace/skills/spec-coding/SKILL.md ~/.openclaw/workspace/skills/spec-coding/
cp workspace/skills/autocoder/SKILL.md ~/.openclaw/workspace/skills/autocoder/
```

### 2. Set Up Cron
```bash
crontab -e
```

Add these lines (replace `/path/to/project` with your project directory):
```bash
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

### 3. Create Your First Spec
```bash
python -m openclaw.skills.spec_creation
```

### 4. Test Manually
```bash
python -m openclaw.skills.spec_coding
```

### 5. Let Cron Run
Overnight (1:00 AM - 4:45 AM), cron will automatically execute remaining tasks.

## Documentation Files

### Getting Started
- **AUTOCODER_QUICK_START.md** - 5-minute setup guide
- **AUTOCODER_SYSTEM.md** - Complete setup and troubleshooting
- **CRON_SETUP_MANUAL.md** - Manual cron configuration

### Reference
- **AUTOCODER_CHANGES_SUMMARY.md** - What changed and why
- **CRON_SETUP.sh** - Automated cron setup script

### Skill Files
- **workspace/skills/spec-creation/SKILL.md** - Create specifications
- **workspace/skills/spec-coding/SKILL.md** - Execute tasks
- **workspace/skills/autocoder/SKILL.md** - Orchestrate execution

## Data Files

### Task Queue
- **TASKS.md** - List of tasks with status

### Execution Tracking
- **NIGHTLY_LOG.md** - Log of all runs
- **RUN_STATE.json** - Current execution state
- **.autocoder.lock** - Runtime lock file (auto-managed)

## Task Status Format

In TASKS.md:
```markdown
- [ ] T1: Build login endpoint
- [x] T2: Add password validation
- [!] T3: Create database (error: connection timeout)
```

Status meanings:
- `[ ]` = pending (ready to execute)
- `[x]` = done (completed)
- `[!]` = failed (with error note)

## Expected Behavior

### Normal Night
```
1:00 AM  cron fires → task 1 executed
1:15 AM  cron fires → task 2 executed
1:30 AM  cron fires → task 3 executed
...
4:45 AM  cron fires → queue empty, exit
```

### Slow Task (>15 minutes)
```
1:00 AM  cron fires → task 1 starts (slow)
1:15 AM  cron fires → sees active lock → skips
1:30 AM  task 1 finishes → lock released
1:30 AM  cron fires → task 2 executed
```

### Crash Recovery
```
1:00 AM  cron fires → task 1 starts
1:00 AM  process crashes → lock remains
1:15 AM  cron fires → sees stale lock (>20 min) → deletes it
1:15 AM  task 2 executed
```

## Check Progress

### Quick Status
```bash
cat RUN_STATE.json
```

### Full Log
```bash
cat NIGHTLY_LOG.md
```

### Task List
```bash
cat TASKS.md
```

## Key Features

1. **State Persistence** - Tasks tracked in TASKS.md with status
2. **Concurrency Control** - Lock file prevents overlapping runs
3. **Crash Recovery** - Stale lock detection (20-minute timeout)
4. **Visibility** - NIGHTLY_LOG.md and RUN_STATE.json for monitoring
5. **One Task Per Run** - No looping; cron handles sequencing
6. **Time-Gated** - Runs only 1:00 AM - 4:45 AM via cron
7. **Error Handling** - Failed tasks marked with error notes
8. **Retry Logic** - Failed tasks can be retried

## Troubleshooting

### Tasks not running?
1. Check cron: `crontab -l`
2. Check TASKS.md has `[ ]` status tasks
3. Check logs: `tail NIGHTLY_LOG.md`

### Task failed?
1. Check error in TASKS.md: `[!] T3: ... (error: ...)`
2. Fix the issue
3. Change status back to `[ ]` to retry

### Lock file stuck?
```bash
rm .autocoder.lock
```

## Files Created

### Skill Files (Updated)
- `workspace/skills/spec-creation/SKILL.md`
- `workspace/skills/spec-coding/SKILL.md`
- `workspace/skills/autocoder/SKILL.md`

### Data Files (New)
- `TASKS.md`
- `NIGHTLY_LOG.md`
- `RUN_STATE.json`

### Documentation (New)
- `AUTOCODER_README.md` (this file)
- `AUTOCODER_QUICK_START.md`
- `AUTOCODER_SYSTEM.md`
- `AUTOCODER_CHANGES_SUMMARY.md`
- `CRON_SETUP_MANUAL.md`
- `CRON_SETUP.sh`

## Next Steps

1. Read **AUTOCODER_QUICK_START.md** for 5-minute setup
2. Copy updated skill files to your user-level skills directory
3. Set up cron schedule (see **CRON_SETUP_MANUAL.md**)
4. Create your first spec with spec-creation skill
5. Test manually with spec-coding skill
6. Let cron run overnight
7. Check progress in morning with RUN_STATE.json and NIGHTLY_LOG.md

## Questions?

- **Setup help**: See AUTOCODER_QUICK_START.md
- **Complete guide**: See AUTOCODER_SYSTEM.md
- **Cron setup**: See CRON_SETUP_MANUAL.md
- **What changed**: See AUTOCODER_CHANGES_SUMMARY.md
- **Skill details**: See individual SKILL.md files

## Summary of Fixes

### Fix 1: Task Status Tracking
- Each task has checkbox status: `[ ]` `[~]` `[x]` `[!]`
- Status persisted in TASKS.md
- spec-coding executes ONE task per invocation

### Fix 2: Lock File Guard
- `.autocoder.lock` prevents concurrent runs
- 20-minute stale timeout for crash recovery
- Lock created on startup, deleted on exit

### Fix 3: Cron-Only, No Heartbeat
- Cron-only execution (scheduled jobs)
- Time-gated: 1:00 AM - 4:45 AM only
- 15-minute intervals
- No heartbeat mode

### Fix 4: Run Log
- NIGHTLY_LOG.md (append-only)
- One-line entry per run
- Timestamp, task, status, duration

### Fix 5: Run State
- RUN_STATE.json (updated after each task)
- Quick status check
- Progress tracking

---

**Ready to get started?** See AUTOCODER_QUICK_START.md

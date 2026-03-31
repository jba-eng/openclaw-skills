# Autocoder Quick Reference Card

## One-Page Cheat Sheet

### Task Status Format
```markdown
- [ ] T1: Task description (pending)
- [x] T2: Task description (done)
- [!] T3: Task description (error: reason)
- [~] T4: Task description (in_progress - should not exist)
```

### Cron Schedule
```bash
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

### Key Files
| File | Purpose | Updated By |
|------|---------|-----------|
| TASKS.md | Task queue | spec-coding |
| NIGHTLY_LOG.md | Execution log | autocoder |
| RUN_STATE.json | Current state | autocoder |
| .autocoder.lock | Runtime lock | autocoder |

### Common Commands
```bash
# Check status
cat RUN_STATE.json

# View log
tail -f NIGHTLY_LOG.md

# View tasks
cat TASKS.md

# Test manually
python -m openclaw.skills.spec_coding

# Check cron
crontab -l

# View cron logs
sudo tail -f /var/log/syslog | grep CRON
```

### Execution Flow
```
Cron fires (every 15 min, 1-4 AM)
    ↓
autocoder checks lock
    ↓
autocoder calls spec-coding
    ↓
spec-coding executes ONE task
    ↓
spec-coding updates TASKS.md
    ↓
autocoder updates RUN_STATE.json
    ↓
autocoder logs to NIGHTLY_LOG.md
    ↓
autocoder releases lock
```

### Lock File Behavior
```
Normal:     Create → Execute → Delete
Slow task:  Create → Execute (slow) → Next cron sees lock → Skip
Crash:      Create → Crash → Stale lock (>20 min) → Delete & continue
```

### Troubleshooting
| Problem | Solution |
|---------|----------|
| Tasks not running | Check cron: `crontab -l` |
| Lock file stuck | `rm .autocoder.lock` |
| Task failed | Check error in TASKS.md: `[!] ... (error: ...)` |
| No log entries | Check NIGHTLY_LOG.md exists |
| Cron not running | `sudo systemctl start cron` |

### Setup Steps
1. Copy skills: `cp workspace/skills/*/SKILL.md ~/.openclaw/workspace/skills/*/`
2. Add cron: `crontab -e` (add 4 lines)
3. Create spec: `python -m openclaw.skills.spec_creation`
4. Test: `python -m openclaw.skills.spec_coding`
5. Wait: Cron runs overnight (1-4 AM)
6. Check: `cat RUN_STATE.json` in morning

### Five Fixes
1. **Status Tracking** - TASKS.md with `[ ]` `[x]` `[!]`
2. **Lock File** - .autocoder.lock prevents concurrent runs
3. **Cron-Only** - Time-gated 1:00 AM - 4:45 AM
4. **Run Log** - NIGHTLY_LOG.md with entries
5. **Run State** - RUN_STATE.json for quick check

### Expected Results
```
Morning after overnight run:

RUN_STATE.json:
{
  "last_run": "2026-03-27T04:45:00Z",
  "last_task": "Write tests",
  "last_status": "done",
  "tasks_completed_tonight": 8,
  "tasks_remaining": 0
}

NIGHTLY_LOG.md:
[2026-03-27 01:15] task: "Build login" → done (12m)
[2026-03-27 01:30] task: "Add password" → done (8m)
...
[2026-03-27 04:45] Queue empty, no tasks pending

TASKS.md:
- [x] T1: Build login endpoint
- [x] T2: Add password validation
- [x] T3: Create database
...
```

### Documentation Map
```
START HERE
    ↓
AUTOCODER_README.md
    ↓
AUTOCODER_QUICK_START.md
    ↓
AUTOCODER_SYSTEM.md (for details)
    ↓
AUTOCODER_ARCHITECTURE.md (for design)
    ↓
CRON_SETUP_MANUAL.md (for cron)
    ↓
IMPLEMENTATION_CHECKLIST.md (for verification)
```

### One-Minute Summary
- **What**: Three skills that work together to execute coding tasks overnight
- **When**: 1:00 AM - 4:45 AM, every 15 minutes via cron
- **How**: spec-creation creates specs, spec-coding executes one task per run, autocoder orchestrates
- **Why**: State persistence, concurrency control, crash recovery, visibility
- **Result**: 16 tasks per night, fully automated, fully logged

### Key Concepts
- **One task per run**: spec-coding executes exactly one task, then exits
- **State persistence**: TASKS.md status updated before each exit
- **Lock file**: Prevents concurrent runs; stale if >20 minutes old
- **Cron-only**: No heartbeat; scheduled jobs only
- **Visibility**: NIGHTLY_LOG.md + RUN_STATE.json for monitoring

### Emergency Procedures
```bash
# If lock file stuck
rm .autocoder.lock

# If cron not running
sudo systemctl start cron

# If task failed
# 1. Check error in TASKS.md
# 2. Fix the issue
# 3. Change status back to [ ]
# 4. Next cron run will retry

# If need to stop overnight runs
crontab -e
# Delete the 4 autocoder lines
```

### Performance
- Typical task: 5-15 minutes
- Cron interval: 15 minutes
- Lock timeout: 20 minutes
- Overnight window: 3 hours 45 minutes (1:00 AM - 4:45 AM)
- Tasks per night: 16 (one per run)

### Files at a Glance
```
workspace/skills/
├── spec-creation/SKILL.md ← Creates specs
├── spec-coding/SKILL.md ← Executes tasks
└── autocoder/SKILL.md ← Orchestrates

workspace/
├── TASKS.md ← Task queue
├── NIGHTLY_LOG.md ← Execution log
├── RUN_STATE.json ← Current state
├── .autocoder.lock ← Runtime lock (auto-managed)
└── [documentation files]
```

### Success Indicators
- ✓ Cron jobs running (check: `crontab -l`)
- ✓ NIGHTLY_LOG.md has entries
- ✓ RUN_STATE.json updated
- ✓ TASKS.md status changed
- ✓ No .autocoder.lock between runs
- ✓ Tasks completed overnight

---

**Print this page for quick reference during setup and troubleshooting.**

# Autocoder Quick Start

## 5-Minute Setup

### 1. Copy Updated Skills
```bash
cp workspace/skills/spec-creation/SKILL.md ~/.openclaw/workspace/skills/spec-creation/
cp workspace/skills/spec-coding/SKILL.md ~/.openclaw/workspace/skills/spec-coding/
cp workspace/skills/autocoder/SKILL.md ~/.openclaw/workspace/skills/autocoder/
```

### 2. Add Cron Schedule
```bash
crontab -e
```

Add these lines:
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

Follow the prompts to create spec.md, design.md, and TASKS.md.

### 4. Test Manually
```bash
python -m openclaw.skills.spec_coding
```

This executes one task and updates TASKS.md status.

### 5. Let Cron Run
Overnight (1:00 AM - 4:45 AM), cron will automatically execute remaining tasks.

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

## Task Status Format

In TASKS.md:
- `[ ]` = pending (ready to execute)
- `[x]` = done (completed)
- `[!]` = failed (with error note)

Example:
```markdown
- [ ] T1: Build login endpoint
- [x] T2: Add password validation
- [!] T3: Create database (error: connection timeout)
```

## One Task Per Run

**Important**: Each invocation executes exactly ONE task.

- Manual run: `python -m openclaw.skills.spec_coding` → executes 1 task
- Cron run: Every 15 minutes → executes 1 task per run
- Total: 15 tasks per night (1:00 AM - 4:45 AM, every 15 min)

## Lock File

Autocoder uses `.autocoder.lock` to prevent concurrent runs.

- Created when run starts
- Deleted when run completes
- If older than 20 minutes: considered stale and deleted

If stuck:
```bash
rm .autocoder.lock
```

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

## Files

- `TASKS.md` - Task queue
- `NIGHTLY_LOG.md` - Execution log
- `RUN_STATE.json` - Current state
- `.autocoder.lock` - Runtime lock (auto-managed)

## Full Documentation

See `AUTOCODER_SYSTEM.md` for complete setup and troubleshooting guide.

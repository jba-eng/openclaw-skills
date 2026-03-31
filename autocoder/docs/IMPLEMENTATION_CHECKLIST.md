# Autocoder Implementation Checklist

Use this checklist to ensure all fixes are properly implemented.

## Phase 1: Preparation

- [ ] Read AUTOCODER_README.md
- [ ] Read AUTOCODER_QUICK_START.md
- [ ] Understand the three skills (spec-creation, spec-coding, autocoder)
- [ ] Understand the data files (TASKS.md, NIGHTLY_LOG.md, RUN_STATE.json)

## Phase 2: Copy Skill Files

- [ ] Copy spec-creation/SKILL.md to ~/.openclaw/workspace/skills/spec-creation/
- [ ] Copy spec-coding/SKILL.md to ~/.openclaw/workspace/skills/spec-coding/
- [ ] Copy autocoder/SKILL.md to ~/.openclaw/workspace/skills/autocoder/
- [ ] Verify files exist in user-level directory

## Phase 3: Set Up Cron

- [ ] Choose setup method (automated or manual)
- [ ] If automated: Run `bash CRON_SETUP.sh`
- [ ] If manual: Follow CRON_SETUP_MANUAL.md
- [ ] Verify cron jobs: `crontab -l`
- [ ] Confirm 4 lines for hours 1-4 AM

## Phase 4: Create First Specification

- [ ] Run spec-creation skill: `python -m openclaw.skills.spec_creation`
- [ ] Answer 6 essential questions
- [ ] Review generated spec.md
- [ ] Review generated design.md
- [ ] Review generated TASKS.md
- [ ] Approve and finalize

## Phase 5: Verify Data Files

- [ ] Check TASKS.md exists and has tasks with `[ ]` status
- [ ] Check NIGHTLY_LOG.md exists (empty initially)
- [ ] Check RUN_STATE.json exists with null values
- [ ] Verify .autocoder.lock does NOT exist (runtime only)

## Phase 6: Manual Testing

- [ ] Run spec-coding manually: `python -m openclaw.skills.spec_coding`
- [ ] Verify one task executed
- [ ] Check TASKS.md status updated to `[x]`
- [ ] Check RUN_STATE.json updated
- [ ] Check NIGHTLY_LOG.md has entry (if autocoder called it)

## Phase 7: Verify Lock File Behavior

- [ ] Run autocoder manually: `python -m openclaw.skills.autocoder`
- [ ] Verify .autocoder.lock created during run
- [ ] Verify .autocoder.lock deleted after run
- [ ] Check NIGHTLY_LOG.md has entry

## Phase 8: Test Concurrency Control

- [ ] Manually create .autocoder.lock with recent timestamp
- [ ] Run autocoder: `python -m openclaw.skills.autocoder`
- [ ] Verify it exits immediately (logs "Lock active, skipping")
- [ ] Delete .autocoder.lock
- [ ] Run autocoder again: verify it executes normally

## Phase 9: Test Stale Lock Recovery

- [ ] Manually create .autocoder.lock with old timestamp (>20 min ago)
- [ ] Run autocoder: `python -m openclaw.skills.autocoder`
- [ ] Verify it deletes stale lock and continues
- [ ] Verify task executed normally

## Phase 10: Overnight Execution

- [ ] Wait for overnight cron runs (1:00 AM - 4:45 AM)
- [ ] Or manually trigger multiple runs to simulate overnight

## Phase 11: Morning Review

- [ ] Check RUN_STATE.json: `cat RUN_STATE.json`
  - [ ] last_run is recent
  - [ ] last_task is set
  - [ ] last_status is "done" or "failed"
  - [ ] tasks_completed_tonight > 0
  - [ ] tasks_remaining is accurate

- [ ] Check NIGHTLY_LOG.md: `cat NIGHTLY_LOG.md`
  - [ ] Multiple entries (one per run)
  - [ ] Timestamps are correct
  - [ ] Tasks are listed
  - [ ] Statuses are recorded

- [ ] Check TASKS.md: `cat TASKS.md`
  - [ ] Completed tasks marked `[x]`
  - [ ] Failed tasks marked `[!]` with error notes
  - [ ] Pending tasks marked `[ ]`

## Phase 12: Verify All 5 Fixes

### Fix 1: Task Status Tracking
- [ ] TASKS.md uses checkbox format: `[ ]` `[x]` `[!]`
- [ ] spec-coding updates status before exiting
- [ ] Status persists between runs

### Fix 2: Lock File Guard
- [ ] .autocoder.lock created on startup
- [ ] .autocoder.lock deleted on exit
- [ ] Stale lock detected (>20 min)
- [ ] Concurrent runs prevented

### Fix 3: Cron-Only, No Heartbeat
- [ ] Cron schedule configured (4 lines)
- [ ] Runs only 1:00 AM - 4:45 AM
- [ ] 15-minute intervals
- [ ] No heartbeat mode

### Fix 4: Run Log
- [ ] NIGHTLY_LOG.md created
- [ ] Entries appended after each run
- [ ] Format: [timestamp] task: "..." → status: ... (duration)
- [ ] "Lock active, skipping" entries present
- [ ] "Queue empty" entries present

### Fix 5: Run State
- [ ] RUN_STATE.json created
- [ ] Updated after each task
- [ ] Contains: last_run, last_task, last_status, tasks_completed_tonight, tasks_remaining
- [ ] Allows quick status check

## Phase 13: Troubleshooting

If any checks fail:

- [ ] Check NIGHTLY_LOG.md for error messages
- [ ] Check TASKS.md for failed tasks: `[!] ... (error: ...)`
- [ ] Check cron logs: `sudo tail -f /var/log/syslog | grep CRON`
- [ ] Verify cron is running: `sudo systemctl status cron`
- [ ] Check lock file: `ls -la .autocoder.lock`
- [ ] Manually run skills to test: `python -m openclaw.skills.spec_coding`

## Phase 14: Production Readiness

- [ ] All 5 fixes verified
- [ ] Cron schedule confirmed
- [ ] Manual tests passed
- [ ] Overnight run completed successfully
- [ ] Morning review shows expected results
- [ ] Documentation reviewed and understood
- [ ] Team notified of new system

## Ongoing Monitoring

- [ ] Check RUN_STATE.json each morning
- [ ] Review NIGHTLY_LOG.md for any issues
- [ ] Monitor TASKS.md for failed tasks
- [ ] Retry failed tasks as needed
- [ ] Add new tasks to TASKS.md as needed

## Quick Reference

### Check Status
```bash
cat RUN_STATE.json
```

### View Log
```bash
tail -f NIGHTLY_LOG.md
```

### View Tasks
```bash
cat TASKS.md
```

### Test Manually
```bash
python -m openclaw.skills.spec_coding
```

### Check Cron
```bash
crontab -l
```

### View Cron Logs
```bash
sudo tail -f /var/log/syslog | grep CRON
```

## Success Criteria

All of the following must be true:

1. ✓ Skill files copied to user-level directory
2. ✓ Cron schedule configured (4 lines)
3. ✓ TASKS.md uses checkbox format
4. ✓ spec-coding executes one task per run
5. ✓ spec-coding updates TASKS.md status
6. ✓ autocoder manages lock file
7. ✓ autocoder prevents concurrent runs
8. ✓ autocoder logs to NIGHTLY_LOG.md
9. ✓ autocoder updates RUN_STATE.json
10. ✓ Overnight runs complete successfully
11. ✓ Morning review shows expected results
12. ✓ All 5 fixes verified and working

## Sign-Off

- [ ] All checklist items completed
- [ ] All 5 fixes verified
- [ ] System ready for production
- [ ] Team trained on new system
- [ ] Documentation reviewed

**Date Completed**: _______________

**Completed By**: _______________

**Notes**: 

---

For questions or issues, refer to:
- AUTOCODER_README.md
- AUTOCODER_SYSTEM.md
- AUTOCODER_ARCHITECTURE.md

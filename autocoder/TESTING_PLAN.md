# Autocoder System - Testing Plan

## Overview

Test the complete autocoder system in a controlled, small-scale environment before overnight production runs. All testing done via Telegram on OpenClaw gateway.

## Testing Strategy

### Phase 1: Component Testing (Individual Skills)
Test each skill independently to verify basic functionality.

### Phase 2: Integration Testing (Skills Together)
Test the complete flow from spec creation to task execution.

### Phase 3: Orchestrator Testing (Cron Simulation)
Test the nightly orchestrator without waiting for 1:00 AM.

### Phase 4: Mini Production Run (Controlled)
Run a small-scale version with 1-2 simple tasks.

---

## Phase 1: Component Testing

### Test 1.1: Active-Projects Skill

**Via Telegram**:
```
@kiro Check if Archivera is in active projects list

Expected: Should read workspace/skills/active-projects/active_projects.json
and confirm Archivera is in the array
```

**Verification**:
- File exists at correct location
- JSON is valid
- Archivera is in active_projects array

### Test 1.2: Spec-Creation Skill (Optional)

**Via Telegram**:
```
@kiro Create a test project called "TestAutocoder" in workspace/software-projects/
with minimal specs:
- One requirement: "Print hello world"
- One task: "Create hello.py that prints hello world"
```

**Verification**:
- Creates workspace/software-projects/TestAutocoder/
- Creates specs.md, design.md, tasks.md
- tasks.md has proper format with **Status:** planned

### Test 1.3: Spec-Coding Skill (Manual)

**Via Telegram**:
```
@kiro Read workspace/software-projects/Archivera/tasks.md
and tell me the first task with **Status:** planned
```

**Verification**:
- Can read tasks.md
- Can identify pending tasks
- Understands status field format

---

## Phase 2: Integration Testing

### Test 2.1: File Location Verification

**Via Telegram**:
```
@kiro Verify the autocoder system file locations:
1. Check workspace/skills/active-projects/active_projects.json exists
2. Check workspace/skills/autocoder/scripts/nightly_orchestrator.py exists
3. Check workspace/skills/autocoder/scripts/project_executor.py exists
4. Check workspace/software-projects/Archivera/tasks.md exists
```

**Expected**: All files exist at correct locations

### Test 2.2: Orchestrator Logic Test

**Via Telegram**:
```
@kiro Simulate what the nightly orchestrator would do:
1. Read active_projects.json
2. For each project, check if tasks.md has pending tasks
3. Report which projects would run tonight
```

**Expected**: Should identify Archivera (or TestAutocoder) as having pending tasks

### Test 2.3: Task Detection Test

**Via Telegram**:
```
@kiro Check workspace/software-projects/Archivera/tasks.md
and count how many tasks have:
- **Status:** planned
- **Status:** in-progress
- **Status:** done
- **Status:** failed
```

**Expected**: Accurate count of tasks by status

---

## Phase 3: Orchestrator Testing

### Test 3.1: Manual Orchestrator Run

**Via Telegram**:
```
@kiro Run the nightly orchestrator manually:
cd workspace
python skills/autocoder/scripts/nightly_orchestrator.py

Show me the output
```

**Expected Output**:
```
[2026-03-27 XX:XX:XX] === Nightly Orchestrator Started ===
[2026-03-27 XX:XX:XX] Found 1 active project(s): Archivera
[2026-03-27 XX:XX:XX] Checking Archivera for pending tasks...
[2026-03-27 XX:XX:XX] ✓ Archivera has pending tasks
[2026-03-27 XX:XX:XX] Spawning executors for 1 project(s)...
[2026-03-27 XX:XX:XX] Spawning executor for Archivera: ...
[2026-03-27 XX:XX:XX] === Nightly Orchestrator Complete ===
```

**Verification**:
- No errors
- Detects Archivera
- Identifies pending tasks
- Attempts to spawn executor

### Test 3.2: Executor Dry Run (Without Actual Execution)

**Via Telegram**:
```
@kiro Check if project_executor.py can be imported and its functions work:
cd workspace
python -c "
from skills.autocoder.scripts.project_executor import check_pending_tasks
from pathlib import Path
result = check_pending_tasks(Path('software-projects/Archivera'))
print(f'Has pending tasks: {result}')
"
```

**Expected**: Should return True if Archivera has pending tasks

---

## Phase 4: Mini Production Run

### Test 4.1: Create Minimal Test Project

**Via Telegram**:
```
@kiro Create a minimal test project:

Project: TestAutocoder
Location: workspace/software-projects/TestAutocoder/

specs.md:
- Requirement: Create a hello world script

design.md:
- Component: hello.py - prints "Hello from Autocoder!"

tasks.md:
### T1: Create hello.py
**Status:** planned
**Dependencies:** None
**Done When:**
1. File hello.py exists
2. Prints "Hello from Autocoder!"
3. Can be run with: python hello.py

Then add TestAutocoder to active_projects.json
```

**Verification**:
- Project created
- All files in correct format
- Added to active projects

### Test 4.2: Manual Task Execution

**Via Telegram**:
```
@kiro Execute the first task from TestAutocoder manually:
1. Read workspace/software-projects/TestAutocoder/tasks.md
2. Find the first task with **Status:** planned
3. Create the hello.py file as specified
4. Update the task status to **Status:** done
5. Show me the updated tasks.md
```

**Expected**:
- Task executed
- hello.py created
- tasks.md updated with **Status:** done

### Test 4.3: Verify Task Execution

**Via Telegram**:
```
@kiro Verify the task was completed:
1. Check workspace/software-projects/TestAutocoder/hello.py exists
2. Run: python workspace/software-projects/TestAutocoder/hello.py
3. Check tasks.md shows **Status:** done
```

**Expected**: hello.py runs and prints "Hello from Autocoder!"

---

## Phase 5: Cron Job Testing

### Test 5.1: Verify Cron Job Configuration

**Via Telegram**:
```
@kiro Check the cron job configuration:
1. Read cron/jobs.json
2. Find the "autocoder-nightly-orchestrator" job
3. Verify it's enabled
4. Verify the schedule is "0 1 * * *"
5. Verify the command points to nightly_orchestrator.py
```

**Expected**: Job configured correctly

### Test 5.2: Simulate Cron Trigger (Daytime)

**Via Telegram**:
```
@kiro Simulate a cron trigger by running the orchestrator command:
cd Y:\home\jonathan\.openclaw\workspace && python skills/autocoder/scripts/nightly_orchestrator.py

Show me the output and any errors
```

**Expected**: Runs successfully, identifies projects with work

### Test 5.3: Check State Files

**Via Telegram**:
```
@kiro After the orchestrator run, check:
1. workspace/skills/active-projects/RUN_STATE.json
2. workspace/software-projects/TestAutocoder/.run_state.json (if created)
3. workspace/software-projects/TestAutocoder/.nightly_log.md (if created)

Show me the contents
```

**Expected**: State files created/updated with run information

---

## Phase 6: End-to-End Test

### Test 6.1: Complete Flow Test

**Via Telegram**:
```
@kiro Run a complete end-to-end test:

1. Create a new test project "E2ETest" with 2 simple tasks:
   - T1: Create file1.txt with "Task 1 complete"
   - T2: Create file2.txt with "Task 2 complete"

2. Add E2ETest to active_projects.json

3. Run the orchestrator manually

4. Check if tasks were executed

5. Show me the results
```

**Expected**:
- Project created
- Added to active projects
- Orchestrator runs
- Tasks executed (or attempted)
- State files updated

---

## Testing Checklist

### Pre-Test Verification
- [ ] All three SKILL.md files updated (autocoder, spec-creation, spec-coding)
- [ ] Cron job configured in cron/jobs.json
- [ ] active-projects skill has active_projects.json
- [ ] Archivera exists in software-projects/
- [ ] Archivera has tasks.md with proper format

### Phase 1: Component Testing
- [ ] Test 1.1: Active-projects skill works
- [ ] Test 1.2: Spec-creation skill works (optional)
- [ ] Test 1.3: Spec-coding skill can read tasks

### Phase 2: Integration Testing
- [ ] Test 2.1: File locations verified
- [ ] Test 2.2: Orchestrator logic works
- [ ] Test 2.3: Task detection works

### Phase 3: Orchestrator Testing
- [ ] Test 3.1: Manual orchestrator run succeeds
- [ ] Test 3.2: Executor functions work

### Phase 4: Mini Production Run
- [ ] Test 4.1: Test project created
- [ ] Test 4.2: Manual task execution works
- [ ] Test 4.3: Task verification passes

### Phase 5: Cron Job Testing
- [ ] Test 5.1: Cron job configured correctly
- [ ] Test 5.2: Cron simulation works
- [ ] Test 5.3: State files created

### Phase 6: End-to-End Test
- [ ] Test 6.1: Complete flow works

---

## Success Criteria

### Minimum Viable Test (MVT)
- Orchestrator runs without errors
- Detects active projects correctly
- Identifies pending tasks correctly
- Can spawn executor (even if execution fails)

### Full Success
- Complete end-to-end flow works
- Tasks executed successfully
- State files updated correctly
- Logs created properly
- Ready for overnight production run

---

## Rollback Plan

If testing reveals issues:

1. **Disable cron job**:
   ```
   @kiro Edit cron/jobs.json and set "enabled": false for autocoder job
   ```

2. **Fix issues** based on test results

3. **Re-test** starting from failed phase

4. **Re-enable** when all tests pass

---

## Production Readiness

After all tests pass:

1. **Enable cron job** (if disabled)
2. **Verify active projects** list is correct
3. **Check Archivera** has pending tasks
4. **Wait for 1:00 AM** or manually trigger for first production run
5. **Check results** in morning

---

## Telegram Testing Commands Summary

### Quick Test Sequence (Copy-paste to Telegram)

```
@kiro Test autocoder system:

1. Verify files exist:
   - workspace/skills/active-projects/active_projects.json
   - workspace/skills/autocoder/scripts/nightly_orchestrator.py
   - workspace/software-projects/Archivera/tasks.md

2. Check active projects:
   cat workspace/skills/active-projects/active_projects.json

3. Check Archivera tasks:
   grep "**Status:**" workspace/software-projects/Archivera/tasks.md

4. Run orchestrator:
   cd workspace && python skills/autocoder/scripts/nightly_orchestrator.py

5. Show results
```

### Minimal Test (Fastest)

```
@kiro Quick autocoder test:
cd workspace && python skills/autocoder/scripts/nightly_orchestrator.py
Show me the output
```

---

## Notes

- All testing via Telegram to OpenClaw gateway
- No need to wait for 1:00 AM - test manually anytime
- Start with minimal tests, expand if successful
- Each test should take 1-5 minutes
- Can stop at any phase if issues found
- Document any errors for debugging

## Next Steps After Testing

1. Review test results
2. Fix any issues found
3. Update documentation if needed
4. Enable cron job for production
5. Monitor first overnight run
6. Iterate based on results

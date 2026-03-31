# Autocoder System - File Locations

## Quick Answer

**RUN_STATE.json is located in the project root**: `./RUN_STATE.json`

All autocoder data files are in the **project root** (same directory as spec.md and design.md).

---

## Complete File Location Map

### Project Root (Same directory as spec.md and design.md)

```
project-root/
├── spec.md                    (Requirements)
├── design.md                  (Architecture)
├── TASKS.md                   (Task queue)
├── NIGHTLY_LOG.md             (Execution log)
├── RUN_STATE.json             (Current state) ← YOU ARE HERE
├── .autocoder.lock            (Runtime lock - auto-managed)
├── src/                       (Implementation)
│   └── ...
├── tests/                     (Tests)
│   └── ...
└── [other project files]
```

### Skill Files (User-level directory)

```
~/.openclaw/workspace/skills/
├── spec-creation/
│   └── SKILL.md
├── spec-coding/
│   └── SKILL.md
└── autocoder/
    └── SKILL.md
```

### Workspace Documentation (For reference only)

```
workspace/
├── skills/
│   ├── spec-creation/SKILL.md
│   ├── spec-coding/SKILL.md
│   └── autocoder/SKILL.md
├── TASKS.md (template)
├── NIGHTLY_LOG.md (template)
├── RUN_STATE.json (template)
├── AUTOCODER_README.md
├── AUTOCODER_QUICK_START.md
├── AUTOCODER_SYSTEM.md
├── AUTOCODER_ARCHITECTURE.md
├── AUTOCODER_CHANGES_SUMMARY.md
├── AUTOCODER_FILES_CREATED.md
├── CRON_SETUP_MANUAL.md
├── CRON_SETUP.sh
├── IMPLEMENTATION_CHECKLIST.md
├── COMPLETION_SUMMARY.md
├── QUICK_REFERENCE.md
├── INDEX.md
├── FILE_LOCATIONS.md (this file)
└── [other documentation]
```

---

## Data Files Explained

### TASKS.md
- **Location**: `./TASKS.md` (project root)
- **Purpose**: Task queue with status
- **Format**: Markdown with checkbox format
- **Updated by**: spec-coding skill
- **Read by**: autocoder and spec-coding skills
- **Example**:
  ```markdown
  - [ ] T1: Build login endpoint
  - [x] T2: Add password validation
  - [!] T3: Create database (error: timeout)
  ```

### RUN_STATE.json
- **Location**: `./RUN_STATE.json` (project root)
- **Purpose**: Current execution state
- **Format**: JSON
- **Updated by**: autocoder skill (after each task)
- **Read by**: You (for morning review)
- **Example**:
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
- **Location**: `./NIGHTLY_LOG.md` (project root)
- **Purpose**: Execution log (append-only)
- **Format**: Markdown with one-line entries
- **Updated by**: autocoder skill (after each run)
- **Read by**: You (for detailed review)
- **Example**:
  ```markdown
  [2026-03-27 01:15] task: "Build login endpoint" → status: done (12m 3s)
  [2026-03-27 01:30] task: "Add password validation" → status: done (8m 15s)
  [2026-03-27 01:45] Lock file active, skipping run
  ```

### .autocoder.lock
- **Location**: `./.autocoder.lock` (project root)
- **Purpose**: Runtime lock file (prevents concurrent runs)
- **Format**: Plain text with ISO timestamp
- **Created by**: autocoder skill (on startup)
- **Deleted by**: autocoder skill (on exit)
- **Example**:
  ```
  2026-03-27T01:15:00Z
  ```
- **Note**: Should NOT exist between runs. If it does, it's either:
  - A run is currently active
  - A run crashed (stale if >20 minutes old)

---

## Directory Structure

### Before Setup
```
project-root/
├── spec.md
├── design.md
└── src/
```

### After Setup
```
project-root/
├── spec.md
├── design.md
├── TASKS.md                   ← Created by spec-creation
├── NIGHTLY_LOG.md             ← Created by autocoder
├── RUN_STATE.json             ← Created by autocoder
├── .autocoder.lock            ← Created/deleted by autocoder (runtime)
├── src/
└── tests/
```

---

## File Access Patterns

### Cron Job (autocoder)
```bash
cd /path/to/project
python -m openclaw.skills.autocoder

# Reads:
#   - ./TASKS.md
#   - ./.autocoder.lock (if exists)

# Writes:
#   - ./.autocoder.lock (create/delete)
#   - ./RUN_STATE.json (update)
#   - ./NIGHTLY_LOG.md (append)
#   - Calls spec-coding which updates ./TASKS.md
```

### Manual Test (spec-coding)
```bash
cd /path/to/project
python -m openclaw.skills.spec_coding

# Reads:
#   - ./TASKS.md
#   - ./spec.md
#   - ./design.md

# Writes:
#   - ./TASKS.md (update status)
#   - ./src/* (implementation)
#   - ./tests/* (tests)
```

### Morning Review (You)
```bash
cd /path/to/project

# Check status
cat RUN_STATE.json

# View log
cat NIGHTLY_LOG.md

# View tasks
cat TASKS.md
```

---

## Relative vs Absolute Paths

### In Cron Jobs
Use absolute path or cd first:
```bash
# Option 1: Absolute path
0,15,30,45 1 * * * cd /home/user/my-project && python -m openclaw.skills.autocoder

# Option 2: With absolute path in script
0,15,30,45 1 * * * /home/user/my-project/run-autocoder.sh
```

### In Python Scripts
Use relative paths (from project root):
```python
# Read TASKS.md
with open('./TASKS.md', 'r') as f:
    tasks = f.read()

# Read RUN_STATE.json
import json
with open('./RUN_STATE.json', 'r') as f:
    state = json.load(f)

# Write RUN_STATE.json
with open('./RUN_STATE.json', 'w') as f:
    json.dump(state, f)
```

---

## Verification

### Check File Locations
```bash
cd /path/to/project

# List all autocoder files
ls -la TASKS.md NIGHTLY_LOG.md RUN_STATE.json .autocoder.lock 2>/dev/null

# Expected output (after first run):
# -rw-r--r-- 1 user group  500 Mar 27 01:15 TASKS.md
# -rw-r--r-- 1 user group  200 Mar 27 01:15 NIGHTLY_LOG.md
# -rw-r--r-- 1 user group  300 Mar 27 01:15 RUN_STATE.json
# (no .autocoder.lock between runs)
```

### Check File Permissions
```bash
# Files should be readable/writable by the user running cron
chmod 644 TASKS.md NIGHTLY_LOG.md RUN_STATE.json
```

### Check File Ownership
```bash
# Files should be owned by the user running cron
chown $USER:$USER TASKS.md NIGHTLY_LOG.md RUN_STATE.json
```

---

## Troubleshooting

### "RUN_STATE.json not found"
- Check: Is it in the project root? `ls -la ./RUN_STATE.json`
- Fix: Create it with: `cat > RUN_STATE.json << 'EOF'`
  ```json
  {
    "last_run": null,
    "last_task": null,
    "last_status": null,
    "tasks_completed_tonight": 0,
    "tasks_remaining": 0
  }
  EOF
  ```

### "Permission denied" when writing
- Check: File permissions: `ls -la RUN_STATE.json`
- Fix: Make writable: `chmod 644 RUN_STATE.json`

### ".autocoder.lock stuck"
- Check: Is it older than 20 minutes? `stat .autocoder.lock`
- Fix: Delete it: `rm .autocoder.lock`

### "Cron can't find files"
- Check: Is cron running from correct directory?
- Fix: Use absolute path in cron: `cd /absolute/path/to/project && python -m ...`

---

## Summary

| File | Location | Purpose | Created By | Updated By |
|------|----------|---------|-----------|-----------|
| TASKS.md | `./TASKS.md` | Task queue | spec-creation | spec-coding |
| RUN_STATE.json | `./RUN_STATE.json` | Current state | autocoder | autocoder |
| NIGHTLY_LOG.md | `./NIGHTLY_LOG.md` | Execution log | autocoder | autocoder |
| .autocoder.lock | `./.autocoder.lock` | Runtime lock | autocoder | autocoder |

**All files are in the project root** (same directory as spec.md and design.md).

---

**Answer to your question**: RUN_STATE.json is located at `./RUN_STATE.json` in the project root.

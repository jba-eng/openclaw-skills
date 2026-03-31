# Autocoder System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOCODER SYSTEM                             │
│                                                                 │
│  Three Skills + Cron + State Files = Autonomous Overnight Code │
└─────────────────────────────────────────────────────────────────┘
```

## Three Skills

```
┌──────────────────┐
│ spec-creation    │  (One-time)
│                  │  Creates specifications
│ Input:  User idea│
│ Output: spec.md  │
│         design.md│
│         TASKS.md │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ spec-coding      │  (Per task)
│                  │  Executes ONE task
│ Input:  TASKS.md │
│ Output: Code     │
│         Updated  │
│         TASKS.md │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ autocoder        │  (Orchestrator)
│                  │  Manages execution
│ Input:  TASKS.md │
│ Output: Logs     │
│         State    │
└──────────────────┘
```

## Execution Flow

### One Complete Cycle (15 minutes)

```
Cron fires at 1:00 AM
         │
         ▼
    ┌─────────────────────────────────────┐
    │ autocoder starts                    │
    └─────────────────────────────────────┘
         │
         ├─ Check .autocoder.lock
         │  ├─ If exists & recent → exit (skip)
         │  ├─ If exists & stale → delete & continue
         │  └─ If not exists → continue
         │
         ├─ Create .autocoder.lock
         │
         ├─ Read TASKS.md
         │  └─ Find first [ ] or [!] task
         │
         ├─ Call spec-coding skill
         │  │
         │  ├─ Mark task as [~] (in_progress)
         │  ├─ Read spec.md + design.md
         │  ├─ Implement code
         │  ├─ Validate done_when
         │  ├─ Run tests
         │  └─ Mark task as [x] or [!]
         │
         ├─ Update RUN_STATE.json
         │
         ├─ Append to NIGHTLY_LOG.md
         │
         ├─ Delete .autocoder.lock
         │
         └─ Exit
```

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      TASKS.md                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ - [ ] T1: Build login endpoint                         │  │
│  │ - [ ] T2: Add password validation                      │  │
│  │ - [ ] T3: Create database                              │  │
│  │ - [ ] T4: Write tests                                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Status: [ ] pending, [~] in_progress, [x] done, [!] failed  │
└──────────────────────────────────────────────────────────────┘
         │
         ├─ Read by autocoder
         │
         ├─ Pass to spec-coding
         │
         └─ Updated by spec-coding
            (status changed)

┌──────────────────────────────────────────────────────────────┐
│                   RUN_STATE.json                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ {                                                      │  │
│  │   "last_run": "2026-03-27T01:15:00Z",                 │  │
│  │   "last_task": "Build login endpoint",                │  │
│  │   "last_status": "done",                              │  │
│  │   "tasks_completed_tonight": 3,                       │  │
│  │   "tasks_remaining": 8                                │  │
│  │ }                                                      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Updated after each task execution                           │
│  Allows quick status check in the morning                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   NIGHTLY_LOG.md                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [2026-03-27 01:15] task: "Build login" → done (12m)   │  │
│  │ [2026-03-27 01:30] task: "Add password" → done (8m)   │  │
│  │ [2026-03-27 01:45] Lock active, skipping              │  │
│  │ [2026-03-27 02:00] task: "Create DB" → failed (err)   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Append-only log of all runs                                 │
│  One line per invocation                                     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                  .autocoder.lock                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 2026-03-27T01:15:00Z                                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Runtime lock file (created/deleted by autocoder)            │
│  Prevents concurrent runs                                    │
│  Stale if older than 20 minutes                              │
└──────────────────────────────────────────────────────────────┘
```

## Cron Schedule

```
Time     │ 1:00 AM │ 1:15 AM │ 1:30 AM │ 1:45 AM │ 2:00 AM │ ...
─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────
Cron     │    ✓    │    ✓    │    ✓    │    ✓    │    ✓    │ ...
─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────
Task     │   T1    │   T2    │   T3    │   T4    │   T5    │ ...
─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────
Status   │  [x]    │  [x]    │  [x]    │  [x]    │  [x]    │ ...

Total: 16 runs per night (1:00 AM - 4:45 AM, every 15 min)
```

## Lock File Behavior

### Normal Case (Task completes in <15 min)

```
1:00 AM
  ├─ Create .autocoder.lock
  ├─ Execute task (5 min)
  ├─ Delete .autocoder.lock
  └─ Exit

1:15 AM
  ├─ Check .autocoder.lock (not found)
  ├─ Create .autocoder.lock
  ├─ Execute task (5 min)
  ├─ Delete .autocoder.lock
  └─ Exit
```

### Slow Task (Takes >15 min)

```
1:00 AM
  ├─ Create .autocoder.lock (timestamp: 1:00 AM)
  ├─ Execute task (20 min)
  │
  1:15 AM (cron fires)
  │  ├─ Check .autocoder.lock (found)
  │  ├─ Check age: 15 min (recent)
  │  ├─ Log "Lock active, skipping"
  │  └─ Exit
  │
  1:20 AM
  ├─ Task completes
  ├─ Delete .autocoder.lock
  └─ Exit

1:30 AM
  ├─ Check .autocoder.lock (not found)
  ├─ Create .autocoder.lock
  ├─ Execute task (5 min)
  ├─ Delete .autocoder.lock
  └─ Exit
```

### Crash Recovery (Stale Lock)

```
1:00 AM
  ├─ Create .autocoder.lock (timestamp: 1:00 AM)
  ├─ Execute task
  ├─ Process crashes (lock remains)
  └─ Exit

1:15 AM
  ├─ Check .autocoder.lock (found)
  ├─ Check age: 15 min (recent)
  ├─ Log "Lock active, skipping"
  └─ Exit

1:30 AM
  ├─ Check .autocoder.lock (found)
  ├─ Check age: 30 min (STALE, >20 min)
  ├─ Delete .autocoder.lock
  ├─ Create new .autocoder.lock
  ├─ Execute task (5 min)
  ├─ Delete .autocoder.lock
  └─ Exit
```

## State Transitions

### Task Status Lifecycle

```
         ┌─────────────────────────────────────────┐
         │                                         │
         ▼                                         │
    ┌─────────┐                                   │
    │ [ ]     │  (pending)                        │
    │ pending │                                   │
    └────┬────┘                                   │
         │                                        │
         │ spec-coding starts                     │
         ▼                                        │
    ┌─────────┐                                   │
    │ [~]     │  (in_progress)                    │
    │ running │                                   │
    └────┬────┘                                   │
         │                                        │
         ├─ All done_when pass ──┐                │
         │                       ▼                │
         │                  ┌─────────┐           │
         │                  │ [x]     │           │
         │                  │ done    │           │
         │                  └─────────┘           │
         │                                        │
         └─ done_when fail or error ──┐           │
                                      ▼           │
                                 ┌─────────┐      │
                                 │ [!]     │      │
                                 │ failed  │      │
                                 └────┬────┘      │
                                      │           │
                                      │ Retry     │
                                      └───────────┘
```

## File Locations

```
Project Root
├── spec.md                    (Requirements)
├── design.md                  (Architecture)
├── TASKS.md                   (Task queue)
├── NIGHTLY_LOG.md             (Execution log)
├── RUN_STATE.json             (Current state)
├── .autocoder.lock            (Runtime lock)
├── src/                       (Implementation)
│   └── ...
├── tests/                     (Tests)
│   └── ...
└── workspace/
    └── skills/
        ├── spec-creation/
        │   └── SKILL.md
        ├── spec-coding/
        │   └── SKILL.md
        └── autocoder/
            └── SKILL.md
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    System Cron                              │
│  (Runs every 15 min from 1:00 AM to 4:45 AM)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ autocoder SKILL        │
        │ (Orchestrator)         │
        └────────────┬───────────┘
                     │
                     ├─ Reads: TASKS.md
                     ├─ Manages: .autocoder.lock
                     ├─ Calls: spec-coding SKILL
                     ├─ Updates: RUN_STATE.json
                     └─ Appends: NIGHTLY_LOG.md
                     │
                     ▼
        ┌────────────────────────┐
        │ spec-coding SKILL      │
        │ (Implementation)       │
        └────────────┬───────────┘
                     │
                     ├─ Reads: spec.md, design.md, TASKS.md
                     ├─ Executes: ONE task
                     ├─ Creates: src/*, tests/*
                     └─ Updates: TASKS.md (status)
```

## Performance Characteristics

```
Typical Task Execution Time: 5-15 minutes
Cron Interval: 15 minutes
Lock Timeout: 20 minutes
Overnight Window: 1:00 AM - 4:45 AM (3 hours 45 minutes)
Total Runs Per Night: 16
Tasks Per Night: 16 (one per run)
```

## Error Handling

```
Task Execution
    │
    ├─ Success
    │  └─ Mark as [x] (done)
    │
    └─ Failure
       ├─ Mark as [!] (failed)
       ├─ Log error message
       ├─ Continue to next run
       └─ Can retry by changing status to [ ]
```

## Monitoring

```
Morning Review
    │
    ├─ Quick check: cat RUN_STATE.json
    │  └─ See: last_run, last_task, tasks_completed_tonight
    │
    ├─ Detailed log: cat NIGHTLY_LOG.md
    │  └─ See: timestamp, task, status, duration
    │
    └─ Task status: cat TASKS.md
       └─ See: [x] done, [!] failed, [ ] pending
```

---

This architecture ensures:
- **State persistence** across runs
- **Concurrency control** via lock file
- **Crash recovery** via stale lock detection
- **Visibility** via logs and state files
- **Reliability** via one-task-per-run discipline

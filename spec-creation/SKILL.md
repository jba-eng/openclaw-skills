---
name: Spec Creation
slug: spec-creation
version: 2.0.0
description: Create comprehensive software specifications with automated discovery, validation, and structured 6-stage workflow. Creates specs.md, design.md, tasks.md in project folder.
metadata: {"requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}
---

## When to Use

User wants to create or update software specifications (specs.md, design.md, tasks.md) for a project in `workspace/software-projects/`.

## File Locations

**Important**: All files are created IN the project folder:

```
workspace/software-projects/{PROJECT}/
├── specs.md          ← Requirements (created by this skill)
├── design.md         ← Architecture (created by this skill)
├── tasks.md          ← Task queue (created by this skill)
├── src/
└── tests/
```

NOT in workspace root!

## Python Utilities (Token Efficient)

Use these instead of manual bash commands:

```bash
# Project discovery (saves ~250 tokens)
python scripts/project_discovery.py full "{PROJECT_NAME}"

# Validate specs (saves ~200 tokens)
python scripts/spec_validator.py .specifications/*.md

# Generate from template (saves ~400 tokens)
echo '{json_data}' | python scripts/spec_generator.py spec

# Compare versions (saves ~150 tokens)
python scripts/spec_diff.py old.md new.md
```

## Workflow (6 Stages)

### 1. PROJECT DISCOVERY
Use Python utility:
```bash
python scripts/project_discovery.py full "{USER_PROJECT}"
```

Output shows: match type, project path, existing specs. If ambiguous, ask user to choose from alternatives.

### 2. CHECK EXISTING SPECS
Based on discovery output:
- If spec.md exists: "Found existing spec.md. Update or start fresh?"
- If partial specs: "Found design.md/tasks.md. Resume from where?"
- Else: "No specs found. Creating new."

### 3. ASK 6 ESSENTIAL QUESTIONS
Get detailed answers:
1. **Core problem**: What failed? What was the impact?
2. **Primary users**: Roles/titles? Location? Devices?
3. **Perfect success**: Ideal outcome? Steps/seconds/results?
4. **Key data**: What must be captured/searched/stored? Examples?
5. **Tech stack**: Language/framework/DB? Local/cloud/offline?
6. **8-week MVP**: ONE killer feature that proves value?

### 4. CREATE spec.md
Use template from `templates/spec_template.md`. Show full content before writing.

Structure:
- Context (from Q1)
- Users (from Q2)
- Requirements (R1, R2, R3...)
- Acceptance Criteria (2-3 ACs per requirement)
- Edge cases, error handling, performance targets

### 5. USER APPROVAL
Show full spec.md. Get approval or iterate on changes.

### 6. CREATE design.md + tasks.md
Use templates. Show before writing.

**design.md**: Components, data flow, interfaces

**tasks.md**: T1, T2, T3... with status, dependencies, done_when

**Task format** (for use with autocoder):
```markdown
### T1: Project Structure & Dependencies
**Status:** planned
**Dependencies:** None
**Done When:**
1. Project directory structure created
2. requirements.txt with all dependencies
3. config.yaml template created

### T2: PDF Parser Implementation
**Status:** planned
**Dependencies:** T1
**Done When:**
1. PDF text extraction working
2. Metadata extraction working
3. Tests passing
```

**Status values**: `planned`, `in-progress`, `blocked`, `done`, `failed`

### 7. VALIDATE & FINALIZE
```bash
python scripts/spec_validator.py .specifications/*.md
```

Show validation results. Get final approval.

### 8. OFFER NEXT STEP
After successful completion, ask:

"Specs complete! Ready to start implementation?
- Type 'yes' to activate spec-coding skill
- Type 'no' to finish here"

If yes, activate spec-coding skill for task execution.

## Core Rules

1. **Always use Python utilities** - Saves 30-40% tokens per session
2. **Never skip discovery** - Always verify project exists and check for existing specs
3. **Get detailed answers** - The 6 questions need comprehensive responses, not one-liners
4. **Show before writing** - Display full file content before creating/updating
5. **Validate quality** - Every requirement needs 2-3 testable acceptance criteria
6. **User approval required** - At spec.md stage and final stage
7. **Comprehensive specs** - 300-800 lines is normal and expected
8. **Task status format** - Use checkbox format: `[ ]` pending, `[x]` done, `[!]` failed

## Data Storage

Creates files in: `workspace/software-projects/{PROJECT}/`
- specs.md
- design.md
- tasks.md

Always ask user before creating or modifying files.

## Integration with Autocoder

After creating specifications:
1. Add project to active-projects skill
2. Autocoder will pick it up at 1:00 AM
3. Tasks will be executed overnight

## Related Skills

- **spec-coding**: Execute tasks from tasks.md (next step after spec creation)
- **autocoder**: Overnight orchestrator that drives spec-coding via cron jobs
- **active-projects**: Add project to active list for overnight execution

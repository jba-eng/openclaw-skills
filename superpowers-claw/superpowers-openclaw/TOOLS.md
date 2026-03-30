# TOOLS.md — Tool Setup & Spec Workflow

> Defines how I use tools, spec creation workflow, and process enforcement.

---

## OpenClaw Environment

**Gateway:** ws://127.0.0.1:18789
**Config:** ~/.openclaw/openclaw.json
**Workspace:** ~/.openclaw/workspace/agents/superpowers-dev/
**Logs:** `openclaw logs --follow`

**Key capabilities:**
- File operations (read, write, edit)
- Shell command execution
- Telegram messaging for user communication
- Subagent dispatch via @mention
- Todo tracking with todowrite

---

## Tool Philosophy

Tools are enforcers of process. I don't just use tools — I use them to ensure discipline. Every tool has a purpose: keep me honest, track progress, verify work.

---

## Core Tools

### todowrite

**Purpose:** Track task progress and checklists

**Usage:**
- Create todo for each skill checklist item
- Update as items complete
- Show active todos when asked

**When Required:**
- Every skill with a checklist
- Any multi-step task
- Tracking implementation progress

### @mention (subagent dispatch)

**Purpose:** Dispatch independent subagents for parallel work

**Usage:**
```
@agent-name "Task description with clear scope and expected output"
```

**When Required:**
- Dispatching parallel agents (dispatching-parallel-agents skill)
- Subagent-driven development (one agent per task)
- Independent work that doesn't need shared context

**Best practices:**
- Give each agent focused scope
- Include all context needed
- Specify expected output format
- Don't share state between agents

### telegram

**Purpose:** Communicate with user

**Usage:**
- Send status updates
- Ask clarifying questions
- Request approvals
- Report completion

**When Required:**
- User approval needed (after spec.md, before implementation)
- Clarifying questions during brainstorming
- Status updates for long-running tasks
- Error reporting

### skill (deprecated - use direct file reading)

**Purpose:** Load and invoke skills

**Usage:**
```bash
# Read skill file directly
cat ~/.openclaw/workspace/agents/superpowers-dev/skills/[skill-name]/SKILL.md

# Or use readFile
readFile ~/.openclaw/workspace/agents/superpowers-dev/skills/[skill-name]/SKILL.md
```

**When Required:**
- Before ANY response, check if skill applies
- Even 1% probability means load and verify

### readFile / readCode

**Purpose:** Read files and understand code

**Usage:**
- readFile for full file content
- readCode for code analysis (AST-based, if available)

**When Required:**
- Exploring project context
- Understanding existing patterns
- Before making changes
- Loading skill files

### writeFile / editFile

**Purpose:** Modify files

**Usage:**
- writeFile for new files or complete rewrites
- editFile for targeted edits (if available)
- For complex refactoring, consider manual edits

**When Required:**
- Implementing features
- Writing tests
- Creating documentation

### shell

**Purpose:** Execute shell commands

**Usage:**
- Run tests
- Run linters
- Git operations

**When Required:**
- Verification (always show output)
- Running test suites
- Git operations

---

## Spec Creation Workflow

Every feature follows this path:

```
BRAINSTORM (spec.md + design.md) → PLAN (implementation tasks) → CODE → TESTS → VERIFY → COMMIT
```

### Step 1: Brainstorming (brainstorming skill)

Before any code:
1. Explore project context
2. Ask 6 essential questions (What, Why, Who, How, When, What else)
3. Propose 2-3 approaches with trade-offs
4. Present design, get user approval
5. writeFile spec.md to `docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.md`
6. writeFile design.md to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`

### Step 2: Planning (writing-plans skill)

After design approved:
1. Create implementation plan
2. Break into 2-5 minute tasks with dependencies
3. Include exact file paths, code snippets, done_when conditions
4. Save to `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`

### Step 3: Execute (executing-plans or subagent-driven-development)

Choose execution mode:
- **Inline:** Execute tasks in this session with checkpoints
- **Subagent:** Dispatch fresh subagent per task with two-stage review

### Step 4: Verify (verification-before-completion)

Before claiming done:
- Run all tests, show output
- Run linter, show output
- Run type checker, show output
- Show manual testing results

### Step 5: Commit

After verification:
- Atomic commits per task
- Descriptive messages
- Push to remote

---

## TDD Enforcement (test-driven-development skill)

**The Cycle:**
1. **RED** — writeFile failing test first
2. **GREEN** — Write minimal code to pass
3. **REFACTOR** — Clean up, keep tests passing

**Rules:**
- NEVER write implementation code before test
- NEVER skip the "failing test" step
- If you write code before a test, DELETE IT and start over
- Run tests after EVERY change

---

## Debugging Workflow (systematic-debugging skill)

**The 4 Phases:**

### Phase 1: Gather Evidence
- Read error completely
- Check logs, stack traces
- Reproduce consistently
- Document what's different

### Phase 2: Form Hypothesis
- What could cause this?
- What's most likely?
- What would confirm/reject?

### Phase 3: Test Hypothesis
- Change ONE thing at a time
- Run test after each change
- Record results

### Phase 4: Implement Fix
- Fix root cause, not symptoms
- writeFile regression test
- Verify fix works
- Commit

**Rules:**
- NEVER guess without evidence
- NEVER change multiple things at once
- NEVER skip reproduction

---

## Code Review Workflow

### Requesting (requesting-code-review skill)

Before PR:
- [ ] All tests pass locally
- [ ] Code follows style
- [ ] No debug code left
- [ ] Commit history clean
- [ ] PR description complete

### Receiving (receiving-code-review skill)

When reviewed:
- readFile all comments first
- Categorize: must fix / should fix / nice to have / discuss
- Address each one
- Never ignore
- Re-request review after changes

---

## Verification Checklist

Before claiming ANY task complete:

- [ ] Tests run and pass (SHOW OUTPUT)
- [ ] Linter passes (SHOW OUTPUT)
- [ ] Types check (SHOW OUTPUT)
- [ ] Manual testing done (SHOW WHAT)

**Never say "done" without proof.**

---

## Git Workflow (using-git-worktrees skill)

For each new piece of work:
1. Create worktree: `git worktree add -b feature/name ../project-feature main`
2. Verify clean baseline: run tests, ensure pass
3. Work in worktree
4. Commit frequently
5. When done: merge, PR, or decide what to do with branch
6. Clean up worktree

---

## Process Enforcement

These are NON-OPTIONAL:

1. **Skill check before EVERY response**
2. **Design before implementation**
3. **Plan before code**
4. **Test before implementation (TDD)**
5. **Verify before completion**
6. **Show output, don't just claim**

The only exception: **User instructions explicitly say otherwise.**
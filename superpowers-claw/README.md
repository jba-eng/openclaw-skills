# Superpowers for OpenClaw

A token-efficient skill system for OpenClaw that enforces proven development workflows.

---

## What Is This?

Superpowers for OpenClaw is a collection of skills that enforce disciplined development practices:

- **Spec-first development** — Design before code
- **Test-driven development** — RED → GREEN → REFACTOR
- **Systematic debugging** — Evidence-based problem solving
- **Code review workflows** — Pre and post review checklists
- **Parallel agent dispatching** — Handle multiple independent problems concurrently

---

## Quick Start

1. Copy the `superpowers-openclaw` folder to your OpenClaw workspace
2. Load `AGENTS.md` at session start
3. The agent will automatically check for applicable skills before responding

---

## File Structure

```
superpowers-openclaw/
├── AGENTS.md          # Core config - mission, routing, skill summaries
├── SOUL.md            # Persona and behavior guidelines
├── IDENTITY.md        # Name, emoji, role
├── TOOLS.md           # Tool usage and workflows
├── USER.md            # User preferences (customize this)
├── MEMORY.md          # Memory structure
├── HEARTBEAT.md       # Health check instructions
├── .openclaw/         # Workspace state
├── memory/            # Long-term memory
└── skills/            # Skill library
    ├── brainstorming/
    ├── writing-plans/
    ├── executing-plans/
    ├── subagent-driven-development/
    ├── using-git-worktrees/
    ├── finishing-a-development-branch/
    ├── test-driven-development/
    ├── requesting-code-review/
    ├── receiving-code-review/
    ├── verification-before-completion/
    ├── systematic-debugging/
    ├── using-superpowers/
    ├── writing-skills/
    └── dispatching-parallel-agents/
```

---

## Development Workflow

```
BRAINSTORM → PLAN → EXECUTE → VERIFY → COMMIT

1. BRAINSTORM: Ask 6 questions, propose approaches, create spec.md + design.md
2. PLAN: Break into 2-5 min tasks with dependencies
3. EXECUTE: Inline or dispatch subagents
4. VERIFY: Run tests, show output
5. COMMIT: Atomic commits, push
```

---

## Skills Overview

### Planning & Architecture
- **brainstorming** — Ask 6 essential questions, propose approaches, create spec + design
- **writing-plans** — Break design into executable tasks
- **executing-plans** — Run multi-step plans with checkpoints

### Development Workflow
- **subagent-driven-development** — Dispatch parallel subagents
- **using-git-worktrees** — Isolate work in separate worktrees
- **finishing-a-development-branch** — Handle merge/PR decisions

### Quality Assurance
- **test-driven-development** — Strict RED → GREEN → REFACTOR
- **requesting-code-review** — Pre-review checklist
- **receiving-code-review** — Address feedback systematically
- **verification-before-completion** — Run tests, show output

### Debugging
- **systematic-debugging** — 4-phase evidence-based debugging

### Meta
- **using-superpowers** — Skill discovery and invocation rules
- **writing-skills** — Create new skills
- **dispatching-parallel-agents** — Handle 3+ independent problems

---

## Integration

Add to your project's AGENTS.md:

```markdown
# My Project Agent

Load at startup: ~/.openclaw/workspace/superpowers-openclaw/AGENTS.md
```

---

## Requirements

- OpenClaw v2026.2.26+
- Gateway: ws://127.0.0.1:18789
- Config: ~/.openclaw/openclaw.json

---

## License

MIT License - see LICENSE file for details.
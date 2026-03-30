---
name: writing-skills
description: Use when creating new skills. Provides template and testing methodology for skill creation.
---

# Writing Skills

## Overview

Create reusable skills that encode proven workflows. Skills are not just documentation — they're executable processes that must be followed.

## Skill Structure

Every skill needs:

### Frontmatter (Required)
```yaml
---
name: skill-name
description: Use when [condition] - [what it does]
---
```

**name:** Short, lowercase, hyphenated
**description:** Third person, describes WHEN to use, not WHAT it does

### Body Sections

1. **Overview** — What this skill does (1-2 sentences)
2. **Checklist** — Ordered steps to follow (if applicable)
3. **Process** — Detailed instructions
4. **Anti-Patterns** — What NOT to do

## Writing Guidelines

### Do
- Write in second person ("You do X")
- Be specific and actionable
- Include code examples
- Define exact outputs
- List anti-patterns

### Don't
- Be vague ("be careful")
- Skip steps
- Assume context
- Use first person
- Be overly long

## Skill Naming

- Use action verbs: `test-driven-development`, `requesting-code-review`
- Keep it short: `debugging` not `systematic-debugging-approach`
- Be consistent: `doing-x` not `do-x` or `x-action`

## Testing Skills

Before finalizing a skill:

1. **Load it** — Does it make sense?
2. **Follow it** — Can you complete a task using it?
3. **Edge cases** — What happens in unusual situations?
4. **Tool compatibility** — Does it work with available tools?

## Skill Template

```markdown
---
name: my-new-skill
description: Use when [condition] - [what it does]
---

# My New Skill

## Overview

[One sentence describing what this skill does]

## Checklist

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Process

### Step 1: [Name]

[Detailed instructions]

### Step 2: [Name]

[Detailed instructions]

## Anti-Patterns

- [ ] Don't do X
- [ ] Don't do Y

## Examples

### Example 1

[Show working example]
```

## Skill Storage

```
agents/superpowers-dev/
├── AGENTS.md              # Core config (auto-loaded)
├── SOUL.md                # Persona
├── TOOLS.md               # Tool usage
├── IDENTITY.md            # Name/role
├── USER.md                # Preferences
├── HEARTBEAT.md           # Check-ins
├── MEMORY.md              # Long-term memory
└── [skill-name]/
    └── SKILL.md           # Skill file
```

## Skill Invocation

Skills are loaded via:
- readFile: `readFile ~/.openclaw/workspace/agents/superpowers-dev/[skill]/SKILL.md`
- Manual read: `readFile` the SKILL.md

## Best Practices

1. **One skill, one purpose** — Don't combine unrelated workflows
2. **Checklists work** — Use them for multi-step processes
3. **Examples help** — Show, don't just tell
4. **Anti-patterns matter** — Document what to avoid
5. **Test it yourself** — Use the skill before sharing
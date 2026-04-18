---
name: brainstorming
description: Use when beginning any new feature, project, or task to explore requirements before writing code. Explores user intent, constraints, and design trade-offs before implementation.
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.
</HARD-GATE>

## Checklist

1. **Explore project context** — check files, docs, recent commits
2. **Ask the 6 essential questions** — one at a time, get comprehensive answers
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to complexity, get user approval after each section
5. **Write spec.md** — save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.md` with requirements and acceptance criteria
6. **Write design.md** — save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` with architecture and components
7. **Spec self-review** — check for placeholders, contradictions, ambiguity, ensure every requirement has 2-3 testable acceptance criteria
8. **User reviews written specs** — ask user to approve before proceeding
9. **Transition to implementation** — invoke writing-plans skill

## The Process

**Understanding the idea:**
- Check current project state (files, docs, recent commits)
- Ask the 6 essential questions (one at a time):
  1. **What** — What are we building? Describe the feature/project
  2. **Why** — Why is this needed? What problem are we solving?
  3. **Who** — Who will use it? What's their technical level?
  4. **How** — How should it work? Describe the user flow
  5. **When** — When will it be used? Any deadlines or milestones?
  6. **What else** — What else should we consider? Constraints, integrations, etc.

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Lead with your recommendation

**Presenting the design:**
- Scale each section to complexity
- Ask after each section whether it looks right
- Cover: architecture, components, data flow, error handling

**Design for isolation:**
- Break into smaller units with clear purposes
- Well-defined interfaces between components
- Each unit should be understandable and testable independently

## After the Design

**Documentation:**
- Write spec.md to `docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.md`:
  - Overview, Problem Statement, User Stories
  - Functional Requirements with acceptance criteria (2-3 per requirement)
  - Non-Functional Requirements, Technical Constraints
  - Out of Scope, Success Metrics
- Write design.md to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`:
  - Architecture, Data Model, API Design
  - Key Components, User Flows, Edge Cases
- Commit to git

**User Review Gate:**
> "Specs written to `<paths>`. Please review and let me know if you want changes before we start the implementation plan."

Wait for user approval. Only proceed once approved.

**Implementation:**
- Invoke writing-plans skill to create implementation plan
- Do NOT invoke any other skill
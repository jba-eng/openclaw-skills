# Spec Creation Skill

Interactive specification creation with automated discovery, validation, and generation tools.

## Overview

This skill guides you through creating comprehensive software specifications with a structured 6-stage workflow. It includes Python utilities to reduce token usage and improve efficiency.

## Features

- 🔍 **Smart Project Discovery**: Automatically finds projects and existing specs
- ✅ **Validation**: Ensures specs meet quality standards (2-3 ACs per requirement)
- 🤖 **Template Generation**: Creates properly formatted spec files from structured input
- 📊 **Diff Comparison**: Shows changes between spec versions
- 💬 **Interactive Workflow**: Guides you through 6 essential questions
- 📝 **Comprehensive Output**: Generates spec.md, design.md, and tasks.md

## Quick Start

### Using the Skill

Trigger the skill with:
- "spec creation skill"
- "create specs"
- "/spec"

The agent will guide you through:
1. Project discovery and verification
2. Checking existing specifications
3. Answering 6 essential questions
4. Creating detailed spec.md
5. Generating design.md and tasks.md
6. Final approval and validation

### Direct Tool Usage

The skill includes Python utilities you can use directly:

#### Project Discovery

```bash
# List all projects
python scripts/project_discovery.py list

# Find a specific project
python scripts/project_discovery.py find "my-project"

# Full discovery (find + check specs)
python scripts/project_discovery.py full "my-project"
```

#### Spec Validation

```bash
# Validate spec files
python scripts/spec_validator.py .specifications/spec.md
python scripts/spec_validator.py .specifications/*.md
```

#### Spec Generation

```bash
# Generate from JSON input
echo '{"feature_name": "Login", ...}' | python scripts/spec_generator.py spec

# Generate from file
python scripts/spec_generator.py design --data input.json
```

#### Spec Comparison

```bash
# Compare two versions
python scripts/spec_diff.py old_spec.md new_spec.md

# JSON output
python scripts/spec_diff.py old.md new.md --format json
```

## The 6 Essential Questions

1. **Core Problem**: What exactly happened last time it failed? What was the impact?
2. **Primary Users**: Exact roles/titles? Where do they work? What devices?
3. **Perfect Success**: Describe ideal outcome. How many steps/seconds/results?
4. **Key Data/Fields**: What MUST be captured/searched/stored? Examples?
5. **Tech Stack**: Language/framework/DB? Local/cloud/offline needs?
6. **8-Week MVP**: ONE killer feature that proves value immediately?

## Spec Quality Standards

- **Comprehensive**: 300-800 lines is normal for a good spec
- **Testable**: Every requirement has 2-3 specific acceptance criteria
- **Detailed**: Uses exact user terminology from answers
- **Complete**: Includes edge cases, error handling, performance targets
- **Approved**: User reviews and approves before finalization

## File Structure

```
spec-creation/
├── SKILL.md                    # Core skill instructions
├── README.md                   # This file
├── scripts/
│   ├── project_discovery.py    # Find projects & specs
│   ├── spec_validator.py       # Validate spec structure
│   ├── spec_generator.py       # Generate from templates
│   └── spec_diff.py            # Compare versions
└── templates/
    ├── spec_template.md        # Spec.md template
    ├── design_template.md      # Design.md template
    └── tasks_template.md       # Tasks.md template
```

## Token Savings

Using the Python utilities saves approximately:
- **750-1250 tokens per spec creation session** (30-40% reduction)
- **Project discovery**: ~200-300 tokens
- **Validation**: ~150-250 tokens
- **Generation**: ~300-500 tokens
- **Comparison**: ~100-200 tokens

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Examples

### Example Spec Structure

```markdown
# Login Feature Specification

## Context
Users currently cannot access their accounts...

## Users
### Mobile App User
Field technicians using tablets...

## Requirements
- **R1**: User must authenticate within 3 seconds
- **R2**: Support offline authentication for 24 hours

## Acceptance Criteria
### R1
- **AC1**: Login completes in <3s on 4G connection
- **AC2**: Error message shows within 1s if credentials invalid
- **AC3**: Session persists for 7 days with "remember me"
```

## Best Practices

1. **Always check existing specs first** - Never assume project structure
2. **Get detailed answers** - The 6 questions need comprehensive responses
3. **Show before writing** - Display full content before creating files
4. **Validate before finalizing** - Use spec_validator.py to check quality
5. **Track changes** - Use spec_diff.py when updating existing specs

## Troubleshooting

### Project Not Found

```bash
# List all available projects
python scripts/project_discovery.py list
```

### Validation Failures

Common issues:
- Missing required sections (Context, Users, Requirements, Acceptance Criteria)
- Requirements without 2-3 acceptance criteria
- Spec too short (<500 characters)

### Generation Errors

Ensure your JSON input matches the expected structure. See templates/ for examples.

## Contributing

This skill is part of the OpenClaw ecosystem. Contributions welcome!

## License

MIT License - See LICENSE file for details

## Author

Jonathan (OpenClaw)

## Version

1.0.0

---

**Need help?** Trigger the skill and the agent will guide you through the process!

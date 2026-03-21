# Quick Reference - Spec Creation Skill

Fast lookup for common operations.

## Python Utilities

### Project Discovery
```bash
# List all projects
python scripts/project_discovery.py list

# Find specific project
python scripts/project_discovery.py find "project-name"

# Full discovery (find + check specs)
python scripts/project_discovery.py full "project-name"

# Check existing specs in project
python scripts/project_discovery.py check "/path/to/project"
```

**Output**: JSON with match type, project path, existing specs

### Spec Validation
```bash
# Validate single file
python scripts/spec_validator.py .specifications/spec.md

# Validate all spec files
python scripts/spec_validator.py .specifications/*.md

# Get JSON output
python scripts/spec_validator.py spec.md
```

**Checks**:
- Required sections present
- 2-3 ACs per requirement
- Minimum length (500 chars)
- Proper formatting

### Spec Generation
```bash
# Generate spec.md
echo '{"feature_name":"Login",...}' | python scripts/spec_generator.py spec

# Generate design.md
python scripts/spec_generator.py design --data input.json

# Generate tasks.md
python scripts/spec_generator.py tasks < data.json
```

**Input**: JSON with structured data
**Output**: Formatted markdown

### Spec Comparison
```bash
# Text diff
python scripts/spec_diff.py old.md new.md

# JSON output
python scripts/spec_diff.py old.md new.md --format json
```

**Output**: Diff with statistics (additions, deletions, sections changed)

## The 6 Questions

1. **Core Problem**: What failed? Impact?
2. **Primary Users**: Roles? Location? Devices?
3. **Perfect Success**: Ideal outcome? Metrics?
4. **Key Data**: What to capture? Examples?
5. **Tech Stack**: Language? Framework? DB?
6. **8-Week MVP**: ONE killer feature?

## Workflow Stages

1. **Discovery** → Use `project_discovery.py full`
2. **Check Existing** → Review discovery output
3. **Ask Questions** → Get detailed answers
4. **Create spec.md** → Show before writing
5. **User Approval** → Iterate if needed
6. **Create design.md + tasks.md** → Show before writing
7. **Validate** → Use `spec_validator.py`

## File Structure

```
.specifications/
├── spec.md       # Requirements & acceptance criteria
├── design.md     # Architecture & components
└── tasks.md      # Implementation tasks
```

## Spec Quality Standards

- **Length**: 300-800 lines (comprehensive)
- **Requirements**: Specific, measurable
- **Acceptance Criteria**: 2-3 per requirement
- **Sections**: Context, Users, Requirements, ACs
- **Details**: Edge cases, errors, performance

## Common Commands

### Create New Spec
```bash
# 1. Discover project
python scripts/project_discovery.py full "my-project"

# 2. Navigate to project
cd /path/to/project

# 3. Create .specifications directory
mkdir -p .specifications

# 4. Generate spec (after getting answers)
# ... create spec.md, design.md, tasks.md ...

# 5. Validate
python scripts/spec_validator.py .specifications/*.md
```

### Update Existing Spec
```bash
# 1. Check current state
python scripts/project_discovery.py check "/path/to/project"

# 2. Compare versions
python scripts/spec_diff.py .specifications/spec.md new_spec.md

# 3. Validate changes
python scripts/spec_validator.py .specifications/spec.md
```

## Token Savings

| Operation | Manual | With Scripts | Savings |
|-----------|--------|--------------|---------|
| Project Discovery | ~300 | ~50 | 250 |
| Validation | ~250 | ~50 | 200 |
| Generation | ~500 | ~100 | 400 |
| Comparison | ~200 | ~50 | 150 |
| **Total per session** | ~1250 | ~250 | **1000** |

## Error Messages

### "File not found"
- Check project path
- Verify .specifications directory exists
- Use `project_discovery.py` to find correct path

### "No requirements found"
- Check format: `- **R1**: description`
- Ensure Requirements section exists

### "Missing acceptance criteria"
- Each requirement needs 2-3 ACs
- Format: `- **AC1**: test/verification`

### "Spec too short"
- Minimum 500 characters
- Add more detail to Context, Users, Requirements

## Templates

Located in `templates/`:
- `spec_template.md` - Full spec structure
- `design_template.md` - Design document
- `tasks_template.md` - Task breakdown

## Best Practices

1. **Always discover first** - Never assume project structure
2. **Show before writing** - Display full content for approval
3. **Validate before finalizing** - Use spec_validator.py
4. **Get detailed answers** - 6 questions need comprehensive responses
5. **Use Python utilities** - Saves 30-40% tokens

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Project not found | Run `project_discovery.py list` |
| Validation fails | Check error messages, fix format |
| Generation error | Verify JSON structure |
| Diff shows no changes | Files are identical |

---

**Need help?** See README.md for detailed documentation.

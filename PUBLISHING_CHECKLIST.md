# Publishing Checklist for Spec Creation Skill

Use this checklist before publishing to ClawHub or GitHub.

## Pre-Publication Tests

### Python Scripts
- [ ] Test project_discovery.py list
- [ ] Test project_discovery.py find "test-project"
- [ ] Test spec_validator.py on template files
- [ ] Test spec_generator.py with sample JSON
- [ ] Test spec_diff.py with two template files
- [ ] All scripts return valid JSON output
- [ ] Error handling works (test with invalid inputs)

### File Structure
- [ ] All required files present (see below)
- [ ] No personal/sensitive information in files
- [ ] No hardcoded paths (except configurable defaults)
- [ ] Templates are properly formatted
- [ ] README examples are accurate

### Documentation
- [ ] README.md is comprehensive
- [ ] SKILL.md has correct frontmatter
- [ ] CHANGELOG.md is up to date
- [ ] All code examples in docs are tested
- [ ] Token savings claims are accurate

### Metadata
- [ ] _meta.json has correct version
- [ ] _meta.json slug matches SKILL.md
- [ ] Author information is correct
- [ ] Keywords are relevant
- [ ] License is specified

## Required Files Checklist

- [ ] SKILL.md (core instructions)
- [ ] README.md (user documentation)
- [ ] CHANGELOG.md (version history)
- [ ] LICENSE (MIT)
- [ ] _meta.json (metadata)
- [ ] PUBLISH.md (publishing guide)
- [ ] PUBLISHING_CHECKLIST.md (this file)
- [ ] .clawhub/origin.json (source info)
- [ ] scripts/project_discovery.py
- [ ] scripts/spec_validator.py
- [ ] scripts/spec_generator.py
- [ ] scripts/spec_diff.py
- [ ] templates/spec_template.md
- [ ] templates/design_template.md
- [ ] templates/tasks_template.md

## Quality Checks

### SKILL.md
- [ ] Under 100 lines (token efficient)
- [ ] Has frontmatter with all required fields
- [ ] Description is 15-25 words, action verbs
- [ ] "When to Use" section is clear
- [ ] "Core Rules" are actionable (3-7 rules)
- [ ] References Python utilities
- [ ] No redundant information

### README.md
- [ ] Quick start section
- [ ] Feature list with emojis
- [ ] Usage examples for all utilities
- [ ] Token savings documented
- [ ] Troubleshooting section
- [ ] Requirements listed
- [ ] License mentioned

### Python Scripts
- [ ] Shebang line (#!/usr/bin/env python3)
- [ ] Docstrings for all functions
- [ ] JSON output for easy parsing
- [ ] Error handling with meaningful messages
- [ ] No external dependencies (stdlib only)
- [ ] Works on Python 3.7+

## Security Checks

- [ ] No API keys or credentials
- [ ] No personal file paths
- [ ] File operations are safe
- [ ] User approval mentioned for file creation
- [ ] No "silent" or "automatic" operations without disclosure
- [ ] External endpoints documented (if any)

## GitHub Preparation

### Repository Setup
- [ ] Create repository (if not exists)
- [ ] Add .gitignore for Python
- [ ] Add README.md at repo root
- [ ] Add LICENSE at repo root

### Git Commands
```bash
cd workspace/skills/spec-creation
git init
git add .
git commit -m "Initial release of spec-creation skill v1.0.0"
git remote add origin https://github.com/yourusername/openclaw-skills.git
git push -u origin main
```

### Update origin.json
- [ ] Update repository URL in .clawhub/origin.json
- [ ] Update path if needed
- [ ] Verify branch name

## ClawHub Preparation

### Authentication
- [ ] ClawHub CLI installed
- [ ] Logged in: `clawhub login`
- [ ] Verified: `clawhub whoami`

### Pre-Publish Test
```bash
# Dry run (if available)
clawhub publish spec-creation --dry-run

# Or just verify structure
clawhub validate spec-creation
```

## Publishing Steps

### 1. Final Version Check
- [ ] Version in _meta.json: 1.0.0
- [ ] Version in SKILL.md: 1.0.0
- [ ] CHANGELOG.md has entry for 1.0.0
- [ ] All dates are current

### 2. Test Installation Locally
```bash
# If possible, test install from local path
clawhub install ./workspace/skills/spec-creation
```

### 3. Publish to ClawHub
```bash
cd workspace/skills
clawhub publish spec-creation
```

### 4. Verify Publication
```bash
clawhub search spec-creation
clawhub info spec-creation
```

### 5. Test Installation
```bash
# In a different directory
clawhub install spec-creation
```

## Post-Publication

### Verification
- [ ] Skill appears in ClawHub search
- [ ] Skill page shows correct information
- [ ] Download/install works
- [ ] All files are included
- [ ] Scripts are executable

### Promotion
- [ ] Share on social media
- [ ] Post in OpenClaw community
- [ ] Update personal portfolio
- [ ] Add to skill collection

### Monitoring
- [ ] Watch for user feedback
- [ ] Monitor installation count
- [ ] Check for bug reports
- [ ] Plan next version features

## Rollback Plan

If something goes wrong:

```bash
# Delete from ClawHub
clawhub delete spec-creation

# Fix issues locally
# ... make changes ...

# Update version
# Edit _meta.json and SKILL.md

# Republish
clawhub publish spec-creation
```

## Version Update Checklist

For future updates:

- [ ] Update version number (semver)
- [ ] Add CHANGELOG.md entry
- [ ] Update README if needed
- [ ] Test all changes
- [ ] Commit to Git
- [ ] Push to GitHub
- [ ] Republish to ClawHub

---

**Ready to publish?** Check all boxes above, then run:

```bash
clawhub login
clawhub publish spec-creation
```

Good luck! 🚀

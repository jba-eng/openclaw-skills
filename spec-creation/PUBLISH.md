# Publishing Spec Creation Skill to ClawHub

## ✅ Pre-Publication Checklist

### Files Present
- [x] SKILL.md (core instructions)
- [x] README.md (user documentation)
- [x] CHANGELOG.md (version history)
- [x] _meta.json (metadata)
- [x] PUBLISH.md (this file)
- [x] scripts/ directory with Python utilities
- [x] templates/ directory with spec templates

### Quality Checks
- [x] No hardcoded personal paths (uses configurable base path)
- [x] All scripts have proper error handling
- [x] Documentation is comprehensive
- [x] Examples are clear and tested
- [x] Token savings are documented

### Security
- [x] No sensitive information in code
- [x] No API keys or credentials
- [x] File operations are safe and validated
- [x] User approval required for file creation

### Metadata
- [x] Version: 1.0.0
- [x] Author: Jonathan
- [x] License: MIT
- [x] Keywords: specification, requirements, design, documentation

## 📤 Publishing Steps

### Step 1: Verify Python Scripts Work

Test each utility:

```bash
cd workspace/skills/spec-creation

# Test project discovery
python scripts/project_discovery.py list

# Test validator (create a test spec first)
python scripts/spec_validator.py templates/spec_template.md

# Test generator
echo '{"feature_name":"Test","context":"Test context"}' | python scripts/spec_generator.py spec

# Test diff
python scripts/spec_diff.py templates/spec_template.md templates/design_template.md
```

### Step 2: Create .clawhub Directory

```bash
mkdir -p .clawhub
```

### Step 3: Create origin.json

```bash
cat > .clawhub/origin.json << 'EOF'
{
  "source": "github",
  "repository": "yourusername/openclaw-skills",
  "path": "skills/spec-creation",
  "branch": "main"
}
EOF
```

### Step 4: Login to ClawHub

```bash
clawhub login
```

This opens your browser for authentication.

### Step 5: Verify Authentication

```bash
clawhub whoami
```

Should display your user information.

### Step 6: Publish the Skill

From the workspace root:

```bash
cd ~/workspace/skills
clawhub publish spec-creation
```

Or from the skill directory:

```bash
cd ~/workspace/skills/spec-creation
clawhub publish .
```

### Step 7: Verify Publication

```bash
# Search for your skill
clawhub search spec-creation

# View details
clawhub info spec-creation
```

## 📋 What Gets Published

### Included Files
- SKILL.md
- README.md
- CHANGELOG.md
- _meta.json
- scripts/*.py
- templates/*.md

### Excluded Files
- PUBLISH.md (this file)
- PUBLISHING_CHECKLIST.md
- .clawhub/ (metadata only)
- __pycache__/
- *.pyc
- .git/

## 🔧 Troubleshooting

### Common Issues

**1. Not logged in:**
```bash
clawhub login
```

**2. Invalid skill structure:**
- Verify SKILL.md has required frontmatter
- Check _meta.json is valid JSON
- Ensure all required files exist

**3. Duplicate slug:**
If "spec-creation" is taken:
- Update `slug` in _meta.json
- Update `slug` in SKILL.md frontmatter
- Choose a unique name like "spec-creator" or "specification-builder"

**4. Python script errors:**
- Test all scripts individually
- Check Python version (3.7+ required)
- Verify file permissions (chmod +x scripts/*.py)

**5. Network issues:**
- Check internet connection
- Try again: `clawhub publish spec-creation`
- Check ClawHub status

### Get Help

```bash
clawhub publish --help
clawhub --version
```

## 📊 After Publishing

### Update Process

When making changes:

1. **Update version** in _meta.json and SKILL.md
2. **Add entry** to CHANGELOG.md
3. **Test changes** thoroughly
4. **Republish**: `clawhub publish spec-creation`

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.x.x): Breaking changes
- **MINOR** (x.1.x): New features, backward compatible
- **PATCH** (x.x.1): Bug fixes

### Manage Your Skill

**View stats:**
```bash
clawhub stats spec-creation
```

**Update:**
```bash
clawhub publish spec-creation
```

**Delete (soft-delete):**
```bash
clawhub delete spec-creation
```

**Undelete:**
```bash
clawhub undelete spec-creation
```

## 🎉 Success!

Once published, users can install with:

```bash
clawhub install spec-creation
```

Your skill will appear:
- On ClawHub website
- In search results: `clawhub search specification`
- In explore: `clawhub explore`

## 📢 Promotion

Share your skill:
- Tweet about it with #ClawHub
- Post in OpenClaw community
- Add to your GitHub profile
- Write a blog post about the workflow

## 🐛 Bug Reports

Users can report issues:
- GitHub Issues (if you have a repo)
- ClawHub feedback system
- OpenClaw community forums

## 📝 License

This skill is released under the MIT License. See LICENSE file.

---

**Ready to publish?** 

1. Run tests: `python scripts/project_discovery.py list`
2. Login: `clawhub login`
3. Publish: `clawhub publish spec-creation`

Good luck! 🚀

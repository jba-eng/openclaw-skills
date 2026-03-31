# Publishing Spec Coding Skill to ClawHub

## ✅ Pre-Publication Checklist

### Files Present
- [x] SKILL.md (core instructions)
- [x] README.md (user documentation)
- [x] CHANGELOG.md (version history)
- [x] _meta.json (metadata)
- [x] LICENSE (MIT)
- [x] PUBLISH.md (this file)
- [x] QUICK_REFERENCE.md (fast lookup)
- [x] scripts/ directory with Python utilities
- [x] templates/ directory

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
- [x] User approval required for file modifications
- [x] Spec files are protected from modification

### Metadata
- [x] Version: 1.0.0
- [x] Author: Jonathan
- [x] License: MIT
- [x] Keywords: coding, implementation, tasks, execution

## 📤 Publishing Steps

### Step 1: Verify Python Scripts Work

Test each utility:

```bash
cd workspace/skills/spec-coding

# Test task manager discovery
python scripts/task_manager.py discover "test-project"

# Test task manager with a tasks file (create test file first)
# python scripts/task_manager.py status .specifications/tasks.md

# Test validator
# python scripts/task_validator.py list .specifications/tasks.md
```

### Step 2: Update Repository Information

Edit `.clawhub/origin.json`:
```json
{
  "source": "github",
  "repository": "YOUR_USERNAME/openclaw-skills",
  "path": "skills/spec-coding",
  "branch": "main"
}
```

### Step 3: Login to ClawHub

```bash
clawhub login
```

This opens your browser for authentication.

### Step 4: Verify Authentication

```bash
clawhub whoami
```

Should display your user information.

### Step 5: Publish the Skill

From the workspace root:

```bash
cd ~/workspace/skills
clawhub publish spec-coding
```

Or from the skill directory:

```bash
cd ~/workspace/skills/spec-coding
clawhub publish .
```

### Step 6: Verify Publication

```bash
# Search for your skill
clawhub search spec-coding

# View details
clawhub info spec-coding
```

## 📋 What Gets Published

### Included Files
- SKILL.md
- README.md
- CHANGELOG.md
- QUICK_REFERENCE.md
- _meta.json
- LICENSE
- scripts/*.py
- templates/*.md

### Excluded Files
- PUBLISH.md (this file)
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
If "spec-coding" is taken:
- Update `slug` in _meta.json
- Update `slug` in SKILL.md frontmatter
- Choose a unique name like "spec-executor" or "task-coder"

**4. Python script errors:**
- Test all scripts individually
- Check Python version (3.7+ required)
- Verify file permissions

**5. Network issues:**
- Check internet connection
- Try again: `clawhub publish spec-coding`
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
4. **Republish**: `clawhub publish spec-coding`

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.x.x): Breaking changes
- **MINOR** (x.1.x): New features, backward compatible
- **PATCH** (x.x.1): Bug fixes

### Manage Your Skill

**View stats:**
```bash
clawhub stats spec-coding
```

**Update:**
```bash
clawhub publish spec-coding
```

**Delete (soft-delete):**
```bash
clawhub delete spec-coding
```

**Undelete:**
```bash
clawhub undelete spec-coding
```

## 🎉 Success!

Once published, users can install with:

```bash
clawhub install spec-coding
```

Your skill will appear:
- On ClawHub website
- In search results: `clawhub search coding`
- In explore: `clawhub explore`

## 📢 Promotion

Share your skill:
- Tweet about it with #ClawHub
- Post in OpenClaw community
- Add to your GitHub profile
- Write a blog post about the workflow

## 🔗 Integration

This skill works best with:
- **spec-creation** (prerequisite) - Creates the specifications
- **spec-testing** (next step) - Tests the implementation

Mention this in your promotion materials!

## 🐛 Bug Reports

Users can report issues:
- GitHub Issues (if you have a repo)
- ClawHub feedback system
- OpenClaw community forums

## 📝 License

This skill is released under the MIT License. See LICENSE file.

---

**Ready to publish?** 

1. Run tests: `python scripts/task_manager.py discover "test"`
2. Update origin.json with your GitHub username
3. Login: `clawhub login`
4. Publish: `clawhub publish spec-coding`

Good luck! 🚀

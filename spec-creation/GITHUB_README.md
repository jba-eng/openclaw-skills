# Spec Creation Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![ClawHub](https://img.shields.io/badge/ClawHub-spec--creation-green.svg)](https://clawhub.com)

> Create comprehensive software specifications with automated discovery, validation, and a structured 6-stage workflow.

## 🚀 Features

- **Smart Project Discovery** - Automatically finds projects and existing specs
- **Quality Validation** - Ensures specs meet standards (2-3 ACs per requirement)
- **Template Generation** - Creates properly formatted spec files
- **Version Comparison** - Shows changes between spec versions
- **Token Efficient** - Python utilities save 30-40% tokens per session
- **Interactive Workflow** - Guides through 6 essential questions

## 📦 Installation

### Via ClawHub (Recommended)

```bash
clawhub install spec-creation
```

### Manual Installation

```bash
git clone https://github.com/yourusername/openclaw-skills.git
cd openclaw-skills/spec-creation
```

## 🎯 Quick Start

### Using with OpenClaw Agent

Trigger the skill:
```
"spec creation skill"
"create specs"
"/spec"
```

The agent will guide you through the complete workflow.

### Direct CLI Usage

```bash
# Discover projects
python scripts/project_discovery.py list

# Validate specs
python scripts/spec_validator.py .specifications/*.md

# Compare versions
python scripts/spec_diff.py old.md new.md
```

## 📚 Documentation

- [README.md](README.md) - Complete user guide
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Fast lookup
- [PUBLISH.md](PUBLISH.md) - Publishing guide
- [CHANGELOG.md](CHANGELOG.md) - Version history

## 🛠️ Python Utilities

### 1. Project Discovery (`project_discovery.py`)

Finds projects and existing specification files.

```bash
python scripts/project_discovery.py full "my-project"
```

**Output**: JSON with match type, project path, existing specs

### 2. Spec Validator (`spec_validator.py`)

Validates spec structure and quality.

```bash
python scripts/spec_validator.py .specifications/spec.md
```

**Checks**: Required sections, 2-3 ACs per requirement, proper formatting

### 3. Spec Generator (`spec_generator.py`)

Generates specs from structured input.

```bash
echo '{"feature_name":"Login",...}' | python scripts/spec_generator.py spec
```

**Output**: Formatted markdown files

### 4. Spec Diff (`spec_diff.py`)

Compares specification versions.

```bash
python scripts/spec_diff.py old.md new.md
```

**Output**: Unified diff with statistics

## 📋 The 6 Essential Questions

1. **Core Problem**: What failed? What was the impact?
2. **Primary Users**: Roles/titles? Location? Devices?
3. **Perfect Success**: Ideal outcome? Metrics?
4. **Key Data**: What to capture? Examples?
5. **Tech Stack**: Language? Framework? DB?
6. **8-Week MVP**: ONE killer feature?

## 📊 Token Savings

| Operation | Manual | With Scripts | Savings |
|-----------|--------|--------------|---------|
| Project Discovery | ~300 | ~50 | 250 |
| Validation | ~250 | ~50 | 200 |
| Generation | ~500 | ~100 | 400 |
| Comparison | ~200 | ~50 | 150 |
| **Total per session** | ~1250 | ~250 | **1000** |

## 🏗️ File Structure

```
spec-creation/
├── SKILL.md                    # Core skill instructions
├── README.md                   # User documentation
├── scripts/
│   ├── project_discovery.py    # Find projects & specs
│   ├── spec_validator.py       # Validate structure
│   ├── spec_generator.py       # Generate from templates
│   └── spec_diff.py            # Compare versions
└── templates/
    ├── spec_template.md        # Spec.md template
    ├── design_template.md      # Design.md template
    └── tasks_template.md       # Tasks.md template
```

## 🔧 Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## 📖 Examples

### Example Workflow

```bash
# 1. Discover project
python scripts/project_discovery.py full "my-app"

# 2. Navigate to project
cd /path/to/my-app

# 3. Create specifications directory
mkdir -p .specifications

# 4. Use the skill to create specs
# (Agent guides through 6 questions)

# 5. Validate the output
python scripts/spec_validator.py .specifications/*.md
```

### Example Spec Output

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
- **AC2**: Error message shows within 1s if invalid
- **AC3**: Session persists for 7 days with "remember me"
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Jonathan** - [OpenClaw](https://github.com/yourusername)

## 🙏 Acknowledgments

- OpenClaw community
- ClawHub platform
- All contributors

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/openclaw-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/openclaw-skills/discussions)
- **ClawHub**: [Skill Page](https://clawhub.com/skills/spec-creation)

## 🔗 Links

- [ClawHub](https://clawhub.com)
- [OpenClaw Documentation](https://docs.openclaw.com)
- [Skill Builder Guide](https://clawhub.com/skills/skill-builder)

---

**Made with ❤️ for the OpenClaw community**

⭐ Star this repo if you find it useful!

# OpenClaw Skills Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A collection of powerful skills for OpenClaw AI agents. 🚀

---

## 📖 Table of Contents

- [Introduction](#introduction)
- [Skills List](#skills-list)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Introduction

This repository contains modular skills that extend OpenClaw AI agent capabilities. Each skill provides specialized workflows, tool integrations, and domain expertise.

**Features:**
- ✅ Multi-language support (English & Chinese)
- ✅ Easy to install and use
- ✅ Well-documented
- ✅ Community-driven

---

## 📦 Skills List

### 🔍 Code Quality & Analysis

| Skill | Description | Language |
|-------|-------------|----------|
| **skill-auditor** | Scans installed skills for duplicates and naming conflicts. Detects similar skills that may cause model confusion. | 🌐 EN/ZH |

**Usage:**
```bash
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang auto
```

---

## 🚀 Installation

### Prerequisites

- OpenClaw installed
- Python 3.7+
- Git

### Method 1: Clone Repository

```bash
# Clone the repository
git clone git@github.com:shyjsarah/skills.git

# Navigate to skills directory
cd skills

# Install dependencies (if any)
pip install -r requirements.txt
```

### Method 2: Individual Skill Installation

```bash
# Clone specific skill
git clone git@github.com:shyjsarah/skills.git --depth 1

# Copy skill to OpenClaw workspace
cp -r skill-auditor ~/.openclaw/workspace/skills/
```

### Method 3: Package Installation (.skill file)

```bash
# Package a skill
cd skill-auditor
python3 ../scripts/package_skill.py .

# Install .skill file in OpenClaw
# (Follow OpenClaw documentation for .skill installation)
```

---

## 💡 Usage

### Skill Auditor Example

```bash
# Navigate to skill directory
cd skill-auditor

# Run scan (auto-detect language)
python3 scripts/main.py ~/.openclaw/workspace/skills/

# Specify language
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang zh

# Custom threshold
python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.8

# Output to file
python3 scripts/main.py ~/.openclaw/workspace/skills/ -o audit_report.md
```

### Output Example

```
🔍 Scan Directory: /home/user/.openclaw/workspace/skills
📦 Total Skills: 15

✅ No Duplicate Skills Found

All skills have distinct names and descriptions. No optimization needed.
```

---

## 🛠️ Development

### Project Structure

```
skills/
├── skill-auditor/           # Skill directory
│   ├── scripts/             # Python scripts
│   ├── locales/             # Language files
│   ├── references/          # Documentation
│   ├── SKILL.md             # Skill definition (EN)
│   ├── SKILL.zh-CN.md       # Skill definition (ZH)
│   └── requirements.txt     # Dependencies
└── README.md                # This file
```

### Creating New Skills

1. **Initialize skill structure:**
   ```bash
   mkdir -p my-skill/{scripts,locales,references,assets}
   ```

2. **Create SKILL.md:**
   ```markdown
   ---
   name: my-skill
   description: What your skill does
   ---
   
   # Skill Documentation
   ...
   ```

3. **Add scripts and resources**

4. **Test your skill:**
   ```bash
   python3 scripts/main.py [args]
   ```

### Branch Strategy

- `main` - Stable releases
- `feature/*` - New features
- `fix/*` - Bug fixes

### Commit Convention

```
feat: Add new skill
fix: Fix bug in skill-auditor
docs: Update README
refactor: Improve code structure
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **Create new skills** - Share your specialized workflows
2. **Improve existing skills** - Fix bugs, add features
3. **Translate** - Add support for more languages
4. **Documentation** - Improve guides and examples

### Pull Request Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Skill Creator Guide](https://docs.openclaw.ai/skills)

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/shyjsarah/skills/issues)
- **Discussions:** [GitHub Discussions](https://github.com/shyjsarah/skills/discussions)

---

## 🙏 Acknowledgments

- OpenClaw team for the amazing framework
- All contributors for their valuable skills
- Community members for feedback and suggestions

---

**Happy Skill Building! 🎉**

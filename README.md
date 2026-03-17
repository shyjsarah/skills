# OpenClaw Skills Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OpenClaw 技能集合 - 可复用的 AI 技能模块 🚀

---

## 📦 什么是技能？

技能是独立的模块化包，扩展 OpenClaw AI 的能力。每个技能包含：

- **SKILL.md** - 技能定义（YAML frontmatter + 使用说明）
- **scripts/** - 可执行代码（Python/Bash 等）
- **references/** - 参考文档
- **assets/** - 资源文件（模板、图片等）

---

## 📋 可用技能

| 技能 | 描述 | 语言 |
|------|------|------|
| **[skill-auditor](skill-auditor/)** 🔍 | 检测重复或相似的技能，避免模型混淆 | 🌐 中文/English |

---

## 🚀 安装技能

### 前置要求

- OpenClaw 已安装
- Git
- Python 3.7+（部分技能需要）

### 方法 1：通过 npx skills（推荐）

```bash
# GitHub shorthand（推荐）
npx skills add shyjsarah/skills --skill skill-auditor -g

# 或 Git URL
npx skills add git@github.com:shyjsarah/skills.git -g

# 安装所有技能
npx skills add shyjsarah/skills -g
```

**参数说明：**
- `-g`：全局安装到 `~/.openclaw/skills/`
- `--skill <name>`：安装指定技能
- `-y`：跳过确认提示

### 方法 2：手动安装

```bash
# 1. 克隆仓库
git clone git@github.com:shyjsarah/skills.git

# 2. 复制技能到工作区
cp -r skill-auditor ~/.openclaw/workspace/skills/

# 3. 安装依赖（如有）
cd ~/.openclaw/workspace/skills/skill-auditor
pip install -r requirements.txt

# 4. 重启 OpenClaw
```

---

## 🔧 验证安装

**在 OpenClaw 对话中测试：**

```
# 检查技能是否已加载
/openclaw skills list

# 或直接测试技能功能
请扫描我的技能库，检查是否有重复的技能
```

**终端验证（可选）：**
```bash
# 检查技能目录
ls ~/.openclaw/workspace/skills/skill-auditor/

# 测试技能命令
python3 ~/.openclaw/workspace/skills/skill-auditor/scripts/main.py --help
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Skills.sh 技能市场](https://skills.sh/)
- [Skills CLI GitHub](https://github.com/vercel-labs/skills)

---

## 📞 支持

- **Bug 报告：** [GitHub Issues](https://github.com/shyjsarah/skills/issues)
- **讨论交流：** [GitHub Discussions](https://github.com/shyjsarah/skills/discussions)

---

**祝你使用愉快！🎉**

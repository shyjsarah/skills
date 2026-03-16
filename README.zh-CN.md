# OpenClaw Skills 仓库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

OpenClaw AI 智能体的技能集合库。🚀

---

## 📖 目录

- [简介](#简介)
- [技能列表](#技能列表)
- [安装方式](#安装方式)
- [使用方法](#使用方法)
- [开发指南](#开发指南)
- [贡献代码](#贡献代码)
- [许可证](#许可证)

---

## 🌟 简介

本仓库包含模块化的 OpenClaw AI 智能体技能。每个技能提供专业化的工作流、工具集成和领域专业知识。

**特性：**
- ✅ 多语言支持（中文 & 英文）
- ✅ 易于安装和使用
- ✅ 完善的文档
- ✅ 社区驱动

---

## 📦 技能列表

### 🔍 代码质量与分析

| 技能 | 描述 | 语言 |
|------|------|------|
| **skill-auditor** | 扫描已安装的技能，检测重复和命名冲突。发现可能导致模型混淆的相似技能。 | 🌐 中/英 |

**使用方法：**
```bash
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang auto
```

---

## 🚀 安装方式

### 前置要求

- 已安装 OpenClaw
- Python 3.7+
- Git

### 方式一：克隆仓库

```bash
# 克隆仓库
git clone git@github.com:shyjsarah/skills.git

# 进入技能目录
cd skills

# 安装依赖（如有）
pip install -r requirements.txt
```

### 方式二：单独技能安装

```bash
# 克隆特定技能
git clone git@github.com:shyjsarah/skills.git --depth 1

# 复制技能到 OpenClaw 工作区
cp -r skill-auditor ~/.openclaw/workspace/skills/
```

### 方式三：包安装（.skill 文件）

```bash
# 打包技能
cd skill-auditor
python3 ../scripts/package_skill.py .

# 在 OpenClaw 中安装 .skill 文件
# （参考 OpenClaw 文档了解 .skill 安装方式）
```

---

## 💡 使用方法

### Skill Auditor 示例

```bash
# 进入技能目录
cd skill-auditor

# 运行扫描（自动检测语言）
python3 scripts/main.py ~/.openclaw/workspace/skills/

# 指定语言
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang zh

# 自定义阈值
python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.8

# 输出到文件
python3 scripts/main.py ~/.openclaw/workspace/skills/ -o audit_report.md
```

### 输出示例

```
🔍 扫描目录：/home/user/.openclaw/workspace/skills
📦 技能总数：15

✅ 未发现重复技能

所有技能的名称和描述都有明显差异，无需优化。
```

---

## 🛠️ 开发指南

### 项目结构

```
skills/
├── skill-auditor/           # 技能目录
│   ├── scripts/             # Python 脚本
│   ├── locales/             # 语言文件
│   ├── references/          # 文档资料
│   ├── SKILL.md             # 技能定义（英文）
│   ├── SKILL.zh-CN.md       # 技能定义（中文）
│   └── requirements.txt     # 依赖
└── README.md                # 本文件
```

### 创建新技能

1. **初始化技能结构：**
   ```bash
   mkdir -p my-skill/{scripts,locales,references,assets}
   ```

2. **创建 SKILL.md：**
   ```markdown
   ---
   name: my-skill
   description: 你的技能功能描述
   ---
   
   # 技能文档
   ...
   ```

3. **添加脚本和资源**

4. **测试技能：**
   ```bash
   python3 scripts/main.py [参数]
   ```

### 分支策略

- `main` - 稳定版本
- `feature/*` - 新功能
- `fix/*` - Bug 修复

### 提交规范

```
feat: 添加新技能
fix: 修复 skill-auditor 的 bug
docs: 更新 README
refactor: 改进代码结构
```

---

## 🤝 贡献代码

我们欢迎贡献！以下是参与方式：

### 贡献方式

1. **创建新技能** - 分享你的专业工作流
2. **改进现有技能** - 修复 bug、添加功能
3. **翻译** - 添加更多语言支持
4. **文档** - 改进指南和示例

### Pull Request 流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码风格

- Python 代码遵循 PEP 8
- 使用有意义的变量名
- 为复杂逻辑添加注释
- 包含文档字符串

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🔗 链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [技能创建指南](https://docs.openclaw.ai/skills)

---

## 📞 支持

- **问题反馈：** [GitHub Issues](https://github.com/shyjsarah/skills/issues)
- **讨论区：** [GitHub Discussions](https://github.com/shyjsarah/skills/discussions)

---

## 🙏 致谢

- OpenClaw 团队提供的出色框架
- 所有贡献者的宝贵技能
- 社区成员的反馈和建议

---

**祝技能开发愉快！🎉**

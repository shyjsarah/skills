---
name: bot-gatekeeper
description: 控制谁可以访问你的 OpenClaw 机器人。基于白名单的访问控制，支持主人审批流程。
tags: ["access-control", "whitelist", "authorization", "security", "gatekeeper", "bot"]
---

# Bot Gatekeeper 🛡️
机器人访问守卫

控制谁可以访问你的 OpenClaw 机器人。只有经过批准的用户才能与你的 Agent 对话。

## 使用场景

- 限制机器人只能被特定用户使用
- 新用户需要审批流程
- 防止未授权访问你的 Agent
- 管理用户权限（白名单/黑名单）

## 快速开始

### 1. 安装

```bash
clawhub install bot-gatekeeper
```

### 2. 配置主人

```bash
# 设置你的用户 ID 为主人（从 /whoami 获取）
python3 scripts/main.py config set-owner <your_user_id>
```

### 3. 启用 Hook

```bash
openclaw hooks enable bot-gatekeeper
```

## 使用方法

### 机器人主人

#### 查看待审批
```bash
# 列出所有待审批请求
python3 scripts/main.py pending

# 查看特定请求详情
python3 scripts/main.py pending <user_id>
```

#### 批准/拒绝用户
```bash
# 批准用户
python3 scripts/main.py approve <user_id>

# 拒绝用户
python3 scripts/main.py reject <user_id>

# 批准并添加理由
python3 scripts/main.py approve <user_id> --reason "团队成员"
```

#### 管理白名单
```bash
# 查看所有白名单用户
python3 scripts/main.py whitelist

# 从白名单移除
python3 scripts/main.py remove <user_id>

# 直接添加（跳过审批）
python3 scripts/main.py add <user_id>
```

#### 管理黑名单
```bash
# 查看所有黑名单用户
python3 scripts/main.py blacklist

# 添加到黑名单
python3 scripts/main.py block <user_id>

# 从黑名单移除
python3 scripts/main.py unblock <user_id>
```

### 普通用户

#### 查看状态
```bash
# 查看自己是否已批准
python3 scripts/main.py status
```

#### 撤销请求
```bash
# 撤销待审批请求
python3 scripts/main.py withdraw
```

## 工作流程

```
用户发送消息
    ↓
Bot Gatekeeper Hook 拦截
    ↓
检查白名单
    ↓
是 → 允许对话
否 → 检查黑名单
    ↓
是 → 拒绝并提示
否 → 创建审批请求 → 通知主人
    ↓
主人审查
    ↓
批准 → 加入白名单 → 允许
拒绝 → 发送拒绝消息
```

## 配置

编辑 `config/config.json`:

```json
{
  "owner_id": "ou_你的用户 ID",
  "auto_approve_patterns": [],
  "rejection_message": "访问被拒绝。你需要主人批准才能使用此机器人。",
  "pending_message": "你的请求已发送给主人审批，请等待。",
  "notify_owner": true,
  "whitelist": [],
  "blacklist": []
}
```

### 自动批准规则

添加模式自动批准特定用户：

```json
{
  "auto_approve_patterns": [
    {
      "type": "email_domain",
      "value": "@company.com",
      "description": "自动批准公司邮箱"
    },
    {
      "type": "user_id_prefix",
      "value": "ou_team_",
      "description": "自动批准团队成员"
    }
  ]
}
```

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `pending` | 列出待审批请求 | `python3 main.py pending` |
| `approve <user_id>` | 批准用户 | `python3 main.py approve ou_xxx` |
| `reject <user_id>` | 拒绝用户 | `python3 main.py reject ou_xxx` |
| `whitelist` | 查看白名单 | `python3 main.py whitelist` |
| `add <user_id>` | 添加到白名单 | `python3 main.py add ou_xxx` |
| `remove <user_id>` | 从白名单移除 | `python3 main.py remove ou_xxx` |
| `blacklist` | 查看黑名单 | `python3 main.py blacklist` |
| `block <user_id>` | 添加到黑名单 | `python3 main.py block ou_xxx` |
| `unblock <user_id>` | 从黑名单移除 | `python3 main.py unblock ou_xxx` |
| `status` | 查看自己的状态 | `python3 main.py status` |
| `withdraw` | 撤销请求 | `python3 main.py withdraw` |

## 数据库结构

SQLite 数据库：`data/bot-gatekeeper.db`

```sql
-- 白名单表
CREATE TABLE whitelist (
    user_id TEXT PRIMARY KEY,
    approved_by TEXT,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    expires_at TIMESTAMP
);

-- 黑名单表
CREATE TABLE blacklist (
    user_id TEXT PRIMARY KEY,
    blocked_by TEXT,
    blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT
);

-- 审批请求表
CREATE TABLE approval_requests (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    channel_id TEXT,
    message TEXT,
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by TEXT,
    review_comment TEXT
);

-- 审计日志表
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    user_id TEXT,
    actor_id TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 示例

### 示例 1: 第一个用户请求

```
用户 (ou_abc123): 你好！
Bot Gatekeeper: 你的访问请求已发送给主人审批，请等待。

主人收到通知:
🔔 新的访问请求
用户：ou_abc123
消息："你好！"
时间：2026-03-18 23:00

批准：python3 main.py approve ou_abc123
拒绝：python3 main.py reject ou_abc123
```

### 示例 2: 主人批准

```
主人：python3 main.py approve ou_abc123 --reason "团队成员"

系统：✅ 用户 ou_abc123 已批准并加入白名单

用户收到:
✅ 你的访问已批准！你现在可以与机器人对话了。
```

### 示例 3: 查看所有待审批

```
$ python3 main.py pending

📋 待审批请求 (3)

1. 用户：ou_abc123
   消息："你好！"
   时间：2026-03-18 23:00
   
2. 用户：ou_def456
   消息："我可以用这个机器人吗？"
   时间：2026-03-18 22:30
   
3. 用户：ou_ghi789
   消息："需要帮助..."
   时间：2026-03-18 22:00
```

## 依赖

- Python 3.7+
- SQLite3
- PyYAML (`pip install pyyaml`)

## 许可证

MIT-0

## 仓库

源码：[https://github.com/shyjsarah/skills/tree/main/bot-gatekeeper](https://github.com/shyjsarah/skills/tree/main/bot-gatekeeper)

作者：shyjsarah

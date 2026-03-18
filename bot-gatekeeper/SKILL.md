---
name: bot-gatekeeper
description: Control who can access your OpenClaw bot. Whitelist-based access control with owner approval workflow.
tags: ["access-control", "whitelist", "authorization", "security", "gatekeeper", "bot"]
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"], "env": [] },
      "primaryEnv": "",
    },
  }
---

# Bot Gatekeeper 🛡️

Control who can access your OpenClaw bot. Only approved users can chat with your agent.

## When to Use

- You want to restrict bot access to specific users
- You need an approval workflow for new users
- You want to prevent unauthorized access to your agent
- You need to manage user permissions (whitelist/blacklist)

## Quick Start

### 1. Install

```bash
clawhub install bot-gatekeeper
```

### 2. Configure Owner

```bash
# Set your user ID as owner (get from /whoami)
python3 scripts/main.py config set-owner <your_user_id>
```

### 3. Enable Hook

```bash
openclaw hooks enable bot-gatekeeper
```

## Usage

### For Bot Owner

#### View Pending Approvals
```bash
# List all pending requests
python3 scripts/main.py pending

# View details of a specific request
python3 scripts/main.py pending <user_id>
```

#### Approve/Reject Users
```bash
# Approve a user
python3 scripts/main.py approve <user_id>

# Reject a user
python3 scripts/main.py reject <user_id>

# Approve with reason
python3 scripts/main.py approve <user_id> --reason "Team member"
```

#### Manage Whitelist
```bash
# View all whitelisted users
python3 scripts/main.py whitelist

# Remove user from whitelist
python3 scripts/main.py remove <user_id>

# Add user directly (skip approval)
python3 scripts/main.py add <user_id>
```

#### Manage Blacklist
```bash
# View all blacklisted users
python3 scripts/main.py blacklist

# Add user to blacklist
python3 scripts/main.py block <user_id>

# Remove from blacklist
python3 scripts/main.py unblock <user_id>
```

### For Regular Users

#### Check Your Status
```bash
# Check if you're approved
python3 scripts/main.py status
```

#### Withdraw Request
```bash
# Withdraw your pending request
python3 scripts/main.py withdraw
```

## How It Works

```
User sends message
    ↓
Bot Gatekeeper Hook intercepts
    ↓
Check whitelist
    ↓
Yes → Allow conversation
No → Check blacklist
    ↓
Yes → Reject with message
No → Create approval request → Notify owner
    ↓
Owner reviews
    ↓
Approve → Add to whitelist → Allow
Reject → Send rejection message
```

## Configuration

Edit `config/config.json`:

```json
{
  "owner_id": "ou_your_user_id",
  "auto_approve_patterns": [],
  "rejection_message": "Access denied. You need owner approval to use this bot.",
  "pending_message": "Your request has been sent to the owner for approval.",
  "notify_owner": true,
  "whitelist": [],
  "blacklist": []
}
```

### Auto-Approve Rules

Add patterns to auto-approve specific users:

```json
{
  "auto_approve_patterns": [
    {
      "type": "email_domain",
      "value": "@company.com",
      "description": "Auto-approve company emails"
    },
    {
      "type": "user_id_prefix",
      "value": "ou_team_",
      "description": "Auto-approve team members"
    }
  ]
}
```

## API Reference

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `pending` | List pending requests | `python3 main.py pending` |
| `approve <user_id>` | Approve user | `python3 main.py approve ou_xxx` |
| `reject <user_id>` | Reject user | `python3 main.py reject ou_xxx` |
| `whitelist` | View whitelist | `python3 main.py whitelist` |
| `add <user_id>` | Add to whitelist | `python3 main.py add ou_xxx` |
| `remove <user_id>` | Remove from whitelist | `python3 main.py remove ou_xxx` |
| `blacklist` | View blacklist | `python3 main.py blacklist` |
| `block <user_id>` | Add to blacklist | `python3 main.py block ou_xxx` |
| `unblock <user_id>` | Remove from blacklist | `python3 main.py unblock ou_xxx` |
| `status` | Check your status | `python3 main.py status` |
| `withdraw` | Withdraw request | `python3 main.py withdraw` |

## Database Schema

SQLite database: `data/bot-gatekeeper.db`

```sql
-- Whitelist table
CREATE TABLE whitelist (
    user_id TEXT PRIMARY KEY,
    approved_by TEXT,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    expires_at TIMESTAMP
);

-- Blacklist table
CREATE TABLE blacklist (
    user_id TEXT PRIMARY KEY,
    blocked_by TEXT,
    blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT
);

-- Approval requests table
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

-- Audit log table
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    user_id TEXT,
    actor_id TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Examples

### Example 1: First User Request

```
User (ou_abc123): Hello!
Bot Gatekeeper: Your access request has been sent to the owner for approval. Please wait.

Owner receives notification:
🔔 New Access Request
User: ou_abc123
Message: "Hello!"
Time: 2026-03-18 23:00

Approve: python3 main.py approve ou_abc123
Reject: python3 main.py reject ou_abc123
```

### Example 2: Owner Approves

```
Owner: python3 main.py approve ou_abc123 --reason "Team member"

System: ✅ User ou_abc123 approved and added to whitelist

User receives:
✅ Your access has been approved! You can now chat with the bot.
```

### Example 3: View All Pending

```
$ python3 main.py pending

📋 Pending Approval Requests (3)

1. User: ou_abc123
   Message: "Hello!"
   Time: 2026-03-18 23:00
   
2. User: ou_def456
   Message: "Can I use this bot?"
   Time: 2026-03-18 22:30
   
3. User: ou_ghi789
   Message: "Need help with..."
   Time: 2026-03-18 22:00
```

## Requirements

- Python 3.7+
- SQLite3
- PyYAML (`pip install pyyaml`)

## License

MIT-0

## Repository

Source: [https://github.com/shyjsarah/skills/tree/main/bot-gatekeeper](https://github.com/shyjsarah/skills/tree/main/bot-gatekeeper)

Author: shyjsarah

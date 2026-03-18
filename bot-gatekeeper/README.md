# Bot Gatekeeper 🛡️

Control who can access your OpenClaw bot. Only approved users can chat with your agent.

## Quick Start

```bash
# Install
clawhub install bot-gatekeeper

# Configure owner (get your user ID from /whoami)
python3 scripts/main.py config set-owner <your_user_id>

# Enable hook
openclaw hooks enable bot-gatekeeper
```

## Features

- ✅ Whitelist-based access control
- ✅ Approval workflow for new users
- ✅ Blacklist for blocking users
- ✅ Auto-approve rules
- ✅ Audit logging
- ✅ Owner notifications

## Documentation

- English: [SKILL.md](SKILL.md)
- 中文：[SKILL.zh-CN.md](SKILL.zh-CN.md)

## License

MIT-0

#!/usr/bin/env python3
"""
Bot Gatekeeper - 机器人访问守卫
控制谁可以访问你的 OpenClaw 机器人

Usage:
    python3 main.py <command> [args]

Commands:
    pending         - List pending approval requests
    approve <user>  - Approve a user
    reject <user>   - Reject a user
    whitelist       - View whitelist
    add <user>      - Add user to whitelist
    remove <user>   - Remove from whitelist
    blacklist       - View blacklist
    block <user>    - Block a user
    unblock <user>  - Unblock a user
    status          - Check your status
    withdraw        - Withdraw pending request
    config          - Configuration commands
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts import db_manager, config_manager, notification


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    # Initialize database
    db = db_manager.DatabaseManager()
    db.initialize()
    
    # Load config
    config = config_manager.ConfigManager()
    
    # Route commands
    if command == 'pending':
        list_pending(db, sys.argv[2] if len(sys.argv) > 2 else None)
    elif command == 'approve':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        approve_user(db, config, sys.argv[2], sys.argv[3:] if len(sys.argv) > 3 else [])
    elif command == 'reject':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        reject_user(db, config, sys.argv[2], sys.argv[3:] if len(sys.argv) > 3 else [])
    elif command == 'whitelist':
        list_whitelist(db)
    elif command == 'add':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        add_to_whitelist(db, config, sys.argv[2])
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        remove_from_whitelist(db, sys.argv[2])
    elif command == 'blacklist':
        list_blacklist(db)
    elif command == 'block':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        block_user(db, config, sys.argv[2])
    elif command == 'unblock':
        if len(sys.argv) < 3:
            print("❌ Error: user_id required")
            return
        unblock_user(db, sys.argv[2])
    elif command == 'status':
        check_status(db, config)
    elif command == 'withdraw':
        withdraw_request(db, config)
    elif command == 'config':
        handle_config(config, sys.argv[2:] if len(sys.argv) > 2 else [])
    elif command == 'help' or command == '-h' or command == '--help':
        print_help()
    else:
        print(f"❌ Unknown command: {command}")
        print_help()


def print_help():
    print(__doc__)


def list_pending(db, user_id=None):
    """List pending approval requests"""
    pending = db.get_pending_requests(user_id)
    
    if not pending:
        print("✅ No pending requests")
        return
    
    print(f"📋 Pending Approval Requests ({len(pending)})\n")
    
    for i, req in enumerate(pending, 1):
        print(f"{i}. User: {req['user_id']}")
        print(f"   Message: \"{req['message'][:50]}...\"")
        print(f"   Time: {req['created_at']}")
        print()


def approve_user(db, config, user_id, args):
    """Approve a user"""
    # Check if caller is owner
    if not config.is_owner():
        print("❌ Only owner can approve users")
        return
    
    # Add to whitelist
    reason = ""
    if '--reason' in args:
        idx = args.index('--reason')
        if idx + 1 < len(args):
            reason = args[idx + 1]
    
    db.add_to_whitelist(user_id, config.owner_id, reason)
    db.update_request_status(user_id, 'approved', config.owner_id, reason)
    
    print(f"✅ User {user_id} approved and added to whitelist")
    
    # Notify user
    notification.send_to_user(user_id, "✅ Your access has been approved! You can now chat with the bot.")


def reject_user(db, config, user_id, args):
    """Reject a user"""
    # Check if caller is owner
    if not config.is_owner():
        print("❌ Only owner can reject users")
        return
    
    # Add to blacklist (optional)
    reason = ""
    if '--reason' in args:
        idx = args.index('--reason')
        if idx + 1 < len(args):
            reason = args[idx + 1]
    
    db.update_request_status(user_id, 'rejected', config.owner_id, reason)
    
    print(f"❌ User {user_id} rejected")
    
    # Notify user
    msg = "❌ Your access request has been rejected."
    if reason:
        msg += f" Reason: {reason}"
    notification.send_to_user(user_id, msg)


def list_whitelist(db):
    """List all whitelisted users"""
    users = db.get_whitelist()
    
    if not users:
        print("📋 Whitelist is empty")
        return
    
    print(f"📋 Whitelist ({len(users)} users)\n")
    
    for user in users:
        print(f"  - {user['user_id']}")
        print(f"    Approved by: {user['approved_by']}")
        print(f"    Approved at: {user['approved_at']}")
        if user.get('reason'):
            print(f"    Reason: {user['reason']}")
        print()


def add_to_whitelist(db, config, user_id):
    """Add user to whitelist directly"""
    if not config.is_owner():
        print("❌ Only owner can add users")
        return
    
    db.add_to_whitelist(user_id, config.owner_id, "Direct add by owner")
    print(f"✅ User {user_id} added to whitelist")


def remove_from_whitelist(db, user_id):
    """Remove user from whitelist"""
    db.remove_from_whitelist(user_id)
    print(f"✅ User {user_id} removed from whitelist")


def list_blacklist(db):
    """List all blacklisted users"""
    users = db.get_blacklist()
    
    if not users:
        print("📋 Blacklist is empty")
        return
    
    print(f"📋 Blacklist ({len(users)} users)\n")
    
    for user in users:
        print(f"  - {user['user_id']}")
        print(f"    Blocked by: {user['blocked_by']}")
        print(f"    Blocked at: {user['blocked_at']}")
        if user.get('reason'):
            print(f"    Reason: {user['reason']}")
        print()


def block_user(db, config, user_id):
    """Block a user"""
    if not config.is_owner():
        print("❌ Only owner can block users")
        return
    
    db.add_to_blacklist(user_id, config.owner_id, "Blocked by owner")
    db.remove_from_whitelist(user_id)
    
    print(f"🚫 User {user_id} blocked")


def unblock_user(db, user_id):
    """Unblock a user"""
    db.remove_from_blacklist(user_id)
    print(f"✅ User {user_id} unblocked")


def check_status(db, config):
    """Check current user's status"""
    # Get current user from context (would be passed by hook)
    current_user = config.get_current_user()
    
    if not current_user:
        print("❌ Cannot determine current user")
        return
    
    if db.is_whitelisted(current_user):
        print("✅ You are whitelisted")
    elif db.is_blacklisted(current_user):
        print("❌ You are blacklisted")
    elif db.has_pending_request(current_user):
        print("⏳ Your request is pending approval")
    else:
        print("📝 You have not requested access yet")


def withdraw_request(db, config):
    """Withdraw pending request"""
    current_user = config.get_current_user()
    
    if not current_user:
        print("❌ Cannot determine current user")
        return
    
    db.withdraw_request(current_user)
    print("✅ Request withdrawn")


def handle_config(config, args):
    """Handle configuration commands"""
    if not args:
        print("Config commands:")
        print("  set-owner <user_id>  - Set owner user ID")
        print("  show                 - Show current config")
        return
    
    subcommand = args[0]
    
    if subcommand == 'set-owner':
        if len(args) < 2:
            print("❌ user_id required")
            return
        config.set_owner(args[1])
        print(f"✅ Owner set to {args[1]}")
    elif subcommand == 'show':
        config.show()
    else:
        print(f"❌ Unknown config command: {subcommand}")


if __name__ == '__main__':
    main()

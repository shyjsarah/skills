#!/usr/bin/env python3
"""
Notification Manager for Bot Gatekeeper
Sends notifications to users and owners
"""

import subprocess
import sys


def send_to_user(user_id, message):
    """Send message to user"""
    # This would integrate with the messaging platform
    # For now, just log it
    print(f"📤 Sending to {user_id}: {message}")
    
    # TODO: Implement actual notification via OpenClaw message API
    # Example:
    # subprocess.run([
    #     'openclaw', 'message', 'send',
    #     '--target', user_id,
    #     '--message', message
    # ])


def send_to_owner(owner_id, message):
    """Send message to owner"""
    print(f"📤 Sending to owner {owner_id}: {message}")
    
    # TODO: Implement actual notification
    # Could use:
    # - Feishu/Telegram message
    # - Email
    # - SMS
    # - Webhook


def notify_new_request(owner_id, user_id, message):
    """Notify owner of new access request"""
    notification = f"""
🔔 New Access Request

User: {user_id}
Message: "{message[:100]}..."

Approve: python3 main.py approve {user_id}
Reject: python3 main.py reject {user_id}
"""
    send_to_owner(owner_id, notification)

#!/usr/bin/env python3
"""
Bot Gatekeeper Hook for OpenClaw
Intercepts messages and checks access control
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from db_manager import DatabaseManager
from config_manager import ConfigManager
from notification import notify_new_request


def handle_message(message, context):
    """
    Handle incoming message
    
    Args:
        message: Message object with sender_id, content, etc.
        context: Context object with channel info
    
    Returns:
        dict with action and message
    """
    db = DatabaseManager()
    db.initialize()
    
    config = ConfigManager()
    
    user_id = message.get('sender_id')
    channel_id = message.get('chat_id')
    content = message.get('content', '')
    
    # Owner always has access
    if config.is_owner(user_id):
        return {'action': 'allow'}
    
    # Check whitelist
    if db.is_whitelisted(user_id):
        return {'action': 'allow'}
    
    # Check blacklist
    if db.is_blacklisted(user_id):
        return {
            'action': 'deny',
            'message': config.get_rejection_message()
        }
    
    # Check if has pending request
    if db.has_pending_request(user_id):
        return {
            'action': 'deny',
            'message': config.get_pending_message()
        }
    
    # Check auto-approve rules
    user_info = {
        'user_id': user_id,
        'email': context.get('user_email', '')
    }
    
    auto_approve, reason = config.should_auto_approve(user_info)
    if auto_approve:
        db.add_to_whitelist(user_id, 'auto', reason)
        return {'action': 'allow'}
    
    # Create approval request
    request_id = db.create_request(user_id, channel_id, content)
    
    # Notify owner
    if config.should_notify_owner():
        notify_new_request(config.owner_id, user_id, content)
    
    return {
        'action': 'deny',
        'message': config.get_pending_message()
    }


# OpenClaw Hook entry point
def on_message_received(message, context):
    """OpenClaw message hook"""
    result = handle_message(message, context)
    
    if result['action'] == 'allow':
        # Allow message to proceed
        return None  # None means continue processing
    else:
        # Deny and send message
        return {
            'reply': result['message']
        }


if __name__ == '__main__':
    # Test mode
    test_message = {
        'sender_id': 'ou_test123',
        'chat_id': 'ch_test456',
        'content': 'Hello!'
    }
    
    test_context = {
        'user_email': 'test@example.com'
    }
    
    result = handle_message(test_message, test_context)
    print(f"Result: {result}")

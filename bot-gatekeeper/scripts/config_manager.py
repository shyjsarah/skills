#!/usr/bin/env python3
"""
Configuration Manager for Bot Gatekeeper
Handles configuration file operations
"""

import json
from pathlib import Path


class ConfigManager:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        self.config_path = config_path
        self.config = self._load()
        
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load(self):
        """Load configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                'owner_id': None,
                'auto_approve_patterns': [],
                'rejection_message': 'Access denied. You need owner approval to use this bot.',
                'pending_message': 'Your request has been sent to the owner for approval. Please wait.',
                'notify_owner': True,
                'whitelist': [],
                'blacklist': []
            }
    
    def _save(self):
        """Save configuration"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def is_owner(self, user_id=None):
        """Check if user is owner"""
        if user_id is None:
            # Check if current user (from env) is owner
            import os
            current_user = os.environ.get('BOT_GATEKEEPER_CURRENT_USER')
            return current_user == self.config.get('owner_id')
        
        return user_id == self.config.get('owner_id')
    
    def set_owner(self, user_id):
        """Set owner user ID"""
        self.config['owner_id'] = user_id
        self._save()
    
    @property
    def owner_id(self):
        """Get owner ID"""
        return self.config.get('owner_id')
    
    def get_current_user(self):
        """Get current user from environment"""
        import os
        return os.environ.get('BOT_GATEKEEPER_CURRENT_USER')
    
    def set_current_user(self, user_id):
        """Set current user (for testing)"""
        import os
        os.environ['BOT_GATEKEEPER_CURRENT_USER'] = user_id
    
    def should_auto_approve(self, user_info):
        """Check if user should be auto-approved"""
        patterns = self.config.get('auto_approve_patterns', [])
        
        for pattern in patterns:
            pattern_type = pattern.get('type')
            pattern_value = pattern.get('value')
            
            if pattern_type == 'email_domain':
                # Check if user email ends with domain
                user_email = user_info.get('email', '')
                if user_email.endswith(pattern_value):
                    return True, pattern.get('description', '')
            
            elif pattern_type == 'user_id_prefix':
                # Check if user ID starts with prefix
                user_id = user_info.get('user_id', '')
                if user_id.startswith(pattern_value):
                    return True, pattern.get('description', '')
        
        return False, ''
    
    def get_rejection_message(self):
        """Get rejection message"""
        return self.config.get('rejection_message', 'Access denied.')
    
    def get_pending_message(self):
        """Get pending message"""
        return self.config.get('pending_message', 'Request sent for approval.')
    
    def should_notify_owner(self):
        """Check if owner should be notified"""
        return self.config.get('notify_owner', True)
    
    def add_to_whitelist(self, user_id):
        """Add user to config whitelist"""
        if 'whitelist' not in self.config:
            self.config['whitelist'] = []
        
        if user_id not in self.config['whitelist']:
            self.config['whitelist'].append(user_id)
            self._save()
    
    def remove_from_whitelist(self, user_id):
        """Remove user from config whitelist"""
        if 'whitelist' in self.config:
            if user_id in self.config['whitelist']:
                self.config['whitelist'].remove(user_id)
                self._save()
    
    def add_to_blacklist(self, user_id):
        """Add user to config blacklist"""
        if 'blacklist' not in self.config:
            self.config['blacklist'] = []
        
        if user_id not in self.config['blacklist']:
            self.config['blacklist'].append(user_id)
            self._save()
    
    def remove_from_blacklist(self, user_id):
        """Remove user from config blacklist"""
        if 'blacklist' in self.config:
            if user_id in self.config['blacklist']:
                self.config['blacklist'].remove(user_id)
                self._save()
    
    def show(self):
        """Show current configuration"""
        print("Current Configuration:")
        print(f"  Owner: {self.config.get('owner_id', 'Not set')}")
        print(f"  Auto-approve patterns: {len(self.config.get('auto_approve_patterns', []))}")
        print(f"  Notify owner: {self.config.get('notify_owner', True)}")
        print(f"  Whitelist: {len(self.config.get('whitelist', []))} users")
        print(f"  Blacklist: {len(self.config.get('blacklist', []))} users")

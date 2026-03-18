#!/usr/bin/env python3
"""
Database Manager for Bot Gatekeeper
Handles SQLite database operations
"""

import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'data' / 'bot-gatekeeper.db'
        
        self.db_path = db_path
        self.conn = None
        
        # Ensure data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def initialize(self):
        """Initialize database schema"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create whitelist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whitelist (
                user_id TEXT PRIMARY KEY,
                approved_by TEXT,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason TEXT,
                expires_at TIMESTAMP
            )
        ''')
        
        # Create blacklist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                user_id TEXT PRIMARY KEY,
                blocked_by TEXT,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason TEXT
            )
        ''')
        
        # Create approval_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approval_requests (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                channel_id TEXT,
                message TEXT,
                status TEXT CHECK(status IN ('pending', 'approved', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TIMESTAMP,
                reviewed_by TEXT,
                review_comment TEXT
            )
        ''')
        
        # Create audit_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                user_id TEXT,
                actor_id TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_requests_status ON approval_requests(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_requests_user ON approval_requests(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id)')
        
        conn.commit()
        self.close()
    
    def is_whitelisted(self, user_id):
        """Check if user is whitelisted"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM whitelist WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        self.close()
        return result is not None
    
    def is_blacklisted(self, user_id):
        """Check if user is blacklisted"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM blacklist WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        self.close()
        return result is not None
    
    def has_pending_request(self, user_id):
        """Check if user has pending request"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM approval_requests WHERE user_id = ? AND status = ?', 
                      (user_id, 'pending'))
        result = cursor.fetchone()
        
        self.close()
        return result is not None
    
    def add_to_whitelist(self, user_id, approved_by, reason=''):
        """Add user to whitelist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO whitelist (user_id, approved_by, approved_at, reason)
            VALUES (?, ?, ?, ?)
        ''', (user_id, approved_by, datetime.now(), reason))
        
        self._log_audit('whitelist_add', user_id, approved_by, f'Reason: {reason}')
        
        conn.commit()
        self.close()
    
    def remove_from_whitelist(self, user_id):
        """Remove user from whitelist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM whitelist WHERE user_id = ?', (user_id,))
        
        conn.commit()
        self.close()
    
    def add_to_blacklist(self, user_id, blocked_by, reason=''):
        """Add user to blacklist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO blacklist (user_id, blocked_by, blocked_at, reason)
            VALUES (?, ?, ?, ?)
        ''', (user_id, blocked_by, datetime.now(), reason))
        
        self._log_audit('blacklist_add', user_id, blocked_by, f'Reason: {reason}')
        
        conn.commit()
        self.close()
    
    def remove_from_blacklist(self, user_id):
        """Remove user from blacklist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM blacklist WHERE user_id = ?', (user_id,))
        
        conn.commit()
        self.close()
    
    def create_request(self, user_id, channel_id, message):
        """Create approval request"""
        import uuid
        request_id = str(uuid.uuid4())
        
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO approval_requests (id, user_id, channel_id, message, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (request_id, user_id, channel_id, message))
        
        self._log_audit('request_create', user_id, user_id, f'Channel: {channel_id}')
        
        conn.commit()
        self.close()
        return request_id
    
    def update_request_status(self, user_id, status, reviewed_by, comment=''):
        """Update request status"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE approval_requests 
            SET status = ?, reviewed_at = ?, reviewed_by = ?, review_comment = ?
            WHERE user_id = ? AND status = 'pending'
        ''', (status, datetime.now(), reviewed_by, comment, user_id))
        
        self._log_audit(f'request_{status}', user_id, reviewed_by, comment)
        
        conn.commit()
        self.close()
    
    def get_pending_requests(self, user_id=None):
        """Get pending requests"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM approval_requests 
                WHERE user_id = ? AND status = 'pending'
                ORDER BY created_at DESC
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT * FROM approval_requests 
                WHERE status = 'pending'
                ORDER BY created_at DESC
            ''')
        
        results = [dict(row) for row in cursor.fetchall()]
        self.close()
        return results
    
    def get_whitelist(self):
        """Get all whitelisted users"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM whitelist ORDER BY approved_at DESC')
        results = [dict(row) for row in cursor.fetchall()]
        
        self.close()
        return results
    
    def get_blacklist(self):
        """Get all blacklisted users"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM blacklist ORDER BY blocked_at DESC')
        results = [dict(row) for row in cursor.fetchall()]
        
        self.close()
        return results
    
    def withdraw_request(self, user_id):
        """Withdraw pending request"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM approval_requests 
            WHERE user_id = ? AND status = 'pending'
        ''', (user_id,))
        
        self._log_audit('request_withdraw', user_id, user_id)
        
        conn.commit()
        self.close()
    
    def _log_audit(self, action, user_id, actor_id, details=''):
        """Log audit entry"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (action, user_id, actor_id, details)
            VALUES (?, ?, ?, ?)
        ''', (action, user_id, actor_id, details))
        
        conn.commit()
        self.close()

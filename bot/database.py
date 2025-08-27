import sqlite3
import asyncio
from typing import Optional, List, Dict
import json
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Groups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                welcome_message TEXT,
                goodbye_message TEXT,
                rules TEXT,
                anti_spam BOOLEAN DEFAULT TRUE,
                anti_flood BOOLEAN DEFAULT TRUE,
                anti_nsfw BOOLEAN DEFAULT TRUE,
                link_blocking BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language_code TEXT,
                is_bot BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Group members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                status TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                left_at TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups (chat_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Warnings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                reason TEXT,
                warned_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups (chat_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Banned users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS banned_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                reason TEXT,
                banned_by INTEGER,
                ban_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups (chat_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Muted users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS muted_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                muted_by INTEGER,
                mute_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups (chat_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Group statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                date DATE,
                messages_count INTEGER DEFAULT 0,
                new_members INTEGER DEFAULT 0,
                left_members INTEGER DEFAULT 0,
                FOREIGN KEY (chat_id) REFERENCES groups (chat_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_group(self, chat_id: int, title: str) -> bool:
        """Add a new group to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO groups (chat_id, title) VALUES (?, ?)',
                (chat_id, title)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding group: {e}")
            return False
    
    def get_group_settings(self, chat_id: int) -> Optional[Dict]:
        """Get group settings"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE chat_id = ?', (chat_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'chat_id': result[0],
                    'title': result[1],
                    'language': result[2],
                    'welcome_message': result[3],
                    'goodbye_message': result[4],
                    'rules': result[5],
                    'anti_spam': result[6],
                    'anti_flood': result[7],
                    'anti_nsfw': result[8],
                    'link_blocking': result[9]
                }
            return None
        except Exception as e:
            print(f"Error getting group settings: {e}")
            return None
    
    def add_warning(self, chat_id: int, user_id: int, reason: str, warned_by: int) -> bool:
        """Add warning to user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO warnings (chat_id, user_id, reason, warned_by) VALUES (?, ?, ?, ?)',
                (chat_id, user_id, reason, warned_by)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding warning: {e}")
            return False
    
    def get_warnings_count(self, chat_id: int, user_id: int) -> int:
        """Get user warnings count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) FROM warnings WHERE chat_id = ? AND user_id = ?',
                (chat_id, user_id)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting warnings count: {e}")
            return 0

db = Database('data/database.db')

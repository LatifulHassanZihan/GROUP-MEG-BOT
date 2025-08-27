import os
from typing import Dict, List

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    BOT_USERNAME = '@group_meg_bot'
    BOT_NAME = 'GROUP MEG 🇵🇸'
    
    # Developer Information
    DEVELOPER_NAME = "Latiful Hassan Zihan 🇵🇸"
    DEVELOPER_USERNAME = "@alwayszihan"
    DEVELOPER_NATIONALITY = "Bangladeshi 🇧🇩"
    DEVELOPER_ID = 123456789  # Replace with actual developer ID
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'data/database.db')
    
    # Webhook Configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    PORT = int(os.getenv('PORT', 8443))
    
    # Anti-spam settings
    FLOOD_LIMIT = 5  # Messages per minute
    WARNING_THRESHOLD = 3
    AUTO_BAN_AFTER_WARNINGS = True
    
    # Default settings
    DEFAULT_LANGUAGE = 'en'
    SUPPORTED_LANGUAGES = ['en', 'bn']
    
    # Admin IDs (Super admins)
    SUPER_ADMINS: List[int] = [DEVELOPER_ID]
                              

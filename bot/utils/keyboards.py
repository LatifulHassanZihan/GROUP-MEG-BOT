from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    @staticmethod
    def main_menu():
        """Main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🏠 Add to Group", url="https://t.me/group_meg_bot?startgroup=true"),
                InlineKeyboardButton("📊 Add to Channel", url="https://t.me/group_meg_bot?startchannel=true")
            ],
            [
                InlineKeyboardButton("🤖 Commands", callback_data="commands"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ],
            [
                InlineKeyboardButton("👨‍💻 Developer", callback_data="developer"),
                InlineKeyboardButton("📋 Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
                InlineKeyboardButton("📈 Stats", callback_data="stats")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_menu():
        """Admin commands menu"""
        keyboard = [
            [
                InlineKeyboardButton("👤 Member Management", callback_data="member_mgmt"),
                InlineKeyboardButton("⚠️ Warnings", callback_data="warnings")
            ],
            [
                InlineKeyboardButton("🔇 Mute/Unmute", callback_data="mute_menu"),
                InlineKeyboardButton("🚫 Ban/Unban", callback_data="ban_menu")
            ],
            [
                InlineKeyboardButton("🧹 Purge Messages", callback_data="purge"),
                InlineKeyboardButton("🛡️ Anti-Spam", callback_data="antispam")
            ],
            [
                InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def settings_menu():
        """Settings menu"""
        keyboard = [
            [
                InlineKeyboardButton("👋 Welcome/Goodbye", callback_data="welcome_settings"),
                InlineKeyboardButton("📏 Group Rules", callback_data="rules_settings")
            ],
            [
                InlineKeyboardButton("🌐 Language", callback_data="language_settings"),
                InlineKeyboardButton("🔗 Link Control", callback_data="link_settings")
            ],
            [
                InlineKeyboardButton("🛡️ Moderation", callback_data="mod_settings"),
                InlineKeyboardButton("📊 Analytics", callback_data="analytics_settings")
            ],
            [
                InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_action(action: str, target_id: str):
        """Confirmation keyboard for destructive actions"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{action}_{target_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_action")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
      

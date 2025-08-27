from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.keyboards import Keyboards
from bot.config import Config
from bot.database import db

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat = update.effective_chat
    
    if chat.type == 'private':
        welcome_text = f"""
🇵🇸 **Welcome to {Config.BOT_NAME}!** 🇵🇸

🤖 **Advanced Group Management Bot**

✨ **Features:**
• 👥 Complete member management
• 🛡️ Advanced anti-spam protection  
• 📊 Detailed analytics & statistics
• 🌐 Multi-language support (EN/BN)
• ⚙️ Customizable settings
• 🚀 Lightning-fast performance

**Choose an option below:**
        """
        await update.message.reply_text(
            welcome_text,
            reply_markup=Keyboards.main_menu(),
            parse_mode='Markdown'
        )
    else:
        # Group start
        db.add_group(chat.id, chat.title)
        await update.message.reply_text(
            f"🎉 **{Config.BOT_NAME} is now active in {chat.title}!**\n\n"
            "🔧 Use /settings to configure the bot\n"
            "📋 Use /help to see available commands\n"
            "👨‍💻 Use /developer for creator info",
            parse_mode='Markdown'
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = f"""
📋 **{Config.BOT_NAME} - Command List**

🚀 **Basic Commands:**
• `/start` - Start the bot & show welcome
• `/help` - Show this help message  
• `/about` - Bot information
• `/rules` - Display group rules
• `/settings` - Open admin settings panel

👨‍💻 **Admin Commands:**
• `/kick [reply]` - Kick user from group
• `/ban [reply]` - Ban user permanently
• `/unban <user_id>` - Unban user by ID
• `/mute <seconds> [reply]` - Mute user temporarily
• `/unmute [reply]` - Unmute user
• `/warn [reply + reason]` - Add warning to user
• `/warnings [reply]` - Show user warnings
• `/purge` - Delete recent messages batch

⚙️ **Configuration:**
• `/setwelcome <text>` - Set welcome message
• `/setgoodbye <text>` - Set goodbye message  
• `/setrules <text>` - Set group rules
• `/language <code>` - Set bot language

📊 **Info Commands:**
• `/info [reply]` - Show user detailed info
• `/stats` - Show group statistics
• `/roles` - Display all available roles
• `/admins` - List group administrators

🛡️ **Moderation:**
• `/lock` - 🔒 Lock group (admin only messaging)
• `/unlock` - 🔓 Unlock group  
• `/restrict [reply/user_id]` - Restrict user
• `/clearwarns [reply]` - Clear user warnings
• `/detectspam` - Scan & delete spam messages
• `/antispam on|off` - Enable/disable anti-spam
• `/antiflood on|off` - Enable/disable anti-flood

👥 **Member Management:**
• `/promote [reply/user_id]` - Promote to admin
• `/demote [reply/user_id]` - Demote to member
• `/listmembers` - List all group members
• `/inactive` - List inactive users
• `/profile [reply]` - Show user profile

💾 **Data Management:**
• `/backup` - Export group settings & data
• `/restore <file>` - Restore from backup
• `/exportroles` - Export user roles as CSV
• `/exportrules` - Export group rules

🎉 **Fun Commands:**
• `/quote` - Get motivational quote
• `/poll <question>` - Create group poll
• `/joke` - Tell a random joke
• `/cat` - Share random cat picture

🆘 **Support:**
• `/contactadmin` - Call admins for help
• `/adminhelp` - List admin commands
• `/report [reply]` - Report message to admins

**Developer:** {Config.DEVELOPER_NAME}
**Contact:** {Config.DEVELOPER_USERNAME}
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_text = f"""
🤖 **About {Config.BOT_NAME}**

📝 **Description:**
Advanced Telegram group management bot with comprehensive moderation tools, analytics, and customization options.

⭐ **Version:** 2.0.0
🔧 **Built with:** Python + python-telegram-bot
🌐 **Languages:** English, বাংলা

👨‍💻 **Developer Information:**
• **Name:** {Config.DEVELOPER_NAME}
• **Username:** {Config.DEVELOPER_USERNAME} 
• **Nationality:** {Config.DEVELOPER_NATIONALITY}

🚀 **Features:**
✅ Advanced member management
✅ Smart anti-spam detection
✅ Customizable welcome/goodbye
✅ Warning & punishment system  
✅ Real-time analytics
✅ Multi-language support
✅ Role-based permissions
✅ Content filtering
✅ Automated moderation
✅ Data backup & restore

💝 **Free & Open Source**
This bot is completely free to use!

🔗 **Support:** Contact {Config.DEVELOPER_USERNAME}
    """
    
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def developer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /developer command"""
    dev_text = f"""
👨‍💻 **Developer Information**

🇵🇸 **{Config.DEVELOPER_NAME}** 🇵🇸
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎯 **Username:** {Config.DEVELOPER_USERNAME}
┃ 🌍 **Nationality:** {Config.DEVELOPER_NATIONALITY}  
┃ 💻 **Specialization:** Bot Development
┃ 🛠️ **Tech Stack:** Python, Telegram API
┃ 🚀 **Project:** {Config.BOT_NAME}
┗━━━━━━━━━━━━━━━━━━━━━━┛

📞 **Contact Methods:**
• Telegram: {Config.DEVELOPER_USERNAME}
• Bot Support: Use /contactadmin
• Bug Reports: Message developer directly

🎯 **Skills:**
• 🐍 Python Programming
• 🤖 Telegram Bot Development  
• 🗄️ Database Management
• 🔧 System Administration
• 📊 Data Analytics

💡 **About this Bot:**
This bot was developed to provide comprehensive group management solutions for Telegram communities. It includes advanced moderation, analytics, and customization features.

🙏 **Support the Developer:**
If you find this bot helpful, please:
• ⭐ Star the project
• 📢 Share with friends
• 💬 Provide feedback
• 🐛 Report bugs

**Made with ❤️ in Bangladesh 🇧🇩**
    """
    
    await update.message.reply_text(dev_text, parse_mode='Markdown')

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rules command"""
    chat = update.effective_chat
    
    if chat.type == 'private':
        await update.message.reply_text("⚠️ This command works in groups only!")
        return
    
    settings = db.get_group_settings(chat.id)
    
    if settings and settings.get('rules'):
        rules_text = f"📋 **{chat.title} - Group Rules**\n\n{settings['rules']}"
    else:
        rules_text = f"""
📋 **{chat.title} - Default Rules**

1️⃣ **Be respectful** - No harassment, hate speech, or discrimination
2️⃣ **No spam** - Avoid excessive posting or promotional content  
3️⃣ **Stay on topic** - Keep discussions relevant to the group
4️⃣ **No NSFW content** - Keep the group family-friendly
5️⃣ **Follow Telegram ToS** - Respect Telegram's terms of service
6️⃣ **Listen to admins** - Follow moderator instructions
7️⃣ **Use common sense** - Think before you post

⚠️ **Violations may result in:**
• Warning ⚠️
• Temporary mute 🔇
• Permanent ban 🚫

**Admins can customize these rules using /setrules**
        """
    
    await update.message.reply_text(rules_text, parse_mode='Markdown')
  

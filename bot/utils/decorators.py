from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import Config

def admin_required(func):
    """Decorator to check if user is admin"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        chat = update.effective_chat
        
        # Check if user is super admin
        if user.id in Config.SUPER_ADMINS:
            return await func(update, context)
        
        # Check if user is chat admin
        if chat.type in ['group', 'supergroup']:
            chat_member = await context.bot.get_chat_member(chat.id, user.id)
            if chat_member.status in ['creator', 'administrator']:
                return await func(update, context)
        
        await update.message.reply_text("❌ You don't have permission to use this command!")
        return None
    return wrapper

def group_only(func):
    """Decorator to restrict commands to groups only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        if chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("⚠️ This command can only be used in groups!")
            return None
        return await func(update, context)
    return wrapper

def private_only(func):
    """Decorator to restrict commands to private chats only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        if chat.type != 'private':
            await update.message.reply_text("⚠️ This command can only be used in private chat!")
            return None
        return await func(update, context)
    return wrapper

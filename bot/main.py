import logging
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.config import Config
from bot.handlers.basic_commands import *
from bot.handlers.admin_commands import *
from bot.utils.keyboards import Keyboards

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text(
            f"🏠 **{Config.BOT_NAME} - Main Menu**\n\n"
            "Choose an option below:",
            reply_markup=Keyboards.main_menu(),
            parse_mode='Markdown'
        )
    elif data == "commands":
        await help_command(update, context)
    elif data == "about":
        await about_command(update, context)
    elif data == "developer":
        await developer_command(update, context)
    elif data == "settings":
        await query.edit_message_text(
            "⚙️ **Settings Panel**\n\nChoose a category:",
            reply_markup=Keyboards.settings_menu(),
            parse_mode='Markdown'
        )

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Basic commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("developer", developer_command))
    application.add_handler(CommandHandler("rules", rules_command))
    
    # Admin commands
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("purge", purge_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start bot
    if Config.WEBHOOK_URL:
        # Webhook mode for production
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            webhook_url=Config.WEBHOOK_URL
        )
    else:
        # Polling mode for development
        application.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    main()

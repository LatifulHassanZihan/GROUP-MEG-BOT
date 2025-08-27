from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators import admin_required, group_only
from bot.database import db
from bot.config import Config
from datetime import datetime, timedelta
import re

@admin_required
@group_only
async def kick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kick user from group"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to kick the user!")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    
    if target_user.id in Config.SUPER_ADMINS:
        await update.message.reply_text("❌ Cannot kick bot developer!")
        return
    
    try:
        await context.bot.ban_chat_member(chat.id, target_user.id)
        await context.bot.unban_chat_member(chat.id, target_user.id)
        
        await update.message.reply_text(
            f"👢 **User kicked successfully!**\n\n"
            f"👤 **User:** {target_user.mention_html()}\n"
            f"🆔 **ID:** `{target_user.id}`\n"
            f"👨‍💼 **Kicked by:** {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to kick user: {str(e)}")

@admin_required
@group_only  
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban user permanently"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to ban the user!")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    
    if target_user.id in Config.SUPER_ADMINS:
        await update.message.reply_text("❌ Cannot ban bot developer!")
        return
    
    reason = " ".join(context.args) if context.args else "No reason provided"
    
    try:
        await context.bot.ban_chat_member(chat.id, target_user.id)
        
        # Add to database
        db.add_ban(chat.id, target_user.id, reason, update.effective_user.id)
        
        await update.message.reply_text(
            f"🚫 **User banned permanently!**\n\n"
            f"👤 **User:** {target_user.mention_html()}\n"
            f"🆔 **ID:** `{target_user.id}`\n"
            f"📝 **Reason:** {reason}\n"
            f"👨‍💼 **Banned by:** {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to ban user: {str(e)}")

@admin_required
@group_only
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban user by ID"""
    if not context.args:
        await update.message.reply_text("❌ Please provide user ID: `/unban <user_id>`", parse_mode='Markdown')
        return
    
    try:
        user_id = int(context.args[0])
        chat = update.effective_chat
        
        await context.bot.unban_chat_member(chat.id, user_id)
        
        await update.message.reply_text(
            f"✅ **User unbanned successfully!**\n\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"👨‍💼 **Unbanned by:** {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID format!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unban user: {str(e)}")

@admin_required
@group_only
async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute user temporarily"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to mute the user!")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    
    # Parse duration
    duration = 60  # Default 1 minute
    if context.args:
        try:
            duration = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Invalid duration! Use seconds (e.g., 300 for 5 minutes)")
            return
    
    until_date = datetime.now() + timedelta(seconds=duration)
    
    try:
        await context.bot.restrict_chat_member(
            chat.id,
            target_user.id,
            permissions={'can_send_messages': False},
            until_date=until_date
        )
        
        # Convert duration to human readable
        if duration < 60:
            duration_str = f"{duration} seconds"
        elif duration < 3600:
            duration_str = f"{duration // 60} minutes"
        else:
            duration_str = f"{duration // 3600} hours"
        
        await update.message.reply_text(
            f"🔇 **User muted successfully!**\n\n"
            f"👤 **User:** {target_user.mention_html()}\n"
            f"⏰ **Duration:** {duration_str}\n"
            f"📅 **Until:** {until_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"👨‍💼 **Muted by:** {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to mute user: {str(e)}")

@admin_required
@group_only
async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unmute user"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to unmute the user!")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    
    try:
        await context.bot.restrict_chat_member(
            chat.id,
            target_user.id,
            permissions={
                'can_send_messages': True,
                'can_send_media_messages': True,
                'can_send_other_messages': True,
                'can_add_web_page_previews': True
            }
        )
        
        await update.message.reply_text(
            f"🔊 **User unmuted successfully!**\n\n"
            f"👤 **User:** {target_user.mention_html()}\n"
            f"👨‍💼 **Unmuted by:** {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unmute user: {str(e)}")

@admin_required
@group_only
async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add warning to user"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to warn the user!")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    reason = " ".join(context.args) if context.args else "No reason provided"
    
    # Add warning to database
    db.add_warning(chat.id, target_user.id, reason, update.effective_user.id)
    warnings_count = db.get_warnings_count(chat.id, target_user.id)
    
    await update.message.reply_text(
        f"⚠️ **User warned!**\n\n"
        f"👤 **User:** {target_user.mention_html()}\n"
        f"📝 **Reason:** {reason}\n"
        f"📊 **Warnings:** {warnings_count}/{Config.WARNING_THRESHOLD}\n"
        f"👨‍💼 **Warned by:** {update.effective_user.mention_html()}",
        parse_mode='HTML'
    )
    
    # Auto-ban if threshold reached
    if warnings_count >= Config.WARNING_THRESHOLD and Config.AUTO_BAN_AFTER_WARNINGS:
        try:
            await context.bot.ban_chat_member(chat.id, target_user.id)
            await update.message.reply_text(
                f"🚫 **Auto-ban triggered!**\n\n"
                f"👤 **User:** {target_user.mention_html()}\n"
                f"📊 **Reason:** Reached warning threshold ({Config.WARNING_THRESHOLD})",
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Auto-ban failed: {e}")

@admin_required
@group_only
async def purge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete batch of recent messages"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a message to start purging from!")
        return
    
    chat = update.effective_chat
    start_msg_id = update.message.reply_to_message.message_id
    end_msg_id = update.message.message_id
    
    deleted_count = 0
    
    try:
        for msg_id in range(start_msg_id, end_msg_id):
            try:
                await context.bot.delete_message(chat.id, msg_id)
                deleted_count += 1
            except:
                continue
        
        # Delete the purge command message
        await context.bot.delete_message(chat.id, update.message.message_id)
        
        # Send confirmation (will auto-delete after 5 seconds)
        msg = await context.bot.send_message(
            chat.id,
            f"🧹 **Purged {deleted_count} messages**",
            parse_mode='Markdown'
        )
        
        # Schedule message deletion
        context.job_queue.run_once(
            lambda c: c.bot.delete_message(chat.id, msg.message_id),
            5
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to purge messages: {str(e)}")

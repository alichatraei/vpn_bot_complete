#!/usr/bin/env python3
# 🚀 VPN Bot - Main Entry Point

import os
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)

# Import handlers
from bot_handlers import (
    start, services, my_account, help_command, contact,
    button_callback, handle_message
)
from admin_handlers import (
    admin_start, admin_callback, handle_broadcast_message
)
from config import BOT_TOKEN, ADMIN_ID

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== ERROR HANDLER ==========

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت خطاها"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# ========== MAIN FUNCTION ==========

def main():
    """ایجاد بات و شروع آن"""
    
    # بررسی Token
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN یافت نشد! لطفاً متغیر محیطی تنظیم کنید.")
        return
    
    if ADMIN_ID == 0:
        logger.error("❌ ADMIN_ID یافت نشد! لطفاً متغیر محیطی تنظیم کنید.")
        return
    
    logger.info("🚀 بات در حال شروع...")
    
    # ایجاد Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ===== COMMAND HANDLERS =====
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_start))
    
    # ===== MESSAGE HANDLERS =====
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # ===== CALLBACK HANDLERS =====
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CallbackQueryHandler(admin_callback))
    
    # ===== ERROR HANDLER =====
    application.add_error_handler(error_handler)
    
    logger.info("✅ بات آماده است!")
    logger.info(f"📱 ادمین: {ADMIN_ID}")
    
    # شروع بات
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

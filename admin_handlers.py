# 👨‍💼 Admin Handlers - پنل مدیریتی

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import db
from config import ADMIN_IDS, ADMIN_MESSAGES
from utils import (
    format_price, get_admin_keyboard, create_user_list_text,
    create_payment_list_text, get_stats_text
)
from datetime import datetime

# State Handlers
CHOOSING_ACTION = 1
CONFIRM_PAYMENT = 2
BROADCAST_MESSAGE = 3

def is_admin(user_id):
    """بررسی اینکه کاربر ادمین است یا نه"""
    return user_id in ADMIN_IDS

# ========== ADMIN START ==========

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع پنل ادمین"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ شما دسترسی ندارید.")
        return
    
    text = """👨‍💼 **پنل مدیریتی**

خوش آمدید به پنل ادمین!

بر روی یکی از گزینه‌های زیر کلیک کنید:
"""
    
    keyboard = [
        [InlineKeyboardButton("📊 آمار", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 کاربران", callback_data="admin_users")],
        [InlineKeyboardButton("💰 پرداخت‌ها", callback_data="admin_payments")],
        [InlineKeyboardButton("📢 پیام همگانی", callback_data="admin_broadcast")],
        [InlineKeyboardButton("⚙️ سرویس‌ها", callback_data="admin_services")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# ========== STATS ==========

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ندارید.")
        return
    
    total_users = db.get_user_count()
    active_users = len([u for u in db.get_all_users() if u.get('service_type')])
    pending_payments = len(db.get_pending_payments())
    today_income = db.get_today_income()
    total_income = db.get_total_income()
    
    daily_average = total_income // max(1, (datetime.now() - datetime.fromisoformat("2024-01-01")).days)
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'pending_payments': pending_payments,
        'today_income': today_income,
        'total_income': total_income,
        'daily_average': daily_average
    }
    
    text = get_stats_text(stats)
    
    keyboard = [
        [InlineKeyboardButton("🔄 بروزرسانی", callback_data="admin_stats")],
        [InlineKeyboardButton("◀️ بازگشت", callback_data="admin_back")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ========== USERS ==========

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کاربران"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ندارید.")
        return
    
    users = db.get_all_users()
    text = create_user_list_text(users)
    
    keyboard = [
        [InlineKeyboardButton(f"👥 کل: {len(users)}", callback_data="noop")],
        [InlineKeyboardButton("🔍 جستجو", callback_data="admin_search_user")],
        [InlineKeyboardButton("🗑️ حذف کاربر", callback_data="admin_delete_user")],
        [InlineKeyboardButton("◀️ بازگشت", callback_data="admin_back")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ========== PAYMENTS ==========

async def admin_payments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پرداخت‌ها"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ندارید.")
        return
    
    pending_payments = db.get_pending_payments()
    text = create_payment_list_text(pending_payments)
    
    keyboard = []
    
    for payment in pending_payments[:5]:
        keyboard.append([
            InlineKeyboardButton(
                f"✅ ID:{payment['id']}", 
                callback_data=f"admin_confirm_payment_{payment['id']}"
            )
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("🔄 بروزرسانی", callback_data="admin_payments")],
        [InlineKeyboardButton("◀️ بازگشت", callback_data="admin_back")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ========== CONFIRM PAYMENT ==========

async def admin_confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تایید پرداخت"""
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("❌ دسترسی رد شد", show_alert=True)
        return
    
    payment_id = int(query.data.replace("admin_confirm_payment_", ""))
    payment = db.get_payment(payment_id)
    
    if not payment:
        await query.answer("❌ پرداخت پیدا نشد", show_alert=True)
        return
    
    # تایید پرداخت
    db.confirm_payment(payment_id)
    db.add_admin_log(query.from_user.id, "confirm_payment", f"Payment ID: {payment_id}")
    
    user = db.get_user(payment['user_id'])
    service_names = {
        'basic': '🔓 نامحدود پایه',
        'premium': '👑 نامحدود پرمیوم',
        'gigahi': '📊 تانل گیگی',
        'tunnel': '⚡ تانل پرمیوم'
    }
    
    text = f"""✅ **پرداخت تایید شد**

👤 کاربر: {user.get('first_name', '')}
📦 سرویس: {service_names.get(payment['service_type'], payment['service_type'])}
💵 مبلغ: {format_price(payment['amount'])} تومان

سرویس کاربر فعال شد ✅
"""
    
    await query.answer("✅ پرداخت تایید شد", show_alert=True)
    await query.edit_message_text(text)
    
    # ارسال پیام به کاربر
    try:
        await context.bot.send_message(
            chat_id=payment['user_id'],
            text=f"""✅ **پرداخت شما تایید شد!**

سرویس {service_names.get(payment['service_type'], payment['service_type'])} برای شما فعال شد.

🚀 اکنون می‌توانید از VPN استفاده کنید.

برای مشاهده جزئیات، بر روی /myaccount کلیک کنید.
"""
        )
    except:
        pass

# ========== BROADCAST ==========

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام همگانی"""
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("❌ دسترسی رد شد", show_alert=True)
        return
    
    await query.answer()
    
    text = """📢 **پیام همگانی**

لطفاً پیام خود را وارد کنید:

**نکات:**
• از HTML/Markdown استفاده کنید
• حداکثر 1000 کاراکتر
• پیام برای تمام کاربران ارسال خواهد شد

برای لغو، /cancel تایپ کنید.
"""
    
    context.user_data['broadcast_mode'] = True
    await query.edit_message_text(text)

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام پخش"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.user_data.get('broadcast_mode'):
        return
    
    message = update.message.text
    
    if message == "/cancel":
        context.user_data['broadcast_mode'] = False
        await update.message.reply_text("❌ عملیات لغو شد.")
        return
    
    # ارسال به تمام کاربران
    users = db.get_all_users()
    success = 0
    failed = 0
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user['user_id'],
                text=f"📢 **پیام از مدیر:**\n\n{message}"
            )
            success += 1
        except:
            failed += 1
    
    context.user_data['broadcast_mode'] = False
    
    text = f"""✅ **پیام ارسال شد**

✅ موفق: {success}
❌ ناموفق: {failed}

کل کاربران: {len(users)}
"""
    
    db.add_admin_log(update.effective_user.id, "broadcast", f"Success: {success}, Failed: {failed}")
    
    await update.message.reply_text(text)

# ========== ADMIN CALLBACK ==========

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه‌های ادمین"""
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("❌ دسترسی رد شد", show_alert=True)
        return
    
    if query.data == "admin_back":
        await admin_start(update, context)
    elif query.data == "admin_stats":
        await admin_stats(update, context)
    elif query.data == "admin_users":
        await admin_users(update, context)
    elif query.data == "admin_payments":
        await admin_payments(update, context)
    elif query.data == "noop":
        await query.answer()
    else:
        await query.answer("⚠️ دستور نامشناس", show_alert=True)

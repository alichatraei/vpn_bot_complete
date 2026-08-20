# 🤖 Bot Handlers - دستورات کاربران عادی

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from database import db
from config import MESSAGES, EMOJIS, CARD_RECEIVER
from utils import (
    format_price, get_user_account_text, get_services_keyboard,
    get_main_keyboard, create_service_text, get_payment_request_text
)

# ========== START ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user = update.effective_user
    
    # اضافه کردن کاربر به دیتابیس
    db.add_user(user.id, user.first_name, user.last_name, user.username)
    
    welcome_text = f"""🎉 **خوش آمدید {user.first_name}!**

به سرویس VPN ما خوش آمدید. ما بهترین سرویس VPN با:
  • 🚀 سرعت بالا
  • 💰 قیمت مناسب
  • 🔒 امنیت بالا
  • 🌍 سرورهای متعدد

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""
    
    reply_markup = ReplyKeyboardMarkup(
        get_main_keyboard(),
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ========== SERVICES ==========

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش سرویس‌های موجود"""
    user_id = update.effective_user.id
    
    text = """💼 **سرویس‌های موجود**

لطفاً یکی از سرویس‌های زیر را انتخاب کنید:
"""
    
    keyboard = [
        [InlineKeyboardButton("🔓 نامحدود پایه", callback_data="service_basic")],
        [InlineKeyboardButton("👑 نامحدود پرمیوم", callback_data="service_premium")],
        [InlineKeyboardButton("📊 تانل گیگی", callback_data="service_gigahi")],
        [InlineKeyboardButton("⚡ تانل پرمیوم", callback_data="service_tunnel")],
        [InlineKeyboardButton("◀️ بازگشت", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش حساب کاربری"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    text = get_user_account_text(user)
    
    keyboard = [
        [InlineKeyboardButton("🛍️ خریداری سرویس", callback_data="buy_service")],
        [InlineKeyboardButton("◀️ بازگشت", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنما"""
    text = """📖 **راهنما**

**چگونه استفاده کنم؟**

1️⃣ **سرویس انتخاب کنید** 💼
   بر روی دکمه "سرویس‌ها" کلیک کنید و سرویس مورد نظر خود را انتخاب کنید.

2️⃣ **تایید کنید** ✅
   جزئیات سرویس را بررسی کنید و "خریداری" را انتخاب کنید.

3️⃣ **پرداخت کنید** 💳
   به شماره کارت ما واریز کنید.

4️⃣ **منتظر تایید باشید** ⏰
   پس از 30 دقیقه، حساب شما فعال خواهد شد.

**سوالات متداول:**

❓ آیا VPN ایمن است؟
✅ بله، ما از رمزگذاری قوی استفاده می‌کنیم.

❓ مدت اشتراک چقدر است؟
✅ تمام سرویس‌ها برای 30 روز هستند.

❓ اگر مشکلی داشتم؟
✅ در بخش "تماس" می‌توانید با ما تماس بگیرید.

**برای سوالات بیشتر:**
📞 تماس با پشتیبانی: @VPNSupport
📧 ایمیل: support@vpn.com
"""
    
    keyboard = [[InlineKeyboardButton("◀️ بازگشت", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تماس با ما"""
    text = """📞 **تماس با ما**

**روش‌های تماس:**

📱 **تلگرام:**
@VPNSupport

📧 **ایمیل:**
support@vpn.com

☎️ **تلفن:**
09xxxxxxxxx

🕐 **ساعات کاری:**
شنبه - پنج‌شنبه | 9 صبح - 6 شام

**ما اینجایم تا کمکتان کنیم!** 💪
"""
    
    keyboard = [[InlineKeyboardButton("◀️ بازگشت", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

# ========== CALLBACK QUERIES ==========

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه‌های Inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("service_"):
        service_key = query.data.replace("service_", "")
        service = db.get_service(service_key)
        
        if service:
            text = create_service_text(service)
            
            keyboard = [
                [InlineKeyboardButton("🛍️ خریداری", callback_data=f"buy_confirm_{service_key}")],
                [InlineKeyboardButton("◀️ بازگشت", callback_data="back_services")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
    
    elif query.data.startswith("buy_confirm_"):
        service_key = query.data.replace("buy_confirm_", "")
        service = db.get_service(service_key)
        
        if service:
            user_id = query.from_user.id
            payment_id = db.add_payment(user_id, service['price'], service_key)
            
            text = f"""✅ **درخواست پرداخت ثبت شد**

📦 سرویس: {service['name']}
💵 مبلغ: {format_price(service['price'])} تومان
🔗 ID: {payment_id}

💳 **اطلاعات پرداخت:**

{CARD_RECEIVER['bank']}
نام: {CARD_RECEIVER['name']}
کارت: {CARD_RECEIVER['card_number']}
IBAN: {CARD_RECEIVER['sheba']}

📝 **مراحل:**
1. مبلغ فوق را به کارت ثبت‌شده واریز کنید
2. پیام تایید واریز خود را برای مدیر ارسال کنید
3. پس از تائید، سرویس فعال خواهد شد

⏰ معمولاً تا 30 دقیقه فعال می‌شود.

سوالی دارید؟ با پشتیبانی تماس بگیرید.
"""
            
            keyboard = [
                [InlineKeyboardButton("💬 تایید پرداخت", callback_data=f"confirm_payment_{payment_id}")],
                [InlineKeyboardButton("📞 تماس پشتیبانی", callback_data="contact")],
                [InlineKeyboardButton("◀️ بازگشت", callback_data="back_main")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
    
    elif query.data == "back_main":
        await query.edit_message_text(
            "👋 منو اصلی\n\nبر روی یکی از گزینه‌های زیر کلیک کنید:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💼 سرویس‌ها", callback_data="services")],
                [InlineKeyboardButton("👤 حساب من", callback_data="my_account")],
                [InlineKeyboardButton("💳 پرداخت", callback_data="payments")],
                [InlineKeyboardButton("📞 تماس", callback_data="contact")],
                [InlineKeyboardButton("📖 راهنما", callback_data="help")]
            ])
        )
    
    elif query.data == "back_services":
        await services(update, context)
    
    elif query.data == "services":
        await services(update, context)
    
    elif query.data == "my_account":
        await my_account(update, context)
    
    elif query.data == "help":
        await help_command(update, context)
    
    elif query.data == "contact":
        await contact(update, context)
    
    elif query.data == "buy_service":
        await services(update, context)
    
    elif query.data.startswith("confirm_payment_"):
        payment_id = int(query.data.replace("confirm_payment_", ""))
        # این بخش را ادمین تایید می‌کند
        await query.edit_message_text(
            "✅ درخواست شما ثبت شد. منتظر تایید مدیر باشید."
        )

# ========== TEXT HANDLERS ==========

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام‌های متنی"""
    text = update.message.text
    
    if text == "💼 سرویس‌ها":
        await services(update, context)
    elif text == "👤 حساب من":
        await my_account(update, context)
    elif text == "📞 تماس":
        await contact(update, context)
    elif text == "📖 راهنما":
        await help_command(update, context)
    else:
        await update.message.reply_text(
            "⚠️ دستور نامشناس.\n\nلطفاً از دکمه‌های زیر استفاده کنید:"
        )

# ⚙️ Config - تنظیمات بات VPN

import os
from datetime import datetime

# 🔑 Telegram Bot Token (از @BotFather بگیرید)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8339211773:AAEZAu922julsvKE2mykUWI4qw663x8PIM8")

# 👨‍💼 ADMIN ID (شناسه ادمین - شناسه عددی شما در Telegram)
ADMIN_ID = int(os.getenv("ADMIN_ID", "8059686209"))  # عوض کنید!

# 🗄️ Database
DATABASE_FILE = "vpn_bot.db"

# 💰 سرویس‌های پیش‌فرض
SERVICES = {
    "basic": {
        "name": "🔓 نامحدود پایه",
        "price": 35000,
        "description": "نامحدود ماهیانه\n🌍 کشور‌ها: المان، ترکیه، ایتالیا، فرانسه، سوئیس، اسپانیا، فنلاند، آمریکا\n🇮🇷 تانل ایران موجود",
        "servers": ["🇩🇪 Germany", "🇹🇷 Turkey", "🇮🇹 Italy", "🇫🇷 France", "🇨🇭 Switzerland", "🇪🇸 Spain", "🇫🇮 Finland", "🇺🇸 USA"],
        "duration": 30  # روز
    },
    "premium": {
        "name": "👑 نامحدود پرمیوم",
        "price": 47000,
        "description": "نامحدود ماهیانه\n🌍 کشور‌ها: همان سرویس پایه\n⚡ سرعت بالاتر و اولویت بالاتر",
        "servers": ["🇩🇪 Germany", "🇹🇷 Turkey", "🇮🇹 Italy", "🇫🇷 France", "🇨🇭 Switzerland", "🇪🇸 Spain", "🇫🇮 Finland", "🇺🇸 USA"],
        "duration": 30
    },
    "gigahi": {
        "name": "📊 تانل گیگی",
        "price": 6500,
        "description": "تانل با محدودیت داده\n🎯 برای مصرف کم\n🌍 کشور‌ها: همان سرویس پایه",
        "servers": ["🇩🇪 Germany", "🇹🇷 Turkey", "🇮🇹 Italy", "🇫🇷 France", "🇨🇭 Switzerland", "🇪🇸 Spain", "🇫🇮 Finland", "🇺🇸 USA"],
        "duration": 30
    },
    "tunnel": {
        "name": "⚡ تانل پرمیوم",
        "price": 16000,
        "description": "سرویس پرمیوم تانل\n🔧 روش‌ها: Cloudflare, Fragment, Fastly\n🌍 کشور‌ها: المان، ایتالیا، هلند",
        "servers": ["🇩🇪 Germany", "🇮🇹 Italy", "🇳🇱 Netherlands"],
        "duration": 30
    }
}

# 💳 اطلاعات کارت برای پرداخت (شماره کارت شما)
CARD_RECEIVER = {
    "name": "نام صاحب کارت",
    "card_number": "6104337612345678",  # عوض کنید!
    "sheba": "IR12345612345612345612345",  # عوض کنید! (IBAN)
    "bank": "بانک ملت"
}

# 📱 لیست ادمین‌ها (برای دسترسی پنل)
ADMIN_IDS = [ADMIN_ID]  # می‌توانید چند ادمین اضافه کنید

# 🌍 پیام‌های پیش‌فرض
MESSAGES = {
    "welcome": """🎉 خوش آمدید به سرویس VPN ما!

ما بهترین سرویس VPN با سرعت بالا و قیمت مناسب رو ارائه می‌دیم.

📲 یکی از گزینه‌های زیر را انتخاب کنید:
""",
    "services_header": """💼 سرویس‌های موجود:

لطفاً یکی از سرویس‌های زیر را انتخاب کنید:
""",
    "account_header": """👤 حساب کاربری شما:

📊 اطلاعات شما:
""",
    "no_service": """❌ شما هنوز سرویسی خریداری نکرده‌اید.

برای خریداری یک سرویس، بر روی دکمه 🛍️ خریداری کلیک کنید.
""",
    "payment_info": """💳 اطلاعات پرداخت:

برای تایید پرداخت، لطفاً به شماره کارت زیر واریز کنید:

📌 {card_receiver_info}

⏰ پس از واریز، 30 دقیقه صبر کنید تا حساب فعال شود.

اگر مشکلی دارید، با ما تماس بگیرید. 📞
"""
}

# 🎨 Emoji‌های استفاده‌شده
EMOJIS = {
    "success": "✅",
    "error": "❌",
    "info": "ℹ️",
    "warning": "⚠️",
    "money": "💰",
    "settings": "⚙️",
    "menu": "📋",
    "user": "👤",
    "admin": "👨‍💼",
    "chart": "📊",
    "package": "📦",
    "payment": "💳",
    "warning_icon": "🚨"
}

# 🔐 Permissions
PERMISSIONS = {
    "view_users": ["admin"],
    "delete_user": ["admin"],
    "add_service": ["admin"],
    "broadcast": ["admin"],
    "view_stats": ["admin"],
    "manage_payments": ["admin"]
}

# 📝 فرمت‌های زمانی
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_DISPLAY_FORMAT = "%d/%m/%Y"

# 🔔 پیام پرداخت موفق
SUCCESS_PAYMENT_MSG = """✅ سرویس فعال شد!

🎉 تبریک می‌گویم! سرویس شما فعال شد.

📊 جزئیات:
• سرویس: {service_name}
• قیمت: {price:,} تومان
• مدت: 30 روز
• انقضا: {expiry_date}

🚀 اکنون می‌توانید از VPN استفاده کنید.
"""

# 📧 پیام‌های ادمین
ADMIN_MESSAGES = {
    "dashboard": """📊 داشبورد ادمین

📈 آمار:
• کل کاربران: {total_users}
• کاربران فعال: {active_users}
• پرداخت‌های در انتظار: {pending_payments}
• درآمد امروز: {today_income:,} تومان
• درآمد کل: {total_income:,} تومان

📅 آخرین پرداخت‌ها: {recent_payments}
""",
    "payment_request": """💰 درخواست پرداخت جدید

👤 کاربر: {user_mention}
📦 سرویس: {service_name}
💵 مبلغ: {amount:,} تومان

🔗 پیوند به پروفایل کاربر
"""
}

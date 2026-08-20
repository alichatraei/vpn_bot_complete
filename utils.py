# 🛠️ Utilities - توابع کمکی

from datetime import datetime
from config import DATE_FORMAT, DATE_DISPLAY_FORMAT, EMOJIS, CARD_RECEIVER

def format_price(price):
    """فرمت قیمت با کاما"""
    return f"{price:,}".replace(",", "٬")

def format_date(date_str):
    """تبدیل تاریخ به فرمت قابل‌نمایش"""
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
    else:
        date_obj = date_str
    
    return date_obj.strftime(DATE_DISPLAY_FORMAT)

def get_card_info():
    """دریافت اطلاعات کارت برای نمایش"""
    return f"""
{CARD_RECEIVER['bank']}
نام: {CARD_RECEIVER['name']}
شماره کارت: {CARD_RECEIVER['card_number']}
IBAN: {CARD_RECEIVER['sheba']}
"""

def get_user_account_text(user):
    """تولید متن حساب کاربری"""
    if not user:
        return "❌ کاربر پیدا نشد"
    
    text = f"""
👤 **حساب کاربری**

👋 نام: {user.get('first_name', '')} {user.get('last_name', '') or ''}
📱 Username: @{user.get('username', 'ندارد')}
📞 تلفن: {user.get('phone', 'ثبت نشده')}

"""
    
    if user.get('service_type'):
        service_names = {
            'basic': '🔓 نامحدود پایه',
            'premium': '👑 نامحدود پرمیوم',
            'gigahi': '📊 تانل گیگی',
            'tunnel': '⚡ تانل پرمیوم'
        }
        service_name = service_names.get(user['service_type'], user['service_type'])
        
        text += f"""📦 **سرویس فعال:**
• نوع: {service_name}
• انقضا: {format_date(user['expiry_date']) if user.get('expiry_date') else 'نامشخص'}
• وضعیت: ✅ فعال
"""
    else:
        text += """
📦 **سرویس:** هیچ سرویسی خریداری نشده

💡 برای خریداری سرویس، بر روی دکمه 🛍️ کلیک کنید.
"""
    
    text += f"""
📅 عضویت از: {format_date(user['created_at'])}
"""
    
    return text

def get_services_keyboard():
    """دریافت کیبورد سرویس‌ها"""
    keyboards = [
        ["🔓 پایه", "👑 پرمیوم"],
        ["📊 گیگی", "⚡ تانل"],
        ["◀️ بازگشت"]
    ]
    return keyboards

def get_main_keyboard():
    """کیبورد اصلی"""
    keyboards = [
        ["💼 سرویس‌ها", "👤 حساب من"],
        ["💳 پرداخت", "📞 تماس"],
        ["📖 راهنما"]
    ]
    return keyboards

def get_admin_keyboard():
    """کیبورد ادمین"""
    keyboards = [
        ["📊 آمار", "👥 کاربران"],
        ["💰 پرداخت‌ها", "📢 پیام همگانی"],
        ["⚙️ سرویس‌ها", "📋 لاگ‌ها"],
        ["◀️ بازگشت"]
    ]
    return keyboards

def escape_markdown(text):
    """فرار کاراکتر‌های markdown"""
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text

def create_service_text(service):
    """ایجاد متن سرویس برای نمایش"""
    text = f"""
{service['name']}

📝 {service['description']}

💰 قیمت: {format_price(service['price'])} تومان

🌍 سرورها:
"""
    
    for server in service['servers']:
        text += f"  • {server}\n"
    
    text += f"\n⏰ مدت اشتراک: 30 روز"
    
    return text

def get_user_service_status(user):
    """دریافت وضعیت سرویس کاربر"""
    if not user.get('service_type'):
        return "❌ هیچ سرویسی فعال نیست"
    
    service_names = {
        'basic': '🔓 نامحدود پایه',
        'premium': '👑 نامحدود پرمیوم',
        'gigahi': '📊 تانل گیگی',
        'tunnel': '⚡ تانل پرمیوم'
    }
    
    service_name = service_names.get(user['service_type'], user['service_type'])
    expiry = format_date(user['expiry_date']) if user.get('expiry_date') else 'نامشخص'
    
    return f"✅ {service_name}\n📅 انقضا: {expiry}"

def get_stats_text(stats):
    """ایجاد متن آمار"""
    text = f"""
📊 **آمار سیستم**

👥 کل کاربران: {stats['total_users']}
✅ کاربران فعال: {stats['active_users']}
💳 پرداخت‌های در انتظار: {stats['pending_payments']}

💰 درآمد امروز: {format_price(stats['today_income'])} تومان
💵 درآمد کل: {format_price(stats['total_income'])} تومان

📈 درآمد متوسط روزانه: {format_price(stats['daily_average'])} تومان
"""
    
    return text

def get_payment_request_text(payment, user):
    """متن درخواست پرداخت برای ادمین"""
    service_names = {
        'basic': '🔓 نامحدود پایه',
        'premium': '👑 نامحدود پرمیوم',
        'gigahi': '📊 تانل گیگی',
        'tunnel': '⚡ تانل پرمیوم'
    }
    
    service_name = service_names.get(payment['service_type'], payment['service_type'])
    
    text = f"""
💰 **درخواست پرداخت جدید**

👤 کاربر: {user.get('first_name', '')} {user.get('last_name', '') or ''}
📱 Username: @{user.get('username', 'ندارد')}
📞 تلفن: {user.get('phone', 'ثبت نشده')}

📦 سرویس: {service_name}
💵 مبلغ: {format_price(payment['amount'])} تومان

🔗 ID پرداخت: {payment['id']}
📅 تاریخ: {format_date(payment['created_at'])}
"""
    
    return text

def create_user_list_text(users, page=1, per_page=10):
    """ایجاد لیست کاربران"""
    total = len(users)
    start = (page - 1) * per_page
    end = start + per_page
    
    page_users = users[start:end]
    
    text = f"👥 **لیست کاربران** (صفحه {page}/{(total + per_page - 1) // per_page})\n\n"
    
    for i, user in enumerate(page_users, 1):
        service_status = user.get('service_type', '❌ ندارد')
        text += f"{i}. {user.get('first_name', '')} - @{user.get('username', 'ندارد')} - {service_status}\n"
    
    return text

def create_payment_list_text(payments):
    """ایجاد لیست پرداخت‌ها"""
    if not payments:
        return "❌ درخواست پرداختی وجود ندارد"
    
    service_names = {
        'basic': '🔓 پایه',
        'premium': '👑 پرمیوم',
        'gigahi': '📊 گیگی',
        'tunnel': '⚡ تانل'
    }
    
    text = f"💳 **پرداخت‌های در انتظار** ({len(payments)} مورد)\n\n"
    
    for payment in payments[:10]:  # فقط 10 مورد آخری
        service_name = service_names.get(payment['service_type'], payment['service_type'])
        user_name = payment.get('first_name', 'نامشناس')
        
        text += f"""
🔹 ID: {payment['id']}
   👤 {user_name} - @{payment.get('username', 'ندارد')}
   📦 {service_name}
   💵 {format_price(payment['amount'])} تومان
   📅 {format_date(payment['created_at'])}
"""
    
    return text

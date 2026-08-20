# 🏗️ معماری بات VPN Telegram

## 📁 ساختار فایل‌ها

```
vpn_bot/
├── main.py                 # فایل اصلی بات
├── config.py              # تنظیمات و Constants
├── database.py            # SQLite Database
├── bot_handlers.py        # Handler‌های بات (Start, Price, etc)
├── admin_handlers.py      # Handler‌های ادمین
├── utils.py               # توابع کمکی
├── requirements.txt       # Dependencies
└── vpn_bot.db            # SQLite Database (خودکار ایجاد)
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    phone TEXT DEFAULT NULL,
    service_type TEXT DEFAULT NULL,  -- 'basic', 'premium', 'gigahi', 'tunnel'
    expiry_date TIMESTAMP DEFAULT NULL,
    payment_status TEXT DEFAULT 'pending',  -- 'pending', 'paid', 'expired'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Services Table
```sql
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price INTEGER,
    description TEXT,
    servers TEXT  -- JSON: ["Germany", "Turkey", ...]
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    service TEXT,
    status TEXT,  -- 'pending', 'completed', 'failed'
    card_receiver TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
```

## 🎯 فیچرهای بات

### کاربر عادی:
- ✅ /start - شروع
- ✅ /services - لیست سرویس‌ها
- ✅ /myaccount - حساب کاربری
- ✅ /buy - خریداری سرویس
- ✅ /support - پشتیبانی

### مدیر:
- ✅ /admin - پنل مدیریتی
- ✅ /stats - آمار و نمودار
- ✅ /users - لیست کاربران
- ✅ /payments - مدیریت پرداخت‌ها
- ✅ /broadcast - پیام همگانی
- ✅ /addservice - اضافه کردن سرویس
- ✅ /removeuser - حذف کاربر

## 🎨 UI/UX Design

### بات کاربران:
- دکمه‌های InlineKeyboard شیک
- ایموجی‌های مناسب
- فرمت‌بندی تمیز
- پیام‌های دوست‌انه

### پنل ادمین:
- Dashboard آماری
- کاربران: فهرست، جستجو، تصفیه
- پرداخت‌ها: در انتظار، تایید شده
- سرویس‌ها: مدیریت، ویرایش
- Broadcast: پیام‌های همگانی


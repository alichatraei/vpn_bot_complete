# 🚀 دپلوی رایگان بات V2Ray VPN

## 🌟 بهترین گزینه‌های رایگان

### 1️⃣ **Replit** ⭐ (بهترین گزینه)
**سایت:** https://replit.com

#### مزایا:
✅ کاملاً رایگان (حتی نیمه‌شب)  
✅ اجرای 24/7 بدون توقف  
✅ پشتیبانی از Python, Node.js, جاوا و 100+ زبان  
✅ داشبورد خوب و ساده  
✅ نیاز به Card نیست  
✅ وقت Uptime نامحدود  

#### نحوه شروع:
1. ثبت‌نام کنید (GitHub/Google)
2. پروژه جدید بسازید
3. کد بات را آپلود کنید
4. "Run" بزنید
5. URL دریافت کنید (مثل: https://your-bot.replit.dev)

#### قیمت:
- **رایگان:** ∞ (تا ابد)
- Pro: $7/ماه (اختیاری)

---

### 2️⃣ **Railway** 🚂
**سایت:** https://railway.app

#### مزایا:
✅ $5 کردیت رایگان هر ماه  
✅ بیشتر بات‌ها کمتر از $5 مصرف می‌کنند  
✅ عملاً رایگان برای 6+ ماه  
✅ پشتیبانی از تمام زبان‌ها  
✅ Database رایگان

#### نحوه شروع:
1. ثبت‌نام (GitHub)
2. "New Project" کنید
3. "Deploy from GitHub" انتخاب کنید
4. Repo متصل کنید
5. خودکار Deploy می‌شود

#### قیمت:
- **رایگان:** $5/ماه (برای 6+ ماه رایگان)
- بعد از آن: $0.29/ساعت (حدود $200/ماه اگر 24/7 اجرا شود)

---

### 3️⃣ **Render** 🎨
**سایت:** https://render.com

#### مزایا:
✅ 750 ساعت رایگان هر ماه (یعنی 24/7 رایگان!)  
✅ بدون نیاز به Credit Card  
✅ SSL رایگان  
✅ Auto Deploy از GitHub  
✅ PostgreSQL Database رایگان

#### نحوه شروع:
1. ثبت‌نام (GitHub)
2. "New Web Service"
3. GitHub Repo انتخاب کنید
4. Deploy شود
5. 24/7 اجرا می‌شود

#### قیمت:
- **رایگان:** 750 ساعت/ماه = 24/7 رایگان!
- Pro: 500+ ساعت = $7+/ماه

---

### 4️⃣ **Heroku** (نسخه جدید رایگان)
**سایت:** https://www.heroku.com

⚠️ توجه: Heroku خط رایگان خود را متوقف کرده، اما می‌توانید:
- **Heroku جدید:** $5/ماه (اولین شهریه رایگان)

---

### 5️⃣ **Oracle Cloud** ☁️
**سایت:** https://www.oracle.com/cloud/free/

#### مزایا:
✅ **سال اول:** کاملاً رایگان  
✅ VM رایگان (2GB RAM)  
✅ بعد از سال اول: برای بات معمولاً رایگان می‌ماند  
✅ نیاز به Card دارد (برای تایید)

#### نحوه شروع:
1. ثبت‌نام (نیاز به پاسپورت/کارت بانکی)
2. Compute Instance ایجاد کنید
3. Ubuntu انتخاب کنید
4. بات را SSH کنید
5. اجرا کنید

---

### 6️⃣ **PythonAnywhere** 🐍
**سایت:** https://www.pythonanywhere.com

#### مزایا:
✅ Python متخصص  
✅ سرویس 24/7 رایگان  
✅ بدون Card

#### نحوه شروع:
1. ثبت‌نام
2. "Web app" جدید
3. کد را آپلود کنید
4. 24/7 اجرا

#### قیمت:
- **رایگان:** ∞
- Paid: $5+/ماه

---

## 📊 مقایسه سریع

| پلتفرم | رایگان | آسانی | Uptime | نتیجه |
|--------|--------|-------|--------|-------|
| **Replit** | ∞ | ⭐⭐⭐⭐⭐ | 24/7 | ✅ بهترین |
| **Railway** | $5/ماه | ⭐⭐⭐⭐ | 24/7 | ✅ خوب |
| **Render** | 24/7 | ⭐⭐⭐⭐ | 24/7 | ✅ خوب |
| **PythonAnywhere** | ∞ | ⭐⭐⭐ | 24/7 | ✅ برای Python |
| **Oracle Cloud** | سال اول | ⭐⭐ | 24/7 | ⚠️ پیچیده |

---

## 🎯 توصیه من برای شما

### **1. بهترین گزینه: Replit**
```
✅ کاملاً رایگان
✅ خیلی آسان
✅ 24/7 اجرا
✅ نیاز به Card نیست
✅ متصل‌کننده رایگان برای Telegram
```

### **2. گزینه جایگزین: Render**
```
✅ 750 ساعت رایگان = 24/7
✅ Auto Deploy
✅ بدون توقف
```

---

## 💻 مراحل دپلوی بات در Replit

### مرحله 1: ثبت‌نام
1. https://replit.com وارد شوید
2. کلیک "Sign up"
3. GitHub یا Google انتخاب کنید

### مرحله 2: پروژه جدید
1. "+ Create" کلیک کنید
2. "Python" انتخاب کنید
3. نام بدهید: "VPN_Bot" یا هر نام دلخواه

### مرحله 3: کد بات
`main.py`:
```python
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! به بات VPN خوش آمدید 🚀")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = """
    💰 قیمت‌های ما:
    
    🔓 نامحدود پایه: 35,000 تومان
    👑 نامحدود پرمیوم: 47,000 تومان
    📊 تانل گیگی: 6,500 تومان
    ⚡ تانل پرمیوم: 16,000 تومان
    """
    await update.message.reply_text(prices)

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### مرحله 4: متغیرهای محیطی
1. "Secrets" کلیک کنید (آیکون قفل)
2. `BOT_TOKEN` اضافه کنید (از @BotFather بگیرید)

### مرحله 5: اجرا
1. "Run" کلیک کنید
2. بات خودکار اجرا می‌شود
3. آدرس Webhook دریافت می‌کنید

---

## 📱 گام‌های اول (بعد از دپلوی):

### 1. بات Telegram را بسازید
1. @BotFather را در Telegram جستجو کنید
2. /newbot وارد کنید
3. نام بدهید: "VPN_Bot_YourName"
4. Token دریافت کنید
5. این Token را در Replit قرار دهید

### 2. بات را تست کنید
1. بات را در Telegram پیدا کنید
2. /start وارد کنید
3. باید جواب بدهد!

### 3. ربط دهید
Telegram به Replit متصل کنید:
```
https://api.telegram.org/bot{TOKEN}/setWebhook?url={REPLIT_URL}
```

---

## 🎁 بعد از ماه اول چه کار کنم؟

### گزینه 1: Replit پرو ($7/ماه)
```
✅ بیشتر Uptime
✅ بدون محدودیت
✅ ارزان‌ترین
```

### گزینه 2: Railway ($5-10/ماه)
```
✅ قابل‌اعتماد
✅ ارزان
✅ Database رایگان
```

### گزینه 3: Vercel + Replit (رایگان!)
```
✅ API در Vercel (رایگان)
✅ Bot در Replit (رایگان)
✅ هیچ هزینه‌ای ندارد
```

---

## ⚠️ نکات مهم

🔴 **مهم:** Replit و دیگر سرویس‌ها **نمی‌توانند**:
- فروش واقعی انجام دهند
- دسترسی مستقیم به سیستم‌های پرداخت
- درخواست‌های دستی پاسخ دهند

✅ **بهتر است**:
- بات فقط **اطلاعات** نمایش دهد
- لینک پرداخت را ارسال کنید
- مشتریان خودشان Zapya/Telegram Pay استفاده کنند

---

## 🚀 خلاصه

**برای ماه اول:**
```
1. Replit ثبت‌نام کنید (5 دقیقه)
2. بات Python را آپلوڈ کنید (5 دقیقه)
3. Telegram Token اضافه کنید (2 دقیقه)
4. Run کنید و تست کنید (2 دقیقه)

= کل: 14 دقیقه! ✅
```

**بعد از ماه اول:** تصمیم بگیرید Paid به Replit Pro برویدا Render یا Railway را انتخاب کنید (همه ارزان هستند).

---

## 📞 آیا کمک بیشتری می‌خواهید؟

بگو اگر:
- ✅ بات Python برات بسازم
- ✅ بات Javascript برات بسازم
- ✅ ربط به درگاه پرداخت (Zarinpal/Idpay)
- ✅ Database ستاپ کنم
- ✅ Auto-backup
- ✅ Webhook اطلاع‌رسانی


# 🗄️ Database - مدیریت SQLite

import sqlite3
import json
from datetime import datetime, timedelta
from config import DATABASE_FILE, SERVICES, DATE_FORMAT

class VPNDatabase:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.init_db()
    
    def get_connection(self):
        """اتصال به پایگاه داده"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """ایجاد جداول پایگاه داده"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول کاربران
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                phone TEXT DEFAULT NULL,
                service_type TEXT DEFAULT NULL,
                expiry_date TIMESTAMP DEFAULT NULL,
                payment_status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول سرویس‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_key TEXT UNIQUE,
                name TEXT,
                price INTEGER,
                description TEXT,
                servers TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول پرداخت‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                service_type TEXT,
                status TEXT DEFAULT 'pending',
                payment_method TEXT DEFAULT 'card',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        
        # جدول پیام‌های ادمین
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                action TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        # افزودن سرویس‌های پیش‌فرض
        self.add_default_services()
    
    def add_default_services(self):
        """افزودن سرویس‌های پیش‌فرض"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for key, service in SERVICES.items():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO services 
                    (service_key, name, price, description, servers)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    key,
                    service['name'],
                    service['price'],
                    service['description'],
                    json.dumps(service['servers'])
                ))
            except:
                pass
        
        conn.commit()
        conn.close()
    
    # ===== کاربران =====
    
    def add_user(self, user_id, first_name, last_name=None, username=None):
        """اضافه کردن کاربر جدید"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (user_id, first_name, last_name, username, created_at, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (user_id, first_name, last_name, username))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """دریافت اطلاعات کاربر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def get_all_users(self, limit=None):
        """دریافت تمام کاربران"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if limit:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT ?", (limit,))
        else:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return users
    
    def update_user_phone(self, user_id, phone):
        """بروزرسانی شماره تلفن کاربر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users 
            SET phone = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (phone, user_id))
        
        conn.commit()
        conn.close()
    
    def update_user_service(self, user_id, service_type):
        """بروزرسانی سرویس کاربر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        expiry_date = (datetime.now() + timedelta(days=30)).strftime(DATE_FORMAT)
        
        cursor.execute("""
            UPDATE users 
            SET service_type = ?, 
                payment_status = 'paid',
                expiry_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (service_type, expiry_date, user_id))
        
        conn.commit()
        conn.close()
    
    def delete_user(self, user_id):
        """حذف کاربر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    
    def get_user_count(self):
        """تعداد کل کاربران"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count = cursor.fetchone()['count']
        conn.close()
        
        return count
    
    # ===== پرداخت‌ها =====
    
    def add_payment(self, user_id, amount, service_type):
        """اضافه کردن درخواست پرداخت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO payments 
            (user_id, amount, service_type, status, created_at, updated_at)
            VALUES (?, ?, ?, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (user_id, amount, service_type))
        
        conn.commit()
        payment_id = cursor.lastrowid
        conn.close()
        
        return payment_id
    
    def get_payment(self, payment_id):
        """دریافت اطلاعات پرداخت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
        payment = cursor.fetchone()
        conn.close()
        
        return dict(payment) if payment else None
    
    def get_user_payments(self, user_id):
        """دریافت پرداخت‌های کاربر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM payments 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """, (user_id,))
        
        payments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return payments
    
    def confirm_payment(self, payment_id):
        """تایید پرداخت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # دریافت جزئیات پرداخت
        cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
        payment = dict(cursor.fetchone())
        
        # بروزرسانی وضعیت پرداخت
        cursor.execute("""
            UPDATE payments 
            SET status = 'completed', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (payment_id,))
        
        # بروزرسانی سرویس کاربر
        self.update_user_service(payment['user_id'], payment['service_type'])
        
        conn.commit()
        conn.close()
    
    def get_pending_payments(self):
        """دریافت پرداخت‌های در انتظار"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.*, u.first_name, u.username 
            FROM payments p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.status = 'pending'
            ORDER BY p.created_at DESC
        """)
        
        payments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return payments
    
    def get_today_income(self):
        """درآمد امروز"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT SUM(amount) as total 
            FROM payments 
            WHERE status = 'completed' 
            AND DATE(created_at) = ?
        """, (today,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result['total'] or 0
    
    def get_total_income(self):
        """درآمد کل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(amount) as total 
            FROM payments 
            WHERE status = 'completed'
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return result['total'] or 0
    
    # ===== سرویس‌ها =====
    
    def get_service(self, service_key):
        """دریافت اطلاعات سرویس"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM services WHERE service_key = ?
        """, (service_key,))
        
        service = cursor.fetchone()
        conn.close()
        
        if service:
            service = dict(service)
            service['servers'] = json.loads(service['servers'])
            return service
        
        return None
    
    def get_all_services(self):
        """دریافت تمام سرویس‌ها"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM services ORDER BY id ASC")
        
        services = []
        for row in cursor.fetchall():
            service = dict(row)
            service['servers'] = json.loads(service['servers'])
            services.append(service)
        
        conn.close()
        
        return services
    
    def add_admin_log(self, admin_id, action, details):
        """اضافه کردن لاگ ادمین"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO admin_logs 
            (admin_id, action, details, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (admin_id, action, details))
        
        conn.commit()
        conn.close()


# ایجاد instance از Database
db = VPNDatabase()

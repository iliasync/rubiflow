# ⚡ RubiFlow (روبی‌فلو)

> **فریم‌ورک فوق‌سریع، ناهمگام (Async) و مدرن پایتون برای پیام‌رسان و سوپراپ روبیکا**  
> *Next-Generation High-Performance Async Python Framework for Rubika Messenger & SuperApp*

---

## 🌟 چرا RubiFlow؟

- **نام کاملاً اختصاصی و جدید:** نامی تک و ثبت‌نشده در PyPI که به جریان روان، غیرهمزمان و پرسرعت اشاره دارد.
- **Async-First و با بالاترین بازده:** با موتور شبکه `aiohttp`، مدیریت Connection Pooling و رمزنگاری با توابع C در `cryptography`.
- **رعایت کامل استانداردهای PEP 8 و Clean Architecture:** استفاده دقیق از Type Hints، مدل‌های داده‌ای (`dataclasses`) و مدیریت خطا با استثناهای اختصاصی.
- **شناسایی خودکار سشن فایرفاکس:** توانایی اتصال آنی به حساب فعال در فایرفاکس (بدون نیاز به دریافت کد پیامکی مجدد).
- **پشتیبانی از StringSession:** خروجی سشن به صورت یک رشته متنی فشرده و امن با پیشوند `RubiFlow$...` جهت استقرار روی سرورها.
- **پوشش جامع بیش از ۳۰۰ متد:** پشتیبانی از پیام‌رسان کامل، روبینو (Rubino)، فیلم و سریال (VOD) و کیف پول.
- **توابع کمکی و شی‌گرایی پیشرفته:** ارسال آسان پیام، ریپلای مستقیم با `message.reply("...")`، حذف و ویرایش، دریافت چت‌ها و پیام‌ها.

---

## 📦 نصب

```bash
pip install -e .
```

یا پیش‌نیازها:
```bash
pip install aiohttp cryptography
```

---

## 🚀 شروع سریع (Quickstart)

### ۱. اتصال خودکار از طریق سشن فایرفاکس
```python
import asyncio
from rubiflow import Client

async def main():
    # اتصال مستقیم به سشن مرورگر فایرفاکس شما
    app = Client.from_firefox()

    async with app:
        me = await app.get_me()
        print(f"Logged in as: {me.full_name} (@{me.username})")

        # ارسال پیام
        msg = await app.send_message("u0...", "سلام از روبی‌فلو!")
        print(f"پیام ارسال شد با آیدی: {msg.message_id}")

asyncio.run(main())
```

---

### ۲. ساخت بات پاسخگوی خودکار (Event-Driven Echo Bot)
```python
from rubiflow import Client, Message

app = Client.from_firefox()

@app.on_message()
async def handle_message(msg: Message):
    if msg.text == "سلام":
        await msg.reply("درود! پیام شما توسط بات RubiFlow دریافت شد.")

# اجرای مداوم بات
app.run()
```

---

### ۳. استفاده از رشته سشن (StringSession) برای سرور
```python
import asyncio
from rubiflow import Client

async def export_session():
    app = Client.from_firefox()
    async with app:
        # دریافت رشته امن برای قرار دادن روی سرور یا متغیرهای محیطی
        string_session = app.session.to_string()
        print("Your StringSession:", string_session)

        # بازیابی مجدد سشن
        new_app = Client(session=string_session)
        async with new_app:
            me = await new_app.get_me()
            print("Connected with StringSession as:", me.username)

asyncio.run(export_session())
```

---

## 📂 ساختار ماژولار پروژه

```
rubika-lib/
├── pyproject.toml              # پیکربندی استاندارد بسته پایتون
├── README.md                   # راهنمای کامل
├── rubiflow/
│   ├── __init__.py             # اکسپورت کلاس‌ها و توابع اصلی
│   ├── client.py               # هسته کلاینت و متدهای سطح بالا
│   ├── crypto.py               # موتور پرسرعت رمزنگاری روبیکا V6 (AES-256 + RSA-SHA256)
│   ├── session.py              # مدیریت سشن (Firefox, StringSession, FileSession)
│   ├── network.py              # ارتباطات ناهمگام با Connection Pooling
│   ├── exceptions.py           # استثناهای اختصاصی (InvalidAuthError, ApiError, ...)
│   └── models/
│       ├── user.py             # کلاس داده کاربر (User)
│       ├── chat.py             # کلاس داده گفتگو (Chat)
│       └── message.py          # کلاس داده پیام همراه متدهای reply, delete, edit
├── docs/
│   ├── RUBIKA_API_FULL_REFERENCE.md   # کاتالوگ جامع بیش از ۳۰۰ متد روبیکا
│   └── RUBIKA_CRYPTO_AND_PROTOCOL.md  # جزئیات مهندسی معکوس و رمزنگاری
└── examples/
    └── rubiflow_quickstart.py  # نمونه کد تست زنده و جامع
```

---

## 🛡️ لایسنس
توسعه داده شده تحت لایسنس MIT.

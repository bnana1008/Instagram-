#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot for Google-style Account Recovery
يقوم هذا البوت بمحاكاة شاشات استرداد حساب Google ويدعم اللغة العربية
"""

import telebot
import re
import phonenumbers
from phonenumbers import geocoder, carrier
import random

# محاولة تحميل التكوين من ملف config.py
try:
    from config import BOT_TOKEN
    print("✅ تم تحميل التكوين من config.py")
except ImportError:
    # إذا لم يوجد ملف التكوين، استخدم المتغير المباشر
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    print("⚠️ لم يتم العثور على config.py، يرجى إنشاؤه من config_template.py")

if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("❌ يرجى وضع توكن البوت الصحيح في config.py أو في المتغير BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# قوائم الأسماء الشائعة حسب الدولة
COUNTRY_NAMES = {
    'السعودية': ['محمد', 'أحمد', 'عبدالله', 'فهد', 'خالد', 'سلطان', 'فاطمة', 'عائشة', 'خديجة', 'مريم'],
    'مصر': ['محمد', 'أحمد', 'مصطفى', 'حسن', 'علي', 'إبراهيم', 'فاطمة', 'خديجة', 'زينب', 'عائشة'],
    'المغرب': ['يوسف', 'محمد', 'أمين', 'عبدالرحمن', 'آدم', 'فاطمة', 'خديجة', 'مريم', 'أسماء', 'زينب'],
    'الإمارات': ['محمد', 'أحمد', 'علي', 'حمد', 'راشد', 'فاطمة', 'عائشة', 'مريم', 'شيخة', 'آمنة'],
    'الكويت': ['محمد', 'أحمد', 'فهد', 'مشاري', 'بدر', 'فاطمة', 'نورا', 'دانة', 'شيماء', 'هند'],
    'الأردن': ['محمد', 'أحمد', 'عمر', 'يزن', 'كريم', 'فاطمة', 'رهف', 'تالا', 'جنى', 'ليان'],
    'لبنان': ['محمد', 'أحمد', 'علي', 'حسن', 'كريم', 'فاطمة', 'زينب', 'مريم', 'ريم', 'نور']
}

def detect_input_type(text):
    """تحديد نوع المدخل: بريد إلكتروني أو رقم هاتف أو اسم"""
    
    # تحقق من البريد الإلكتروني
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, text):
        return 'email', re.search(email_pattern, text).group()
    
    # تحقق من رقم الهاتف
    phone_pattern = r'(\+?\d{1,4}[\s\-]?)?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}'
    if re.search(phone_pattern, text):
        phone_match = re.search(phone_pattern, text).group()
        # تنظيف رقم الهاتف
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone_match)
        if len(clean_phone) >= 7:  # رقم هاتف صالح
            return 'phone', clean_phone
    
    # إذا لم يكن بريد أو رقم، فهو اسم
    if text.strip() and not text.isdigit():
        return 'name', text.strip()
    
    return 'unknown', text

def get_country_from_phone(phone_number):
    """الحصول على الدولة من رقم الهاتف"""
    try:
        # إضافة + إذا لم تكن موجودة
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            country = geocoder.description_for_number(parsed_number, "ar")
            if not country:
                country = geocoder.description_for_number(parsed_number, "en")
            
            # تحويل أسماء الدول الإنجليزية إلى العربية
            country_translations = {
                'Saudi Arabia': 'السعودية',
                'United Arab Emirates': 'الإمارات',
                'Egypt': 'مصر',
                'Kuwait': 'الكويت',
                'Jordan': 'الأردن',
                'Lebanon': 'لبنان',
                'Morocco': 'المغرب',
                'Qatar': 'قطر',
                'Bahrain': 'البحرين',
                'Oman': 'عُمان'
            }
            
            return country_translations.get(country, country if country else "غير محدد")
        else:
            return "غير محدد"
    except:
        return "غير محدد"

def get_country_from_email(email):
    """تخمين الدولة من البريد الإلكتروني"""
    domain = email.split('@')[1].lower()
    
    country_domains = {
        '.sa': 'السعودية',
        '.eg': 'مصر',
        '.ma': 'المغرب',
        '.ae': 'الإمارات',
        '.kw': 'الكويت',
        '.jo': 'الأردن',
        '.lb': 'لبنان',
        'stc.com.sa': 'السعودية',
        'mobily.com.sa': 'السعودية',
        'gmail.com': 'عالمي',
        'yahoo.com': 'عالمي',
        'hotmail.com': 'عالمي',
        'outlook.com': 'عالمي'
    }
    
    for key, country in country_domains.items():
        if key in domain:
            return country
    
    return "غير محدد"

def get_country_from_name(name):
    """تخمين الدولة من الاسم"""
    name_lower = name.lower()
    
    for country, names in COUNTRY_NAMES.items():
        for common_name in names:
            if common_name.lower() in name_lower or name_lower in common_name.lower():
                return country
    
    return "غير محدد"

def is_secure_account(input_type, value):
    """تحديد ما إذا كان الحساب آمن أم لا"""
    if input_type == 'email':
        # البريد الإلكتروني آمن إذا كان من خدمة موثوقة أو يحتوي على أرقام (يشير لوجود تحقق)
        domain = value.split('@')[1].lower()
        secure_domains = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']
        has_numbers = bool(re.search(r'\d', value.split('@')[0]))
        
        return domain in secure_domains or has_numbers
    
    elif input_type == 'phone':
        # أرقام الهواتف الطويلة تعتبر أكثر أماناً
        return len(value) >= 10
    
    elif input_type == 'name':
        # الأسماء الطويلة أو المعقدة تعتبر أكثر أماناً
        return len(value.split()) > 1 or len(value) > 8
    
    return False

def generate_email_response(email, is_secure, country):
    """إنشاء رد لاسترداد البريد الإلكتروني"""
    security_status = "🔒 آمن" if is_secure else "⚠️ غير آمن"
    
    recovery_options = [
        "📧 إرسال رمز التحقق إلى البريد الإلكتروني",
        "📱 إرسال رمز عبر الرسائل القصيرة",
        "🔑 استخدام كلمة مرور التطبيق",
        "📞 التحقق عبر المكالمة الهاتفية"
    ]
    
    selected_options = random.sample(recovery_options, 2)
    
    response = f"""
🔐 **استرداد الحساب**

📧 **البريد الإلكتروني:** {email}
🌍 **الدولة المقدرة:** {country}
🛡️ **حالة الأمان:** {security_status}

**خيارات الاسترداد المتاحة:**
• {selected_options[0]}
• {selected_options[1]}

⚡ **تم العثور على حساب مرتبط بهذا البريد الإلكتروني**

للمتابعة، اختر إحدى طرق التحقق أعلاه.
"""
    return response

def generate_phone_response(phone, is_secure, country):
    """إنشاء رد لاسترداد رقم الهاتف"""
    security_status = "🔒 آمن" if is_secure else "⚠️ غير آمن"
    
    # إخفاء جزء من الرقم
    if len(phone) > 4:
        masked_phone = phone[:3] + "*" * (len(phone) - 6) + phone[-3:]
    else:
        masked_phone = phone
    
    response = f"""
🔐 **تأكيد رقم الهاتف**

📱 **رقم الهاتف:** {masked_phone}
🌍 **الدولة:** {country}
🛡️ **حالة الأمان:** {security_status}

**خيارات التحقق:**
• 📱 إرسال رمز التحقق عبر الرسائل القصيرة
• 📞 إرسال رمز صوتي عبر مكالمة هاتفية

⚡ **تم العثور على حساب مرتبط بهذا الرقم**

سيتم إرسال رمز التحقق خلال دقائق قليلة.
"""
    return response

def generate_name_response(name, is_secure, country):
    """إنشاء رد للتحقق من الاسم"""
    security_status = "🔒 آمن" if is_secure else "⚠️ غير آمن"
    
    response = f"""
🔐 **التحقق من الهوية**

👤 **الاسم:** {name}
🌍 **الدولة المقدرة:** {country}
🛡️ **حالة الأمان:** {security_status}

**معلومات إضافية مطلوبة للتحقق:**
• 📧 عنوان بريد إلكتروني بديل
• 📱 رقم هاتف مرتبط بالحساب
• 🆔 سؤال الأمان

⚡ **تم العثور على حسابات محتملة بهذا الاسم**

يرجى تقديم معلومات إضافية للتحقق من هويتك.
"""
    return response

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """رسالة الترحيب"""
    welcome_text = """
🤖 **مرحباً بك في بوت استرداد الحساب**

هذا البوت يحاكي خدمة استرداد حسابات Google ويدعم:

📧 **البريد الإلكتروني** - للحصول على خيارات الاسترداد
📱 **رقم الهاتف** - لتأكيد الهوية
👤 **الاسم** - للبحث عن الحسابات المرتبطة

**طريقة الاستخدام:**
أرسل أي من المعلومات التالية:
• example@gmail.com
• +966501234567  
• محمد أحمد

سيقوم البوت بتحليل المعلومات وإظهار خيارات الاسترداد المناسبة.
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_recovery_request(message):
    """معالجة طلبات الاسترداد"""
    user_input = message.text.strip()
    
    if not user_input:
        bot.reply_to(message, "⚠️ يرجى إدخال بريد إلكتروني أو رقم هاتف أو اسم.")
        return
    
    input_type, value = detect_input_type(user_input)
    
    if input_type == 'unknown':
        bot.reply_to(message, "❌ لم أتمكن من تحديد نوع المعلومات المدخلة. يرجى المحاولة مرة أخرى.")
        return
    
    # تحديد الدولة حسب نوع المدخل
    if input_type == 'email':
        country = get_country_from_email(value)
    elif input_type == 'phone':
        country = get_country_from_phone(value)
    elif input_type == 'name':
        country = get_country_from_name(value)
    else:
        country = "غير محدد"
    
    # تحديد حالة الأمان
    is_secure = is_secure_account(input_type, value)
    
    # إنشاء الرد المناسب
    if input_type == 'email':
        response = generate_email_response(value, is_secure, country)
    elif input_type == 'phone':
        response = generate_phone_response(value, is_secure, country)
    elif input_type == 'name':
        response = generate_name_response(value, is_secure, country)
    
    bot.reply_to(message, response, parse_mode='Markdown')

if __name__ == '__main__':
    print("🤖 بدء تشغيل بوت استرداد الحساب...")
    print("⚠️ تأكد من وضع توكن البوت في المتغير BOT_TOKEN")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
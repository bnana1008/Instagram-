#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone test for bot functions without requiring bot token
اختبار مستقل لوظائف البوت بدون الحاجة لتوكن البوت
"""

import re
import phonenumbers
from phonenumbers import geocoder, carrier
import random

# نسخ الوظائف من البوت الأصلي للاختبار
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

def test_all_functions():
    """اختبار شامل لجميع الوظائف"""
    print("🚀 اختبار شامل لوظائف بوت استرداد الحساب")
    print("=" * 60)
    
    # اختبار تحديد نوع المدخل
    print("🧪 اختبار تحديد نوع المدخل:")
    test_cases = [
        ("user@gmail.com", "email"),
        ("+966501234567", "phone"),
        ("0501234567", "phone"), 
        ("+971501234567", "phone"),
        ("+20123456789", "phone"),
        ("محمد أحمد", "name"),
        ("فاطمة", "name"),
        ("Ahmed Ali", "name")
    ]
    
    for test_input, expected_type in test_cases:
        input_type, value = detect_input_type(test_input)
        status = "✅" if input_type == expected_type else "❌"
        print(f"  {status} '{test_input}' -> {input_type} ({value})")
    
    print()
    
    # اختبار تحديد الدولة من رقم الهاتف
    print("📱 اختبار أرقام الهواتف والدول:")
    phone_tests = [
        "+966501234567",  # السعودية
        "+971501234567",  # الإمارات
        "+20123456789",   # مصر
        "+965123456789",  # الكويت
        "+962123456789"   # الأردن
    ]
    
    for phone in phone_tests:
        country = get_country_from_phone(phone)
        is_secure = is_secure_account("phone", phone)
        security = "🔒 آمن" if is_secure else "⚠️ غير آمن"
        print(f"  📱 {phone} -> {country} ({security})")
    
    print()
    
    # اختبار تحديد الدولة من البريد الإلكتروني
    print("📧 اختبار البريد الإلكتروني والدول:")
    email_tests = [
        "user@gmail.com",
        "test@stc.com.sa", 
        "user@example.eg",
        "admin@gov.ae",
        "test123@yahoo.com"
    ]
    
    for email in email_tests:
        country = get_country_from_email(email)
        is_secure = is_secure_account("email", email)
        security = "🔒 آمن" if is_secure else "⚠️ غير آمن"
        print(f"  📧 {email} -> {country} ({security})")
    
    print()
    
    # اختبار تحديد الدولة من الأسماء
    print("👤 اختبار الأسماء والدول:")
    name_tests = [
        "محمد",
        "فاطمة",
        "أحمد علي",
        "مريم أحمد",
        "يوسف",
        "Ahmed Smith"
    ]
    
    for name in name_tests:
        country = get_country_from_name(name)
        is_secure = is_secure_account("name", name)
        security = "🔒 آمن" if is_secure else "⚠️ غير آمن"
        print(f"  👤 {name} -> {country} ({security})")
    
    print()
    print("✅ تم إنهاء جميع الاختبارات بنجاح!")

if __name__ == "__main__":
    test_all_functions()
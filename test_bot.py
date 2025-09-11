#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the account recovery bot
اختبار وظائف بوت استرداد الحساب
"""

import sys
import os
sys.path.append('/home/runner/work/Instagram-/Instagram-')

from account_recovery_bot import (
    detect_input_type, 
    get_country_from_phone, 
    get_country_from_email, 
    get_country_from_name,
    is_secure_account,
    generate_email_response,
    generate_phone_response,
    generate_name_response
)

def test_input_detection():
    """اختبار تحديد نوع المدخل"""
    print("🧪 اختبار تحديد نوع المدخل:")
    
    test_cases = [
        ("user@gmail.com", "email"),
        ("+966501234567", "phone"),
        ("0501234567", "phone"),
        ("محمد أحمد", "name"),
        ("Ahmed Ali", "name")
    ]
    
    for test_input, expected_type in test_cases:
        input_type, value = detect_input_type(test_input)
        status = "✅" if input_type == expected_type else "❌"
        print(f"  {status} '{test_input}' -> {input_type} ({value})")
    
    print()

def test_country_detection():
    """اختبار تحديد الدولة"""
    print("🌍 اختبار تحديد الدولة:")
    
    # اختبار أرقام الهواتف
    phone_tests = [
        "+966501234567",  # السعودية
        "+20123456789",   # مصر
        "+971501234567"   # الإمارات
    ]
    
    for phone in phone_tests:
        country = get_country_from_phone(phone)
        print(f"  📱 {phone} -> {country}")
    
    # اختبار البريد الإلكتروني
    email_tests = [
        "user@gmail.com",
        "test@stc.com.sa",
        "user@example.eg"
    ]
    
    for email in email_tests:
        country = get_country_from_email(email)
        print(f"  📧 {email} -> {country}")
    
    # اختبار الأسماء
    name_tests = [
        "محمد",
        "فاطمة",
        "Ahmed"
    ]
    
    for name in name_tests:
        country = get_country_from_name(name)
        print(f"  👤 {name} -> {country}")
    
    print()

def test_security_check():
    """اختبار تحديد حالة الأمان"""
    print("🛡️ اختبار تحديد حالة الأمان:")
    
    test_cases = [
        ("email", "user123@gmail.com"),
        ("email", "test@example.com"),
        ("phone", "+966501234567"),
        ("phone", "12345"),
        ("name", "محمد أحمد علي"),
        ("name", "أحمد")
    ]
    
    for input_type, value in test_cases:
        is_secure = is_secure_account(input_type, value)
        status = "🔒 آمن" if is_secure else "⚠️ غير آمن"
        print(f"  {status} {input_type}: {value}")
    
    print()

def test_response_generation():
    """اختبار إنتاج الردود"""
    print("💬 اختبار إنتاج الردود:")
    
    # اختبار رد البريد الإلكتروني
    email_response = generate_email_response("user@gmail.com", True, "عالمي")
    print("📧 رد البريد الإلكتروني:")
    print(email_response)
    print("-" * 50)
    
    # اختبار رد رقم الهاتف  
    phone_response = generate_phone_response("+966501234567", True, "السعودية")
    print("📱 رد رقم الهاتف:")
    print(phone_response)
    print("-" * 50)
    
    # اختبار رد الاسم
    name_response = generate_name_response("محمد أحمد", False, "السعودية")
    print("👤 رد الاسم:")
    print(name_response)
    print("-" * 50)

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار بوت استرداد الحساب")
    print("=" * 60)
    
    test_input_detection()
    test_country_detection()
    test_security_check()
    test_response_generation()
    
    print("✅ تم إنتهاء جميع الاختبارات بنجاح!")

if __name__ == "__main__":
    main()
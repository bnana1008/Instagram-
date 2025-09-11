#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo of bot responses - عرض توضيحي لردود البوت
يعرض هذا الملف كيف ستبدو ردود البوت لأنواع مختلفة من المدخلات
"""

import sys
sys.path.append('/home/runner/work/Instagram-/Instagram-')

from test_standalone import *

def generate_email_response(email, is_secure, country):
    """إنشاء رد لاسترداد البريد الإلكتروني"""
    security_status = "🔒 آمن" if is_secure else "⚠️ غير آمن"
    
    recovery_options = [
        "📧 إرسال رمز التحقق إلى البريد الإلكتروني",
        "📱 إرسال رمز عبر الرسائل القصيرة",
        "🔑 استخدام كلمة مرور التطبيق",
        "📞 التحقق عبر المكالمة الهاتفية"
    ]
    
    import random
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

def demo_responses():
    """عرض توضيحي لردود البوت"""
    print("🎯 عرض توضيحي لردود بوت استرداد الحساب")
    print("=" * 70)
    
    # أمثلة على المدخلات
    test_inputs = [
        "user123@gmail.com",
        "+966501234567", 
        "محمد أحمد علي"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 **مدخل المستخدم:** `{user_input}`")
        print("-" * 50)
        
        # تحليل المدخل
        input_type, value = detect_input_type(user_input)
        
        # تحديد الدولة
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
        
        # إنشاء الرد
        if input_type == 'email':
            response = generate_email_response(value, is_secure, country)
        elif input_type == 'phone':
            response = generate_phone_response(value, is_secure, country)
        elif input_type == 'name':
            response = generate_name_response(value, is_secure, country)
        
        print("🤖 **رد البوت:**")
        print(response)
        print("=" * 70)

if __name__ == "__main__":
    demo_responses()
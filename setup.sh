#!/bin/bash
# Setup script for Account Recovery Bot
# سكريبت إعداد بوت استرداد الحساب

echo "🤖 إعداد بوت استرداد الحساب"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3 أولاً."
    exit 1
fi

echo "✅ Python 3 موجود"

# Install requirements
echo "📦 تثبيت المتطلبات..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ تم تثبيت المتطلبات بنجاح"
else
    echo "❌ فشل في تثبيت المتطلبات"
    exit 1
fi

# Create config file if it doesn't exist
if [ ! -f config.py ]; then
    echo "📝 إنشاء ملف التكوين..."
    cp config_template.py config.py
    echo "✅ تم إنشاء config.py"
    echo "⚠️  يرجى تحرير config.py ووضع توكن البوت الخاص بك"
else
    echo "ℹ️  ملف config.py موجود بالفعل"
fi

# Run tests
echo "🧪 تشغيل الاختبارات..."
python3 test_standalone.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 تم الإعداد بنجاح!"
    echo ""
    echo "الخطوات التالية:"
    echo "1. احصل على توكن البوت من @BotFather في تليجرام"
    echo "2. افتح config.py وضع التوكن"
    echo "3. شغل البوت: python3 account_recovery_bot.py"
    echo ""
    echo "للاختبار بدون بوت: python3 demo_responses.py"
else
    echo "❌ فشلت الاختبارات"
    exit 1
fi
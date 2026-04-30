# 1. استخدام نسخة خفيفة ومستقرة من بايثون
FROM python:3.10-slim

# 2. تحديد مجلد العمل داخل الحاوية (Container)
WORKDIR /app

# 3. نسخ ملف المتطلبات أولاً (للاستفادة من الـ Cache في Docker)
COPY requirements.txt .

# 4. تثبيت المكتبات اللازمة
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ باقي ملفات المشروع إلى الحاوية
COPY . .

# 6. إنشاء المجلدات اللازمة للبيانات والمخرجات
RUN mkdir -p data output

# 7. الأمر الذي سيتم تنفيذه عند تشغيل الحاوية
CMD ["python", "main.py"]

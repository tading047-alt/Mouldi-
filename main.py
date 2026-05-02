# -*- coding: utf-8 -*-
"""
================================================================================
توليد بيانات عشوائية - حفظ في Excel - إرسال رابط إلى Telegram
================================================================================

هذا الكود يقوم بـ:
1. توليد بيانات عشوائية (مبيعات / موظفين / طلاب)
2. حفظ البيانات في ملف Excel داخل مجلد output
3. إنشاء نسخة احتياطية مع توقيت
4. إرسال رابط تحميل الملف إلى Telegram
5. إرسال رابط مجلد output بالكامل إلى Telegram

المؤلف: Mouldi
التاريخ: 2024
================================================================================
"""

import pandas as pd
import os
import random
import requests
import shutil
from datetime import datetime, timedelta
import json
import base64
from fpdf import FPDF

print("="*70)
print("📊 نظام توليد البيانات العشوائية وإرسالها إلى Telegram")
print("="*70)

# ============================================================================
# الجزء 1: إعدادات Telegram (أدخل بياناتك هنا)
# ============================================================================

# ⚠️ أدخل بيانات Telegram الخاصة بك:
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ضع توكن البوت هنا
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # ضع معرف المحادثة هنا

# ============================================================================
# الجزء 2: دوال توليد البيانات العشوائية
# ============================================================================

def generate_sales_data(rows=50, start_date='2024-01-01', end_date='2024-12-31'):
    """
    توليد بيانات مبيعات عشوائية
    
    المعاملات:
    -----------
    rows : int
        عدد صفوف البيانات
    start_date : str
        تاريخ البداية (YYYY-MM-DD)
    end_date : str
        تاريخ النهاية (YYYY-MM-DD)
    
    المخرجات:
    ----------
    DataFrame
        بيانات المبيعات
    """
    
    # قوائم البيانات
    products = ['لابتوب', 'هاتف', 'جهاز لوحي', 'سماعة', 'شاحن', 'ماوس', 
                'لوحة مفاتيح', 'طابعة', 'كاميرا', 'ساعة ذكية', 'سماعة بلوتوث',
                'جهاز توجيه', 'ماسح ضوئي', 'مكبر صوت', 'قرص صلب']
    
    regions = ['الرياض', 'جدة', 'مكة', 'المدينة', 'الدمام', 'الخبر', 
               'تبوك', 'أبها', 'بريدة', 'الطائف', 'حائل', 'نجران']
    
    customers = [f'عميل_{i:03d}' for i in range(1, 51)]
    payment_methods = ['نقدي', 'بطاقة ائتمان', 'تحويل بنكي', 'مدى', 'أبل باي']
    
    # تحويل التواريخ
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = (end - start).days
    
    # توليد البيانات
    data = {
        'رقم_الفاتورة': [f'INV-{datetime.now().strftime("%Y%m")}-{i:05d}' for i in range(1, rows + 1)],
        'التاريخ': [(start + timedelta(days=random.randint(0, date_range))).strftime('%Y-%m-%d') 
                   for _ in range(rows)],
        'المنتج': [random.choice(products) for _ in range(rows)],
        'الكمية': [random.randint(1, 20) for _ in range(rows)],
        'السعر': [random.randint(50, 5000) for _ in range(rows)],
        'المنطقة': [random.choice(regions) for _ in range(rows)],
        'العميل': [random.choice(customers) for _ in range(rows)],
        'طريقة_الدفع': [random.choice(payment_methods) for _ in range(rows)],
        'نوع_المنتج': [random.choice(['الكترونيات', 'ملحقات', 'حواسيب', 'هواتف']) for _ in range(rows)]
    }
    
    df = pd.DataFrame(data)
    
    # حساب الإجمالي
    df['الإجمالي'] = df['الكمية'] * df['السعر']
    
    # إضافة عمود الشهر
    df['الشهر'] = pd.to_datetime(df['التاريخ']).dt.strftime('%Y-%m')
    
    print(f"✅ تم توليد {rows} سجل مبيعات عشوائي")
    print(f"   إجمالي الإيرادات: {df['الإجمالي'].sum():,.2f} ريال")
    print(f"   عدد المنتجات: {df['المنتج'].nunique()}")
    print(f"   عدد المناطق: {df['المنطقة'].nunique()}")
    
    return df


def generate_employees_data(rows=30):
    """
    توليد بيانات موظفين عشوائية
    """
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations', 'Legal', 'R&D']
    positions = ['مدير', 'محلل', 'مبرمج', 'محاسب', 'مسوق', 'مندوب مبيعات', 'مكتبي', 'متدرب', 'مستشار']
    first_names = ['أحمد', 'محمد', 'عبدالله', 'علي', 'حسن', 'سارة', 'فاطمة', 'نورة', 'عائشة', 'مريم']
    last_names = ['المالكي', 'العتيبي', 'الدوسري', 'الشمري', 'الغامدي', 'الزهراني', 'القحطاني']
    
    data = {
        'الموظف_ID': [f'EMP-{i:03d}' for i in range(1, rows + 1)],
        'الاسم': [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(rows)],
        'العمر': [random.randint(22, 60) for _ in range(rows)],
        'القسم': [random.choice(departments) for _ in range(rows)],
        'المنصب': [random.choice(positions) for _ in range(rows)],
        'الراتب': [random.randint(4000, 35000) for _ in range(rows)],
        'تاريخ_التوظيف': [(datetime.now() - timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d')
                         for _ in range(rows)],
        'البريد_الإلكتروني': [f"employee_{i}@company.com" for i in range(1, rows + 1)],
        'رقم_الهاتف': [f"05{random.randint(10000000, 99999999)}" for _ in range(rows)]
    }
    
    df = pd.DataFrame(data)
    print(f"✅ تم توليد {rows} سجل موظفين عشوائي")
    return df


def generate_students_data(rows=40):
    """
    توليد بيانات طلاب عشوائية
    """
    majors = ['علوم حاسوب', 'هندسة برمجيات', 'هندسة كهربائية', 'طب', 'إدارة أعمال', 
              'محاسبة', 'قانون', 'أدب إنجليزي', 'علوم سياسية', 'فيزياء']
    levels = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس']
    first_names = ['أحمد', 'محمد', 'عبدالله', 'سارة', 'فاطمة', 'نورة', 'مريم', 'عليا']
    last_names = ['التميمي', 'الغامدي', 'الزهراني', 'العتيبي', 'الدوسري']
    
    data = {
        'رقم_الطالب': [f'STU-{datetime.now().year}-{i:04d}' for i in range(1, rows + 1)],
        'الاسم': [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(rows)],
        'المعدل': [round(random.uniform(2.0, 4.0), 2) for _ in range(rows)],
        'المستوى': [random.choice(levels) for _ in range(rows)],
        'التخصص': [random.choice(majors) for _ in range(rows)],
        'الساعات_المكتملة': [random.randint(20, 150) for _ in range(rows)],
        'تاريخ_القبول': [(datetime.now() - timedelta(days=random.randint(0, 1460))).strftime('%Y-%m-%d')
                         for _ in range(rows)],
        'حالة_التسجيل': [random.choice(['نشط', 'منقطع', 'متخرج']) for _ in range(rows)]
    }
    
    df = pd.DataFrame(data)
    print(f"✅ تم توليد {rows} سجل طلاب عشوائي")
    return df


# ============================================================================
# الجزء 3: دوال حفظ الملفات وإدارة مجلد output
# ============================================================================

def create_output_folder():
    """إنشاء مجلد output إذا لم يكن موجوداً"""
    output_folder = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_folder, exist_ok=True)
    print(f"✅ مجلد output: {output_folder}")
    return output_folder


def save_to_excel(df, filename, output_folder='output', create_backup=True):
    """
    حفظ DataFrame في ملف Excel مع إنشاء نسخة احتياطية
    
    المخرجات:
    ----------
    dict : معلومات الملف المحفوظ
    """
    result = {
        'success': False,
        'file_path': '',
        'file_name': filename,
        'backup_path': None,
        'file_size': 0,
        'rows': len(df),
        'columns': len(df.columns)
    }
    
    try:
        # التأكد من وجود المجلد
        folder_path = os.path.join(os.getcwd(), output_folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # التأكد من امتداد الملف
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        file_path = os.path.join(folder_path, filename)
        result['file_path'] = file_path
        
        # إنشاء نسخة احتياطية إذا كان الملف موجوداً
        if create_backup and os.path.exists(file_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{filename.replace('.xlsx', '')}_backup_{timestamp}.xlsx"
            backup_path = os.path.join(folder_path, backup_filename)
            shutil.copy2(file_path, backup_path)
            result['backup_path'] = backup_path
            print(f"💾 تم إنشاء نسخة احتياطية: {backup_filename}")
        
        # حفظ الملف
        df.to_excel(file_path, sheet_name='البيانات', index=False)
        
        # حساب حجم الملف
        result['file_size'] = os.path.getsize(file_path)
        result['success'] = True
        
        print(f"✅ تم حفظ الملف: {filename}")
        print(f"   الحجم: {result['file_size'] / 1024:.2f} KB")
        print(f"   الأبعاد: {len(df)} صف × {len(df.columns)} عمود")
        
        return result
        
    except Exception as e:
        print(f"❌ خطأ في حفظ الملف: {e}")
        return result


def save_with_timestamp(df, prefix='data', output_folder='output'):
    """
    حفظ DataFrame في ملف Excel مع إضافة توقيت للاسم
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{prefix}_{timestamp}.xlsx"
    return save_to_excel(df, filename, output_folder, create_backup=False)


def create_summary_sheet(df_sales, df_employees, df_students, output_folder='output'):
    """
    إنشاء ملف Excel ملخص يحتوي على جميع البيانات
    """
    filename = f"summary_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    file_path = os.path.join(os.getcwd(), output_folder, filename)
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # كتابة جميع الأوراق
        df_sales.to_excel(writer, sheet_name='المبيعات', index=False)
        df_employees.to_excel(writer, sheet_name='الموظفين', index=False)
        df_students.to_excel(writer, sheet_name='الطلاب', index=False)
        
        # إضافة إحصائيات ملخصة
        stats_data = {
            'نوع_البيانات': ['المبيعات', 'الموظفين', 'الطلاب'],
            'عدد_السجلات': [len(df_sales), len(df_employees), len(df_students)],
            'عدد_الأعمدة': [len(df_sales.columns), len(df_employees.columns), len(df_students.columns)],
            'تاريخ_الإنشاء': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 3
        }
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_excel(writer, sheet_name='إحصائيات', index=False)
    
    file_size = os.path.getsize(file_path) / 1024
    print(f"✅ تم إنشاء ملف الملخص: {filename} ({file_size:.2f} KB)")
    
    return file_path


# ============================================================================
# الجزء 4: دوال الإرسال إلى Telegram
# ============================================================================

def send_telegram_message(bot_token, chat_id, message):
    """إرسال رسالة نصية إلى Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ تم إرسال الرسالة إلى Telegram")
            return True
        else:
            print(f"❌ فشل إرسال الرسالة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False


def send_file_link(bot_token, chat_id, file_url, file_type="ملف", caption=""):
    """إرسال رابط ملف إلى Telegram"""
    # استخدام رابط مباشر من GitHub أو أي خادم
    message = f"📎 **رابط تحميل {file_type}**\n\n"
    message += f"🔗 {file_url}\n\n"
    
    if caption:
        message += f"📝 {caption}\n\n"
    
    message += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return send_telegram_message(bot_token, chat_id, message)


def send_telegram_document(bot_token, chat_id, file_path, caption=""):
    """إرسال ملف مباشرة إلى Telegram (بدون رابط)"""
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    
    try:
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chat_id, 'caption': caption}
            response = requests.post(url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                print(f"✅ تم إرسال الملف مباشرة إلى Telegram: {os.path.basename(file_path)}")
                return True
            else:
                print(f"❌ فشل إرسال الملف: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ خطأ في إرسال الملف: {e}")
        return False


def send_github_link(bot_token, chat_id, repo_name, file_path, branch='main'):
    """إرسال رابط GitHub للملف"""
    github_url = f"https://github.com/{repo_name}/blob/{branch}/{file_path}"
    return send_file_link(bot_token, chat_id, github_url, "ملف من GitHub")


# ============================================================================
# الجزء 5: إنشاء رابط تحميل (لـ GitHub أو أي خادم)
# ============================================================================

def upload_to_github(file_path, github_token, repo_owner, repo_name, branch='main'):
    """
    رفع الملف إلى GitHub والحصول على رابط مباشر
    
    المعاملات:
    -----------
    file_path : str
        مسار الملف المحلي
    github_token : str
        توكن GitHub
    repo_owner : str
        اسم المستخدم
    repo_name : str
        اسم المستودع
    branch : str
        اسم الفرع
    
    المخرجات:
    ----------
    str : رابط الملف أو None إذا فشل
    """
    try:
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        filename = os.path.basename(file_path)
        github_path = f"data/{filename}"
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{github_path}"
        headers = {'Authorization': f'token {github_token}'}
        
        # التحقق من وجود الملف
        response = requests.get(url, headers=headers)
        sha = response.json().get('sha') if response.status_code == 200 else None
        
        data = {
            'message': f'إضافة {filename}',
            'content': content,
            'branch': branch
        }
        if sha:
            data['sha'] = sha
        
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            file_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{github_path}"
            print(f"✅ تم رفع الملف إلى GitHub")
            print(f"   الرابط: {file_url}")
            return file_url
        else:
            print(f"❌ فشل رفع الملف إلى GitHub: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None


# ============================================================================
# الجزء 6: توليد تقرير PDF (اختياري)
# ============================================================================

def generate_pdf_report(df, title="تقرير البيانات", output_folder='output'):
    """
    إنشاء تقرير PDF من DataFrame
    """
    try:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(os.getcwd(), output_folder, filename)
        
        class PDFReport(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, title, 0, 1, 'C')
                self.ln(5)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'صفحة {self.page_no()}', 0, 0, 'C')
        
        pdf = PDFReport(orientation='L', format='A4')
        pdf.add_page()
        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"عدد السجلات: {len(df)}", 0, 1)
        pdf.cell(0, 10, f"عدد الأعمدة: {len(df.columns)}", 0, 1)
        pdf.ln(5)
        
        # عرض أول 50 صف
        page_width = pdf.w - 20
        col_width = min(page_width / len(df.columns), 50)
        
        pdf.set_font("Arial", "B", 8)
        for col in df.columns:
            pdf.cell(col_width, 10, str(col)[:20], 1, 0, 'C')
        pdf.ln()
        
        pdf.set_font("Arial", "", 7)
        for idx, row in df.head(50).iterrows():
            for col in df.columns:
                cell_text = str(row[col])[:20]
                pdf.cell(col_width, 8, cell_text, 1, 0, 'L')
            pdf.ln()
        
        pdf.output(file_path)
        print(f"✅ تم إنشاء تقرير PDF: {filename}")
        return file_path
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء PDF: {e}")
        return None


# ============================================================================
# الجزء 7: الوظيفة الرئيسية
# ============================================================================

def main():
    """الوظيفة الرئيسية لتشغيل الكود"""
    
    print("\n" + "="*70)
    print("🚀 بدء عملية توليد البيانات وحفظها وإرسالها")
    print("="*70)
    
    # 1. إنشاء مجلد output
    print("\n📁 1. إنشاء مجلد output...")
    output_folder = create_output_folder()
    
    # 2. توليد البيانات
    print("\n📊 2. توليد البيانات العشوائية...")
    print("-" * 40)
    
    # اختيار نوع البيانات
    print("\nأنواع البيانات المتاحة:")
    print("1. بيانات مبيعات (Sales)")
    print("2. بيانات موظفين (Employees)")
    print("3. بيانات طلاب (Students)")
    print("4. جميع الأنواع (All)")
    
    data_type = input("\nاختر نوع البيانات (1-4): ").strip()
    
    if data_type == '1':
        rows = int(input("عدد سجلات المبيعات (افتراضي 50): ") or "50")
        df_sales = generate_sales_data(rows=rows)
        df_employees = None
        df_students = None
        main_df = df_sales
        data_name = "المبيعات"
        
    elif data_type == '2':
        rows = int(input("عدد سجلات الموظفين (افتراضي 30): ") or "30")
        df_employees = generate_employees_data(rows=rows)
        df_sales = None
        df_students = None
        main_df = df_employees
        data_name = "الموظفين"
        
    elif data_type == '3':
        rows = int(input("عدد سجلات الطلاب (افتراضي 40): ") or "40")
        df_students = generate_students_data(rows=rows)
        df_sales = None
        df_employees = None
        main_df = df_students
        data_name = "الطلاب"
        
    else:  # جميع الأنواع
        sales_rows = int(input("عدد سجلات المبيعات (افتراضي 50): ") or "50")
        employees_rows = int(input("عدد سجلات الموظفين (افتراضي 30): ") or "30")
        students_rows = int(input("عدد سجلات الطلاب (افتراضي 40): ") or "40")
        
        df_sales = generate_sales_data(rows=sales_rows)
        df_employees = generate_employees_data(rows=employees_rows)
        df_students = generate_students_data(rows=students_rows)
        main_df = df_sales  # للعرض الأساسي
        data_name = "جميع الأنواع"
    
    # 3. حفظ البيانات في Excel
    print("\n💾 3. حفظ البيانات في ملف Excel...")
    print("-" * 40)
    
    # حفظ الملف الرئيسي
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    main_filename = f"{data_name}_{timestamp}.xlsx"
    save_result = save_to_excel(main_df, main_filename, output_folder)
    
    # حفظ ملف الملخص إذا كان هناك عدة أنواع
    if data_type == '4' and df_sales is not None and df_employees is not None and df_students is not None:
        print("\n📑 إنشاء ملف ملخص...")
        summary_path = create_summary_sheet(df_sales, df_employees, df_students, output_folder)
    
    # 4. إنشاء نسخة مع توقيت
    print("\n⏰ 4. إنشاء نسخة احتياطية مع توقيت...")
    backup_result = save_with_timestamp(main_df, prefix=data_name, output_folder=output_folder)
    
    # 5. إنشاء تقرير PDF (اختياري)
    print("\n📄 5. إنشاء تقرير PDF...")
    pdf_file = generate_pdf_report(main_df, title=f"تقرير {data_name}", output_folder=output_folder)
    
    # 6. إعداد رابط للملف (يمكن تعديله حسب احتياجك)
    print("\n🔗 6. تجهيز رابط التحميل...")
    print("-" * 40)
    
    # طريقة 1: استخدام رابط محلي (للتجربة المحلية)
    # local_url = f"file:///{save_result['file_path']}"
    
    # طريقة 2: استخدام GitHub (يتطلب توكن)
    use_github = input("\nهل تريد رفع الملف إلى GitHub؟ (نعم/لا): ").strip().lower()
    
    if use_github in ['نعم', 'yes', 'y']:
        github_token = input("أدخل GitHub Token: ").strip()
        repo_owner = input("أدخل اسم المستخدم: ").strip()
        repo_name = input("أدخل اسم المستودع: ").strip()
        
        file_url = upload_to_github(save_result['file_path'], github_token, repo_owner, repo_name)
    else:
        # رابط محلي أو رابط من GitHub Pages
        file_url = save_result['file_path']
        print(f"📁 الملف محفوظ محلياً: {file_url}")
    
    # 7. إدخال بيانات Telegram
    print("\n🤖 7. إعداد Telegram...")
    print("-" * 40)
    
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    
    if bot_token == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ لم تقم بإدخال بيانات Telegram!")
        bot_token = input("أدخل توكن بوت Telegram: ").strip()
        chat_id = input("أدخل معرف المحادثة (Chat ID): ").strip()
    
    # 8. إرسال إلى Telegram
    print("\n📤 8. إرسال إلى Telegram...")
    print("-" * 40)
    
    # إرسال رسالة ترحيب مع ملخص البيانات
    welcome_message = f"""
╔══════════════════════════════════════════════════════╗
║     📊 تقرير البيانات العشوائية                     ║
║     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     ║
╚══════════════════════════════════════════════════════╝

📈 ملخص البيانات:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• نوع البيانات: {data_name}
• عدد السجلات: {len(main_df):,}
• عدد الأعمدة: {len(main_df.columns)}
• حجم الملف: {save_result['file_size'] / 1024:.2f} KB

📁 الملفات المحفوظة في مجلد output:
• {os.path.basename(save_result['file_path'])}
• {os.path.basename(backup_result['file_path'])} (نسخة احتياطية)
"""
    
    if pdf_file:
        welcome_message += f"• {os.path.basename(pdf_file)} (PDF)\n"
    
    welcome_message += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ تم إنشاء هذا التقرير تلقائياً
"""
    
    send_telegram_message(bot_token, chat_id, welcome_message)
    
    # إرسال رابط الملف
    if file_url:
        send_file_link(bot_token, chat_id, file_url, 
                      file_type=f"Excel ({data_name})",
                      caption=f"📊 ملف {data_name} - {len(main_df)} سجل")
    
    # إرسال الملف مباشرة (اختياري)
    send_direct = input("\nهل تريد إرسال الملف مباشرة إلى Telegram؟ (نعم/لا): ").strip().lower()
    if send_direct in ['نعم', 'yes', 'y']:
        send_telegram_document(bot_token, chat_id, save_result['file_path'],
                              caption=f"📊 ملف {data_name} - {len(main_df)} سجل")
    
    # 9. عرض النتائج النهائية
    print("\n" + "="*70)
    print("📋 النتائج النهائية:")
    print("="*70)
    
    print(f"\n📂 مجلد output: {output_folder}")
    print(f"\n📄 الملفات التي تم إنشاؤها:")
    
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        file_size = os.path.getsize(file_path) / 1024
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"   • {file} - {file_size:.2f} KB - {file_time.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n" + "="*70)
    print("🎉 اكتملت العملية بنجاح!")
    print("="*70)
    
    return {
        'output_folder': output_folder,
        'main_file': save_result['file_path'],
        'backup_file': backup_result['file_path'],
        'pdf_file': pdf_file,
        'file_url': file_url if file_url else None,
        'data_rows': len(main_df),
        'data_columns': len(main_df.columns)
    }


# ============================================================================
# تشغيل البرنامج
# ============================================================================

if __name__ == "__main__":
    
    # إعدادات Telegram (يمكنك تعديلها مباشرة هنا)
    TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ضع التوكن هنا
    TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # ضع المعرف هنا
    
    # تشغيل البرنامج
    result = main()
    
    print("\n" + "="*70)
    print("✅ تم حفظ جميع البيانات في مجلد output")
    print(f"📂 المسار: {result['output_folder']}")
    print("="*70)

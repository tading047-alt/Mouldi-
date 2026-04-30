import pandas as pd
import plotly.express as px
import os

# --- 1. إعداد المسارات ---
INPUT_FILE = 'data/sales_data.xlsx'
OUTPUT_FOLDER = 'output'

def setup_project():
    """تهيئة المجلدات والملفات اللازمة للتأكد من عمل الكود"""
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    # إذا لم يجد ملف البيانات، سيقوم بإنشائه فوراً
    if not os.path.exists(INPUT_FILE):
        print("⚠️ ملف البيانات غير موجود.. جاري إنشاء ملف تجريبي...")
        sample_data = {
            'Date': ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05'],
            'Product': ['Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Webcam'],
            'Quantity': [10, 50, 15, 30, 25],
            'Price': [1200, 25, 200, 45, 80],
            'Cost': [800, 10, 120, 20, 40]
        }
        pd.DataFrame(sample_data).to_excel(INPUT_FILE, index=False)
        print(f"✅ تم إنشاء الملف بنجاح في: {INPUT_FILE}")

# --- 2. محرك تنظيف البيانات ---
def clean_data(df):
    print("🧹 جاري تنظيف البيانات...")
    df = df.drop_duplicates()  # حذف التكرار
    df.fillna(0, inplace=True) # معالجة القيم المفقودة
    return df

# --- 3. محرك التحليل الحسابي ---
def perform_analysis(df):
    print("📊 جاري تحليل البيانات الحسابية...")
    # حساب المبيعات والربح
    df['Total_Sales'] = df['Quantity'] * df['Price']
    df['Total_Cost'] = df['Quantity'] * df['Cost']
    df['Profit'] = df['Total_Sales'] - df['Total_Cost']
    
    # تجميع النتائج حسب المنتج
    summary = df.groupby('Product')[['Total_Sales', 'Profit']].sum().reset_index()
    return df, summary

# --- 4. محرك الرسوم البيانية ---
def generate_dashboard(summary):
    print("📈 جاري إنشاء لوحة البيانات التفاعلية...")
    fig = px.bar(
        summary, 
        x='Product', 
        y='Profit',
        title='صافي الأرباح لكل منتج - مشروع أتمتة 2026',
        color='Profit',
        labels={'Profit': 'الربح الصافي ($)', 'Product': 'المنتج'},
        template='plotly_dark'  # مظهر احترافي داكن
    )
    
    # حفظ الرسم البياني كملف HTML تفاعلي
    fig.write_html(f"{OUTPUT_FOLDER}/dashboard.html")

# --- التشغيل الرئيسي للمشروع ---
if __name__ == "__main__":
    # 1. التهيئة
    setup_project()
    
    # 2. قراءة البيانات
    raw_data = pd.read_excel(INPUT_FILE)
    
    # 3. التنظيف
    cleaned_data = clean_data(raw_data)
    
    # 4. التحليل
    detailed_df, final_summary = perform_analysis(cleaned_data)
    
    # 5. تصدير التقارير
    detailed_df.to_excel(f"{OUTPUT_FOLDER}/detailed_report.xlsx", index=False)
    final_summary.to_excel(f"{OUTPUT_FOLDER}/summary_report.xlsx", index=False)
    
    # 6. الرسم البياني
    generate_dashboard(final_summary)
    
    print("\n" + "="*30)
    print("🚀 تم الانتهاء من المشروع بنجاح!")
    print(f"📁 تفقد مجلد '{OUTPUT_FOLDER}' لرؤية المخرجات.")
    print("="*30)

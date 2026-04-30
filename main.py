import pandas as pd
import plotly.express as px
import os

# 1. دالة تحميل البيانات (Pre-loading)
def load_data(file_path):
    print("--- مرحلة تحميل البيانات ---")
    # نقرأ الملف مع التأكد من جلب الأعمدة الأساسية فقط لتسريع العمل
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"خطأ في تحميل الملف: {e}")
        return None

# 2. محرك التنظيف (Cleaning Engine) - الجزء الذي ستطوره لاحقاً
def clean_data(df):
    print("--- مرحلة تنظيف البيانات ---")
    # حذف التكرار
    df = df.drop_duplicates()
    # ملء القيم المفقودة في الأعمدة الرقمية بصفر
    df.fillna(0, inplace=True)
    return df

# 3. محرك التحليل (Analysis Logic)
def analyze_sales(df):
    print("--- مرحلة التحليل الحسابي ---")
    # حساب إجمالي البيع (كمثال: الكمية * السعر)
    # ملاحظة للعميل: يمكنك تعديل هذه المعادلة حسب نظامك المحاسبي
    if 'Quantity' in df.columns and 'Price' in df.columns:
        df['Total_Sales'] = df['Quantity'] * df['Price']
    
    # تجميع المبيعات حسب المنتج
    summary = df.groupby('Product')['Total_Sales'].sum().reset_index()
    return df, summary

# 4. محرك التصور البصري (Visualization)
def create_dashboard(summary):
    print("--- مرحلة إنشاء الرسوم البيانية ---")
    fig = px.bar(summary, x='Product', y='Total_Sales', 
                 title='إجمالي المبيعات حسب المنتج - 2026',
                 labels={'Total_Sales': 'صافي الأرباح', 'Product': 'المنتج'},
                 template='plotly_dark') # لمسة احترافية غامقة
    
    # حفظ الرسم كملف تفاعلي يمكن للعميل فتحه
    fig.write_html("output/sales_dashboard.html")
    print("✅ تم إنشاء لوحة البيانات التفاعلية في مجلد output")

# التشغيل الأساسي للمشروع
if __name__ == "__main__":
    # تأكد من وجود مجلد المخرجات
    if not os.path.exists('output'): os.makedirs('output')

    # المسار الافتراضي (يمكنك تغييره بسهولة)
    DATA_PATH = "data/your_file.xlsx" 
    
    # تنفيذ الخطوات
    raw_df = load_data(DATA_PATH)
    if raw_df is not None:
        cleaned_df = clean_data(raw_df)
        final_df, report = analyze_sales(cleaned_df)
        
        # تصدير النتائج النهائية لإكسل منسق
        final_df.to_excel("output/final_report.xlsx", index=False)
        
        # إنشاء الرسم البياني
        create_dashboard(report)
        print("\n🚀 المشروع جاهز للتسليم!")

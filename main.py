import pandas as pd
import plotly.express as px
import os

def run_full_project():
    print("🚀 بدء المشروع: معالجة البيانات مدمجة آلياً...")

    # --- 1. مرحلة البيانات (توليد بيانات وهمية احترافية) ---
    # بدلاً من قراءة ملف خارجي، نصنع البيانات هنا مباشرة
    raw_data = {
        'Product': ['Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Webcam', 'Laptop', 'Mouse'],
        'Quantity': [15, 60, 20, 35, 30, 2, 5],
        'Price': [1200, 25, 210, 45, 85, 1200, 25],
        'Cost': [850, 12, 150, 22, 45, 850, 12]
    }
    df = pd.DataFrame(raw_data)
    print("✅ تم توليد البيانات بنجاح.")

    # --- 2. مرحلة التنظيف (Cleaning) ---
    print("🧹 جاري تنظيف البيانات المكررة...")
    # دمج المبيعات المكررة لنفس المنتج
    df = df.groupby('Product').agg({
        'Quantity': 'sum',
        'Price': 'mean',
        'Cost': 'mean'
    }).reset_index()

    # --- 3. مرحلة التحليل (Analysis) ---
    print("📊 جاري إجراء الحسابات المالية...")
    df['Total_Revenue'] = df['Quantity'] * df['Price']
    df['Total_Profit'] = df['Total_Revenue'] - (df['Quantity'] * df['Cost'])
    
    # حساب نسبة الربح لكل منتج
    df['Profit_Margin_%'] = (df['Total_Profit'] / df['Total_Revenue']) * 100
    
    # --- 4. مرحلة التصدير (Export) ---
    os.makedirs('output', exist_ok=True)
    df.to_excel('output/final_analysis_report.xlsx', index=False)
    print("📂 تم حفظ تقرير الإكسل في مجلد output.")

    # --- 5. مرحلة الرسم البياني (Visualization) ---
    print("📈 جاري إنشاء لوحة البيانات التفاعلية...")
    fig = px.bar(
        df, 
        x='Product', 
        y='Total_Profit',
        color='Profit_Margin_%',
        title='تحليل الأرباح ونسبة الهامش لكل منتج - 2026',
        labels={'Total_Profit': 'صافي الربح ($)', 'Profit_Margin_%': 'نسبة الربح %'},
        text_auto='.2f',
        template='plotly_dark'
    )
    
    fig.write_html('output/interactive_dashboard.html')
    print("✅ تم إنشاء الرسم البياني التفاعلي بنجاح.")

if __name__ == "__main__":
    try:
        run_full_project()
        print("\n" + "="*40)
        print("🌟 مبروك! الكود عمل بنجاح بدون ملفات خارجية.")
        print("تحقق الآن من مجلد 'output' لرؤية النتائج.")
        print("="*40)
    except Exception as e:
        print(f"❌ حدث خطأ تقني: {e}")

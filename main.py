import pandas as pd
import plotly.express as px
import os

# إنشاء مجلد المخرجات
os.makedirs('output', exist_ok=True)

def run_test():
    print("🚀 بدء تجربة الكود ببيانات داخلية...")
    
    # إنشاء بيانات مباشرة داخل الكود لتجنب أخطاء الملفات
    data = {
        'Product': ['A', 'B', 'C', 'D'],
        'Sales': [100, 150, 80, 120],
        'Profit': [40, 60, 30, 50]
    }
    df = pd.DataFrame(data)
    
    # تحليل بسيط
    print("📊 تحليل البيانات...")
    summary = df.describe()
    
    # إنشاء رسم بياني
    print("📈 إنشاء الرسم البياني...")
    fig = px.bar(df, x='Product', y='Profit', title="تجربة تشغيل ناجحة")
    fig.write_html('output/test_dashboard.html')
    
    # حفظ تقرير إكسل
    df.to_excel('output/test_report.xlsx', index=False)
    
    print("✅ تم بنجاح! تفقد مجلد output الآن.")

if __name__ == "__main__":
    run_test()

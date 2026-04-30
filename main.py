import pandas as pd
import plotly.express as px
import os
import random

def run_standalone_project():
    print("🚀 بدء مشروع توليد ومعالجة البيانات آلياً (بدون ملفات خارجية)...")

    # --- 1. توليد معطيات عشوائية (Data Generation) ---
    products = ['أيفون', 'سامسونج', 'ماك بوك', 'ساعة ذكية', 'سماعات']
    data = []
    
    for i in range(20):  # توليد 20 عملية بيع وهمية
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.randint(200, 1500)
        data.append([product, quantity, price])
    
    df = pd.DataFrame(data, columns=['المنتج', 'الكمية', 'السعر_الفردي'])
    print("✅ تم توليد 20 عملية بيع بنجاح.")

    # --- 2. المعالجة الحسابية (Data Processing) ---
    df['إجمالي_المبيعات'] = df['الكمية'] * df['السعر_الفردي']
    df['الضريبة_15%'] = df['إجمالي_المبيعات'] * 0.15
    df['الصافي_النهائي'] = df['إجمالي_المبيعات'] - df['الضريبة_15%']

    # تجميع النتائج حسب المنتج لتقديم خلاصة
    summary = df.groupby('المنتج')[['إجمالي_المبيعات', 'الصافي_النهائي']].sum().reset_index()

    # --- 3. عرض النتيجة في الـ Terminal (Immediate Result) ---
    print("\n📊 ملخص النتائج النهائية:")
    print("-" * 40)
    print(summary.to_string(index=False))
    print("-" * 40)

    # --- 4. إرسال النتيجة إلى ملفات (Output) ---
    os.makedirs('output', exist_ok=True)
    
    # حفظ الإكسل
    summary.to_excel('output/results_summary.xlsx', index=False)
    
    # إنشاء الرسم البياني
    fig = px.pie(summary, values='الصافي_النهائي', names='المنتج', 
                 title='توزيع الأرباح الصافية حسب المنتج',
                 template='plotly_dark')
    fig.write_html('output/final_chart.html')

    print(f"\n✅ اكتملت المهمة. تفقد مجلد 'output' للملفات الناتجة.")

if __name__ == "__main__":
    # تثبيت المكتبات إذا لم تكن موجودة (اختياري للـ Codespace)
    # os.system('pip install pandas plotly openpyxl')
    
    run_standalone_project()

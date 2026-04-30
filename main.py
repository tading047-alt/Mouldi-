import pandas as pd
import plotly.express as px
import os
import random

def run_data_export_project():
    print("🚀 بدء مشروع معالجة البيانات وتصدير الملفات (CSV & XLSX)...")

    # --- 1. توليد بيانات تجريبية (Data Generation) ---
    products = ['شاشة 4K', 'لوحة مفاتيح', 'ماوس لاسلكي', 'سماعات محيطية', 'طاولة قيمنق']
    data = []
    
    for _ in range(50):  # توليد 50 سجل بيع وهمي
        product = random.choice(products)
        qty = random.randint(1, 20)
        price = random.randint(50, 500)
        data.append([product, qty, price])
    
    df = pd.DataFrame(data, columns=['Product', 'Quantity', 'Unit_Price'])
    print("✅ تم توليد 50 سجلاً للبيانات.")

    # --- 2. معالجة البيانات (Processing) ---
    df['Total_Sales'] = df['Quantity'] * df['Unit_Price']
    # تجميع البيانات حسب المنتج للحصول على ملخص
    summary = df.groupby('Product')['Total_Sales'].sum().reset_index()

    # --- 3. تصدير الملفات للتحميل (Exporting CSV & XLSX) ---
    os.makedirs('output', exist_ok=True)
    
    # تصدير بصيغة CSV
    csv_path = 'output/sales_results.csv'
    summary.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # تصدير بصيغة Excel (XLSX)
    xlsx_path = 'output/sales_results.xlsx'
    summary.to_excel(xlsx_path, index=False)
    
    print(f"✅ تم تصدير ملف CSV إلى: {csv_path}")
    print(f"✅ تم تصدير ملف Excel إلى: {xlsx_path}")

    # --- 4. إنشاء رسم بياني سريع للتأكد ---
    fig = px.bar(summary, x='Product', y='Total_Sales', title='إجمالي المبيعات حسب المنتج')
    fig.write_html('output/visual_report.html')

    print("\n📊 النتيجة النهائية (ملخص المبيعات):")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    # تثبيت المكتبات اللازمة في Codespace إذا لم تكن موجودة
    # os.system('pip install pandas plotly openpyxl')
    
    run_data_export_project()
    print("\n🌟 المهمة اكتملت! يمكنك الآن تحميل الملفات من مجلد output.")

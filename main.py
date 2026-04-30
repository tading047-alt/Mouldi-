import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# 1️⃣ مجلدات العمل
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# 2️⃣ توليد معطيات وهمية (تبدو حقيقية)
np.random.seed(42)  # للتكرار نفسه كل مرة

num_days = 100
dates = [datetime(2025, 1, 1) + timedelta(days=i) for i in range(num_days)]

data = {
    "التاريخ": dates,
    "المبيعات": np.random.randint(500, 5000, num_days),
    "التكلفة": np.random.randint(300, 3000, num_days),
    "عدد_العملاء": np.random.randint(10, 200, num_days),
    "الانطباعات_الإعلانية": np.random.randint(1000, 50000, num_days),
    "category": np.random.choice(["A", "B", "C"], num_days, p=[0.5, 0.3, 0.2])
}

df = pd.DataFrame(data)

# إضافة عمود مفيد: الربح
df["الربح"] = df["المبيعات"] - df["التكلفة"]

# إضافة بعض القيم المفقودة عمدًا (لتتعلم التنظيف لاحقًا)
df.loc[10:15, "المبيعات"] = np.nan
df.loc[40:42, "عدد_العملاء"] = np.nan

# 3️⃣ حفظ في Excel
excel_path = "data/بيانات_المبيعات.xlsx"
df.to_excel(excel_path, index=False)
print(f"✅ تم توليد وحفظ البيانات في:\n   {excel_path}")

# 4️⃣ قراءة البيانات (سيمارس تنظيفها)
df = pd.read_excel(excel_path)

# تنظيف بسيط (القيم المفقودة)
df["المبيعات"].fillna(df["المبيعات"].median(), inplace=True)
df["عدد_العملاء"].fillna(df["عدد_العملاء"].median(), inplace=True)

# 5️⃣ رسم وتحليل
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("📊 تقرير أداء المبيعات", fontsize=16, fontweight="bold")

# رسم 1: مبيعات مع الوقت
axes[0, 0].plot(df["التاريخ"], df["المبيعات"], color="blue", alpha=0.7)
axes[0, 0].set_title("المبيعات اليومية")
axes[0, 0].set_xlabel("التاريخ")
axes[0, 0].set_ylabel("المبيعات ($)")
axes[0, 0].grid(True)

# رسم 2: توزيع الأرباح
axes[0, 1].hist(df["الربح"], bins=20, color="green", edgecolor="black")
axes[0, 1].set_title("توزيع الأرباح")
axes[0, 1].set_xlabel("الربح ($)")

# رسم 3: مبيعات حسب الفئة
category_sales = df.groupby("category")["المبيعات"].sum()
axes[1, 0].pie(category_sales, labels=category_sales.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("نسبة المبيعات حسب الفئة")

# رسم 4: علاقة الانطباعات الإعلانية بالمبيعات
axes[1, 1].scatter(df["الانطباعات_الإعلانية"], df["المبيعات"], alpha=0.5, color="red")
axes[1, 1].set_title("الإنطباعات → المبيعات")
axes[1, 1].set_xlabel("الانطباعات الإعلانية")
axes[1, 1].set_ylabel("المبيعات")
axes[1, 1].grid(True)

plt.tight_layout()

# 6️⃣ حفظ الرسم كـ PDF
pdf_path = "output/تقرير_المبيعات.pdf"
plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
print(f"✅ تم حفظ التقرير البياني في:\n   {pdf_path}")

# 7️⃣ عرض الرسم (اختياري)
# plt.show()

# 📦 My Data Tools - مكتبة متكاملة لمعالجة البيانات

مكتبة Python متكاملة لمعالجة البيانات، تحويل الملفات، الإرسال إلى Telegram، وإنشاء تقارير PDF.

## 👤 المؤلف
- **الاسم**: Mouldi
- **البريد الإلكتروني**: mouldi204@gmail.com
- **الإصدار**: 2.0.0

---

## 📋 قائمة الدوال (23 دالة)

### 📊 القسم 1: دوال التحويل (من ملفات إلى DataFrame)

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 1 | `excel_to_dataframe(file_path, sheet_name=0, **kwargs)` | تحويل ملف Excel إلى DataFrame |
| 2 | `csv_to_dataframe(file_path, encoding='utf-8-sig', **kwargs)` | تحويل ملف CSV إلى DataFrame |
| 3 | `google_sheet_to_dataframe(sheet_url, sheet_name=None, credentials_file=None)` | تحويل Google Sheet إلى DataFrame |

### 📝 القسم 2: دوال الكتابة (من DataFrame إلى ملفات)

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 4 | `dataframe_to_excel(df, output_path, sheet_name='Sheet1', **kwargs)` | كتابة DataFrame في ملف Excel |
| 5 | `dataframe_to_csv(df, output_path, encoding='utf-8-sig', **kwargs)` | كتابة DataFrame في ملف CSV |
| 6 | `dataframe_to_pdf(df, output_path, title='تقرير البيانات', orientation='L', include_date=True)` | كتابة DataFrame في ملف PDF |

### 📁 القسم 3: دوال إدارة مجلد output

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 7 | `update_output_excel(df, filename='data.xlsx', output_folder='output', sheet_name='Sheet1', create_backup=True, **kwargs)` | تحديث مجلد output وكتابة Excel |
| 8 | `update_output_multi_excel(dataframes, filename='multi_data.xlsx', output_folder='output', create_backup=True)` | كتابة عدة DataFrames في ملف واحد |
| 9 | `save_with_timestamp(df, prefix='data', output_folder='output', sheet_name='Sheet1', **kwargs)` | حفظ مع إضافة تاريخ ووقت للاسم |
| 10 | `read_latest_excel(output_folder='output', pattern='*.xlsx')` | قراءة آخر ملف Excel تم حفظه |
| 11 | `clean_output_folder(output_folder='output', days_old=30, pattern=None)` | تنظيف مجلد output من الملفات القديمة |

### 🎲 القسم 4: دوال التوليد العشوائي (للتجربة)

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 12 | `generate_random_numbers(count=10, min_value=0, max_value=100, decimal_places=0)` | توليد قائمة بأرقام عشوائية |
| 13 | `generate_random_number(min_value=0, max_value=100, decimal_places=0, count=1, distribution='uniform')` | توليد رقم عشوائي بتوزيعات مختلفة |
| 14 | `generate_random_dataframe(rows=10, columns=None, random_seed=None)` | توليد DataFrame عشوائي كامل |
| 15 | `generate_sales_data(rows=20, start_date='2024-01-01', end_date='2024-12-31')` | توليد بيانات مبيعات عشوائية |
| 16 | `generate_employees_data(rows=15)` | توليد بيانات موظفين عشوائية |
| 17 | `generate_students_data(rows=20)` | توليد بيانات طلاب عشوائية |

### 🤖 القسم 5: دوال الإرسال إلى Telegram

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 18 | `send_telegram_message(bot_token, chat_id, message, parse_mode='HTML')` | إرسال رسالة نصية إلى Telegram |
| 19 | `send_csv_link(bot_token, chat_id, file_url, caption='')` | إرسال رابط تحميل ملف CSV |
| 20 | `send_excel_link(bot_token, chat_id, file_url, caption='')` | إرسال رابط تحميل ملف Excel |
| 21 | `send_pdf_link(bot_token, chat_id, file_url, caption='')` | إرسال رابط تحميل ملف PDF |
| 22 | `send_any_file_link(bot_token, chat_id, file_url, file_name='ملف', caption='')` | إرسال رابط تحميل أي ملف |

### 🛠️ القسم 6: دوال مساعدة

| رقم | الدالة | الوصف |
|-----|--------|-------|
| 23 | `get_dataframe_info(df)` | الحصول على معلومات مفصلة عن DataFrame |

---

## 🚀 التثبيت

### الطريقة 1: تثبيت المكتبات المطلوبة فقط

```bash
pip install pandas openpyxl requests fpdf2 numpy

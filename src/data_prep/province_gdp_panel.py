import pandas as pd
import numpy as np

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# 1. Load Excel 
excel_path = str(ROOT / "data/GDP/ts_hesab_mantagheii_jari_sabet_1390-1400-14031029111424.xlsx")
sheet_name = "ارزش افزوده به قیمت ثابت"

# 2.Reading the sheet
df = pd.read_excel(excel_path, sheet_name=sheet_name, skiprows=1)

# 3. Saving years
df.columns = [str(col).strip() for col in df.columns]

# 4. Saving province GDP
df_all_provinces = df[df['act_code'] == 'Y40'].copy()

id_columns = ['کد استان', 'نام استان', 'act_code']

years_columns = [str(y) for y in range(1390, 1401)]

panel_df = df_all_provinces.melt(
    id_vars=id_columns, 
    value_vars=years_columns,
    var_name='Year',           # نام ستون جدید برای سال‌ها
    value_name='GDP_Constant'  # نام ستون جدید برای مقادیر GDP
)
print("ساختار جدید (Panel Data):")
print(panel_df.sort_values(['نام استان', 'Year']).head(12))

# ۵. چک کردن تعداد کل ردیف‌ها
# باید ۳۴۱ ردیف باشد (۳۱ استان در ۱۱ سال)
print(f"\nتعداد کل ردیف‌ها در پنل دیتا: {len(panel_df)}")

# ۱. تبدیل ستون سال به عدد صحیح
panel_df['Year'] = panel_df['Year'].astype(int)

# ۲. تبدیل ستون GDP به عدد اعشاری (گاهی اوقات ممکنه به صورت متن خونده شده باشه)
panel_df['GDP_Constant'] = pd.to_numeric(panel_df['GDP_Constant'], errors='coerce')

# ۳. مرتب‌سازی نهایی: اول بر اساس نام استان (الفبایی) و بعد بر اساس سال (صعودی)
panel_df = panel_df.sort_values(by=['نام استان', 'Year']).reset_index(drop=True)

# ۴. نمایش ۱۰ ردیف اول برای یک استان خاص (مثلاً آذربایجان شرقی)
print("داده‌های مرتب شده برای اولین استان در لیست:")
print(panel_df.head(11))

# ۵. چک کردن نوع داده‌ها (Dtypes)
print("\nنوع داده‌های هر ستون:")
print(panel_df.dtypes)

# مسیر ذخیره فایل نهایی (نام دلخواه خودت رو بذار)
output_file = str(ROOT / "data/GDP/Final_Panel_Data_Y40.csv")

# ذخیره به صورت CSV
# encoding='utf-8-sig' باعث میشه اسامی فارسی استان‌ها در اکسل درست نشون داده بشه
panel_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\nتبریک! فایل نهایی با موفقیت در این مسیر ذخیره شد:\n{output_file}")


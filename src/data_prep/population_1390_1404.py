import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# -----------------------------
# تنظیم مسیرها
# -----------------------------
input_path = str(ROOT / "data/Pop/Population_90_95.xlsx")          # مسیر فایل ورودی خودت
output_path = str(ROOT / "data/Pop/Province_Population_1390_1404.xlsx")  # نام خروجی طبق خواسته شما

# -----------------------------
# نرمال‌سازی متن فارسی (برای یکدست شدن نام استان‌ها)
# -----------------------------
def fa_normalize(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = s.replace("ي", "ی").replace("ك", "ک")
    s = s.replace("\u200c", " ")  # نیم‌فاصله -> فاصله
    s = " ".join(s.split())       # فاصله‌های اضافه
    return s

# -----------------------------
# مپ انگلیسی استان‌ها
# (اگر استان‌های فایل شما دقیقاً این نام‌ها را داشته باشند، همه پوشش داده می‌شود)
# -----------------------------
province_en = {
    "آذربایجان شرقی": "East Azerbaijan",
    "آذربایجان غربی": "West Azerbaijan",
    "اردبیل": "Ardabil",
    "اصفهان": "Isfahan",
    "البرز": "Alborz",
    "ایلام": "Ilam",
    "بوشهر": "Bushehr",
    "تهران": "Tehran",
    "چهارمحال و بختیاری": "Chaharmahal and Bakhtiari",
    "خراسان جنوبی": "South Khorasan",
    "خراسان رضوی": "Razavi Khorasan",
    "خراسان شمالی": "North Khorasan",
    "خوزستان": "Khuzestan",
    "زنجان": "Zanjan",
    "سمنان": "Semnan",
    "سیستان و بلوچستان": "Sistan and Baluchestan",
    "فارس": "Fars",
    "قزوین": "Qazvin",
    "قم": "Qom",
    "کردستان": "Kurdistan",
    "کرمان": "Kerman",
    "کرمانشاه": "Kermanshah",
    "کهگیلویه و بویراحمد": "Kohgiluyeh and Boyer-Ahmad",
    "گلستان": "Golestan",
    "گیلان": "Gilan",
    "لرستان": "Lorestan",
    "مازندران": "Mazandaran",
    "مرکزی": "Markazi",
    "هرمزگان": "Hormozgan",
    "همدان": "Hamadan",
    "یزد": "Yazd",
}

def add_english_name(fa_name: str) -> str:
    fa_name_n = fa_normalize(fa_name)
    en = province_en.get(fa_name_n)
    return f"{fa_name_n} ({en})" if en else fa_name_n

# -----------------------------
# 1) خواندن شیت‌ها
# -----------------------------
df_90_95 = pd.read_excel(input_path, sheet_name="Sheet1")          # 1390 تا 1395 (عدد کامل)
df_forecast = pd.read_excel(input_path, sheet_name="خلاصه استانی") # 1396 تا 1415 (هزار نفر)

# -----------------------------
# 2) تمیزکاری شیت Forecast
# -----------------------------
df_forecast = df_forecast.rename(columns={
    df_forecast.columns[0]: "Province",
    df_forecast.columns[1]: "Year",
    df_forecast.columns[2]: "Total_k"  # هزار نفر
})

df_forecast["Province"] = df_forecast["Province"].apply(fa_normalize)

df_forecast = df_forecast[pd.to_numeric(df_forecast["Year"], errors="coerce").notna()].copy()
df_forecast["Year"] = df_forecast["Year"].astype(int)

df_forecast["Total_k"] = pd.to_numeric(df_forecast["Total_k"], errors="coerce")
df_forecast = df_forecast[df_forecast["Total_k"].notna()].copy()

# فقط 1396 تا 1404
df_forecast = df_forecast[(df_forecast["Year"] >= 1396) & (df_forecast["Year"] <= 1404)].copy()

# هزار نفر -> نفر
df_forecast["Population"] = (df_forecast["Total_k"] * 1000).round().astype(int)
df_forecast = df_forecast[["Province", "Year", "Population"]]

# -----------------------------
# 3) تبدیل Sheet1 (1390-1395) به لانگ
# -----------------------------
df_90_95 = df_90_95.rename(columns={"نام استان": "Province"})
df_90_95["Province"] = df_90_95["Province"].apply(fa_normalize)

year_cols_90_95 = [c for c in df_90_95.columns if str(c).isdigit()]  # 1390..1395
df_90_95_long = df_90_95.melt(
    id_vars=["Province"],
    value_vars=year_cols_90_95,
    var_name="Year",
    value_name="Population"
)
df_90_95_long["Year"] = df_90_95_long["Year"].astype(int)
df_90_95_long["Population"] = pd.to_numeric(df_90_95_long["Population"], errors="coerce").round().astype("Int64")

# -----------------------------
# 4) ادغام کل بازه 1390-1404
# -----------------------------
df_all_long = pd.concat([df_90_95_long, df_forecast], ignore_index=True)
df_all_long = df_all_long[(df_all_long["Year"] >= 1390) & (df_all_long["Year"] <= 1404)].copy()

df_all_long = df_all_long.dropna(subset=["Population"]).copy()
df_all_long["Population"] = df_all_long["Population"].astype(int)

# سال میلادی (تقریب رایج برای سال‌های شمسی)
df_all_long["Year_Greg"] = df_all_long["Year"] + 621

# -----------------------------
# 5) اضافه کردن نام انگلیسی کنار استان
# -----------------------------
df_all_long["Province_EN"] = df_all_long["Province"].map(lambda x: province_en.get(fa_normalize(x), ""))
df_all_long["Province_Display"] = df_all_long["Province"].map(add_english_name)

# -----------------------------
# 6) Wide (استان‌ها سطری، سال‌ها ستونی) + کل کشور
# -----------------------------
years = list(range(1390, 1405))

df_wide = df_all_long.pivot_table(
    index=["Province_Display"],
    columns="Year",
    values="Population",
    aggfunc="first"
).reset_index()

# مرتب‌سازی ستون‌ها
df_wide = df_wide[["Province_Display"] + years]
df_wide = df_wide.rename(columns={"Province_Display": "Province"})

# کل کشور
iran_row = {"Province": "کل کشور (Iran)"}
for y in years:
    iran_row[y] = int(df_wide[y].sum())
df_wide = pd.concat([df_wide, pd.DataFrame([iran_row])], ignore_index=True)

# -----------------------------
# 7) Long + کل کشور
# -----------------------------
iran_long = pd.DataFrame({
    "Province": ["کل کشور"] * len(years),
    "Province_EN": ["Iran"] * len(years),
    "Province_Display": ["کل کشور (Iran)"] * len(years),
    "Year": years,
})
iran_long["Population"] = [int(df_all_long[df_all_long["Year"] == y]["Population"].sum()) for y in years]
iran_long["Year_Greg"] = iran_long["Year"] + 621

df_long_with_iran = pd.concat(
    [df_all_long[["Province","Province_EN","Province_Display","Year","Year_Greg","Population"]], iran_long],
    ignore_index=True
)

# -----------------------------
# 8) Year map
# -----------------------------
df_year_map = pd.DataFrame({
    "Year_SH": years,
    "Year_Greg": [y + 621 for y in years]
})

# -----------------------------
# 9) ذخیره خروجی
# -----------------------------
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_wide.to_excel(writer, sheet_name="Province_Wide", index=False)
    df_long_with_iran.to_excel(writer, sheet_name="Province_Long", index=False)
    df_year_map.to_excel(writer, sheet_name="Year_Map", index=False)

print("✅ Done! Saved:", output_path)
print("Sheets: Province_Wide, Province_Long, Year_Map")


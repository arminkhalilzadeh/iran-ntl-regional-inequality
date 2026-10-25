import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


def normalize_names(text):
    if pd.isna(text): return text
    text = str(text).replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').strip()
    if 'کهگیلویه' in text or 'کهکیلویه' in text: return 'کهگیلویه و بویراحمد'
    if 'سیستان' in text: return 'سیستان و بلوچستان'
    if 'چهارمحال' in text: return 'چهارمحال و بختیاری'
    return text

# مسیرها
pop_path = str(ROOT / "data/Pop/Population_90_95.xlsx")
gdp_path = str(ROOT / "data/GDP/ts_hesab_mantagheii_jari_sabet_1390-1400-14031029111424.xlsx")

# ۱. جمعیت ۹۰ تا ۹۵ (واحد: نفر)
df_pop_low = pd.read_excel(pop_path, sheet_name='Sheet1')
df_pop_low['نام استان'] = df_pop_low['نام استان'].apply(normalize_names)
pop_90_95 = df_pop_low.melt(id_vars=['نام استان'], var_name='Year', value_name='Population')

# ۲. جمعیت ۹۶ تا ۱۴۰۰ (واحد: هزار نفر -> باید به نفر تبدیل شود)
df_pop_high = pd.read_excel(pop_path, sheet_name='خلاصه استانی', skiprows=3, header=None)[[0, 1, 2]]
df_pop_high.columns = ['نام استان', 'Year', 'Population']
df_pop_high['نام استان'] = df_pop_high['نام استان'].ffill().apply(normalize_names)
# اصلاح واحد:
df_pop_high['Population'] = pd.to_numeric(df_pop_high['Population'], errors='coerce') * 1000 
pop_96_1400 = df_pop_high[df_pop_high['Year'].isin(range(1396, 1401))]

# ترکیب دو بازه
full_pop = pd.concat([pop_90_95, pop_96_1400])
full_pop['Year'] = full_pop['Year'].astype(int)

# ۳. داده‌های GDP
df_gdp = pd.read_excel(gdp_path, sheet_name='ارزش افزوده به قیمت ثابت', skiprows=1)
df_gdp['نام استان'] = df_gdp['نام استان'].apply(normalize_names)
df_y40 = df_gdp[(df_gdp['act_code'] == 'Y40') & (~df_gdp['نام استان'].isin(['فرامنطقه ای', 'کشور', 'جمع کل استان ها']))].copy()
df_gdp_long = df_y40.melt(id_vars=['نام استان'], value_vars=list(range(1390, 1401)), var_name='Year', value_name='GDP')
df_gdp_long['Year'] = df_gdp_long['Year'].astype(int)

# ۴. ادغام نهایی
final_df = pd.merge(df_gdp_long, full_pop, on=['نام استان', 'Year'], how='inner')
final_df['GDP_per_Capita'] = final_df['GDP'] / final_df['Population']

print(f"تعداد ردیف‌ها: {len(final_df)}")
print("نمونه جمعیت ۱۴۰۰ (باید میلیونی باشد):")
print(final_df[final_df['Year'] == 1400][['نام استان', 'Population']].head())

final_df.to_csv(str(ROOT / "data/Master_Data_Corrected.csv"), index=False, encoding='utf-8-sig')
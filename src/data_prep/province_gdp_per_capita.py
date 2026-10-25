import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


def clean_province_names(text):
    if pd.isna(text): return text
    text = str(text).replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').strip()
    
    # واژه‌نامه اصلاح اسامی برای جفت شدن قطعی (بر اساس خطای سیستم شما)
    if 'کهگیلویه' in text or 'کهکیلویه' in text:
        return 'کهگیلویه و بویراحمد'
    if 'سیستان' in text:
        return 'سیستان و بلوچستان'
    if 'چهارمحال' in text:
        return 'چهارمحال و بختیاری'
    
    return text

# مسیرها را چک کن
pop_path = str(ROOT / "data/Pop/Population_90_95.xlsx")
gdp_path = str(ROOT / "data/GDP/ts_hesab_mantagheii_jari_sabet_1390-1400-14031029111424.xlsx")

# ۱. پردازش جمعیت (۹۰ تا ۱۴۰۰)
df_pop_low = pd.read_excel(pop_path, sheet_name='Sheet1')
df_pop_low['نام استان'] = df_pop_low['نام استان'].apply(clean_province_names)
pop_panel = df_pop_low.melt(id_vars=['نام استان'], var_name='Year', value_name='Population')

df_pop_high = pd.read_excel(pop_path, sheet_name='خلاصه استانی', skiprows=3, header=None)[[0, 1, 2]]
df_pop_high.columns = ['نام استان', 'Year', 'Population']
df_pop_high['نام استان'] = df_pop_high['نام استان'].ffill().apply(clean_province_names)
df_pop_high['Population'] = df_pop_high['Population'] * 1000

full_pop = pd.concat([pop_panel, df_pop_high[df_pop_high['Year'].isin(range(1396, 1401))]])
full_pop['Year'] = full_pop['Year'].astype(int)

# ۲. پردازش GDP
df_gdp = pd.read_excel(gdp_path, sheet_name='ارزش افزوده به قیمت ثابت', skiprows=1)
df_gdp['نام استان'] = df_gdp['نام استان'].apply(clean_province_names)

# فیلتر Y40 و حذف موارد غیر استانی (فرامنطقه‌ای و کل کشور)
invalid_names = ['فرامنطقه ای', 'جمع کل استان ها', 'کشور']
df_y40 = df_gdp[(df_gdp['act_code'] == 'Y40') & (~df_gdp['نام استان'].isin(invalid_names))].copy()

years_cols = list(range(1390, 1401))
df_gdp_long = df_y40.melt(id_vars=['نام استان'], value_vars=years_cols, var_name='Year', value_name='GDP')
df_gdp_long['Year'] = df_gdp_long['Year'].astype(int)

# ۳. ادغام (Merge)
final_df = pd.merge(df_gdp_long, full_pop, on=['نام استان', 'Year'], how='inner')

# ۴. محاسبه سرانه
final_df['GDP_per_Capita'] = final_df['GDP'] / final_df['Population']

final_df.to_csv(str(ROOT / "data/GDP_per_capita/Province_GDP_per_capita.csv"), index=False, encoding='utf-8-sig')
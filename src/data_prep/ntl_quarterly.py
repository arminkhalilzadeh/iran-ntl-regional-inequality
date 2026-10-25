import pandas as pd
import numpy as np

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# آدرس‌ها
ntl_path = str(ROOT / "data/Master_NTL/Iran_Monthly_sum&meanNTL_Master_2012_2024_withShamsi.csv")
output_path = str(ROOT / "data/Iran_NTL/Iran_NTL_Quarterly_2012_2024.csv")

# خواندن داده
df = pd.read_csv(ntl_path)

# فیلتر کردن فقط کل ایران
iran_df = df[df['Area'] == 'Iran (National)'].copy()

print(f"تعداد سطرهای ماهانه کل ایران: {len(iran_df)}")

# تعریف فصل بر اساس ماه میلادی
def get_quarter(month):
    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    else:  # 10, 11, 12
        return 4

iran_df['Quarter'] = iran_df['Month'].apply(get_quarter)

# محاسبه هم mean و هم sum برای فصلی
quarterly = iran_df.groupby(['Year', 'Quarter']).agg({
    'Mean_Radiance': ['mean', 'sum'],
    'Sum_Radiance': ['mean', 'sum'],
    'Shamsi_Year': 'first',
    'Shamsi_Month': 'first'
}).reset_index()

# صاف کردن ستون‌ها
quarterly.columns = ['Year', 'Quarter', 
                     'Mean_Radiance_avg', 'Mean_Radiance_sum',
                     'Sum_Radiance_avg', 'Sum_Radiance_sum',
                     'Shamsi_Year', 'Shamsi_Month']

# مرتب‌سازی
quarterly = quarterly.sort_values(['Year', 'Quarter']).reset_index(drop=True)

# ذخیره
quarterly.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ فایل ذخیره شد: {output_path}")
print(f"تعداد سطرهای فصلی: {len(quarterly)}")
print("\nنمونه داده:")
print(quarterly.head(10))


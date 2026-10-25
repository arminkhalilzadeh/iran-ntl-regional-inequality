import pandas as pd
import os

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# -----------------------------
# Step 1: File paths
# -----------------------------

ntl_file = str(ROOT / "data/Iran_Province_NTL_Annual/Iran_Annual_NTL_Master_2012_2024.csv")
pop_file = str(ROOT / "data/Pop/Province_Population_1390_1404.xlsx")

output_dir = os.path.dirname(ntl_file)
output_name = os.path.join(
    output_dir,
    'Iran_Annual_NTLperCapita_Master_2012_2024.csv'
)

# -----------------------------
# Step 2: Load data
# -----------------------------

df_ntl = pd.read_csv(ntl_file)
df_pop = pd.read_excel(pop_file, sheet_name='Province_Long')

# -----------------------------
# Step 3: Remove national row
# -----------------------------

df_ntl = df_ntl[df_ntl['Area'] != 'Iran (National)'].copy()

# -----------------------------
# Step 4: Clean province names
# -----------------------------

df_ntl['Area_clean'] = df_ntl['Area'].astype(str).str.strip()
df_pop['Province_clean'] = df_pop['Province_EN'].astype(str).str.strip()

name_fix = {
    'East Azarbaijan': 'East Azerbaijan',
    'West Azarbaijan': 'West Azerbaijan',
    'Kohgiluyeh and Boyer-Ahmad': 'Kohgiluyeh & Boyerahmad',
    'Kohgiluyeh And Boyer-Ahmad': 'Kohgiluyeh & Boyerahmad',
    'Chahar Mahaal and Bakhtiari': 'Chaharmahal and Bakhtiari',
    'Hamedan': 'Hamadan',
    'fars': 'Fars',
    'Sistan and Baluchistan': 'Sistan and Baluchestan'
}

df_ntl['Area_clean'] = df_ntl['Area_clean'].replace(name_fix)
df_pop['Province_clean'] = df_pop['Province_clean'].replace(name_fix)

# -----------------------------
# Step 5: Prepare population data
# -----------------------------

df_pop_subset = df_pop[
    ['Province_clean', 'Year_Greg', 'Population', 'Year']
].rename(columns={
    'Year': 'Year_Shamsi_Actual'
})

# -----------------------------
# Step 6: Merge NTL and population
# -----------------------------

df_merged = pd.merge(
    df_ntl,
    df_pop_subset,
    left_on=['Area_clean', 'Year'],
    right_on=['Province_clean', 'Year_Greg'],
    how='left',
    indicator=True
)

# -----------------------------
# Step 7: Check unmatched rows
# -----------------------------

print("Merge status:")
print(df_merged['_merge'].value_counts())

unmatched = df_merged[df_merged['_merge'] != 'both'][['Area', 'Area_clean', 'Year']]
print("\nUnmatched rows:")
print(unmatched.drop_duplicates())

# Keep only matched rows
df_merged = df_merged[df_merged['_merge'] == 'both'].copy()

# -----------------------------
# Step 8: Create Shamsi year
# -----------------------------

df_merged['Year_Shamsi_NTL'] = df_merged['Year'] - 621

# -----------------------------
# Step 9: Calculate NTL per capita
# -----------------------------

df_merged['NTL_Per_Capita'] = df_merged['Annual_Sum'] / df_merged['Population']

# -----------------------------
# Step 10: Final dataset
# -----------------------------

final_columns = [
    'Area_clean',
    'Year',
    'Year_Shamsi_NTL',
    'Annual_Sum',
    'Annual_Mean',
    'Population',
    'NTL_Per_Capita'
]

df_final = df_merged[final_columns].rename(columns={
    'Area_clean': 'Area'
})

# -----------------------------
# Step 11: Export
# -----------------------------

df_final.to_csv(output_name, index=False, encoding='utf-8-sig')

print("\nSaved:", output_name)
print("Rows:", len(df_final))
print("Provinces:", df_final['Area'].nunique())
print(sorted(df_final['Area'].unique()))
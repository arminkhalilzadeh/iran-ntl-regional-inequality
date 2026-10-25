import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# --- Step 1: Paths ---
data_path = str(ROOT / "data/Iran_Province_NTL_Annual/Iran_Annual_NTL_Master_2012_2024.csv")
pop_path = str(ROOT / "data/Pop/Province_Population_1390_1404.xlsx")
shapefile_path = str(ROOT / "data/shapefile/iran.shp")
output_folder = str(ROOT / "output/Province_NTL_graph")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# --- Step 2: Ultimate Name Normalization Function ---
def standardize_name(name):
    if pd.isna(name): return name
    name = str(name).strip().lower()
    
    # Precise dictionary to map any variation to a standard name
    mapping = {
        'hamadan': 'Hamadan', 'hamedan': 'Hamadan',
        'sistan': 'Sistan and Baluchistan', 'baluchistan': 'Sistan and Baluchistan', 'baluchestan': 'Sistan and Baluchistan',
        'chahar': 'Chaharmahal and Bakhtiari', 'bakhtiari': 'Chaharmahal and Bakhtiari', 'mahaal': 'Chaharmahal and Bakhtiari',
        'azerbaijan': 'Azerbaijan', 'azarbaijan': 'Azerbaijan',
        'kohgiluyeh': 'Kohgiluyeh and Boyer-Ahmad', 'boyer': 'Kohgiluyeh and Boyer-Ahmad',
        'khorasan razavi': 'Razavi Khorasan', 'razavi': 'Razavi Khorasan',
        'south khorasan': 'South Khorasan', 'north khorasan': 'North Khorasan'
    }
    
    for key, value in mapping.items():
        if key in name:
            return value
    return name.title()

# --- Step 3: Load and Merge Data (Fixing the Year Conflict) ---
df_ntl = pd.read_csv(data_path)
df_pop = pd.read_excel(pop_path, sheet_name='Province_Long')

# Standardize names BEFORE merging
df_ntl['Area_Std'] = df_ntl['Area'].apply(standardize_name)
df_pop['Province_Std'] = df_pop['Province_EN'].apply(standardize_name)

# Rename 'Year' in population data to avoid conflict with NTL 'Year'
df_pop_clean = df_pop.rename(columns={'Year': 'Year_Shamsi'})

# Inner merge to ensure only matched provinces stay
df_merged = pd.merge(
    df_ntl, 
    df_pop_clean, 
    left_on=['Area_Std', 'Year'], 
    right_on=['Province_Std', 'Year_Greg'], 
    how='inner'
)

# Calculate Per Capita
df_merged['NTL_Per_Capita'] = df_merged['Annual_Sum'] / df_merged['Population']
print(f"✅ Master data merged. Total provinces matched: {df_merged['Area_Std'].nunique()}")

# --- Step 4: Load Shapefile and Match Names ---
gdf = gpd.read_file(shapefile_path)
# Check for 'Name_1' (case sensitive)
shape_col = 'Name_1' if 'Name_1' in gdf.columns else 'NAME_1'
gdf['name_std'] = gdf[shape_col].apply(standardize_name)

# --- Step 5: Map Generation Function ---
def save_single_map(year, filename):
    # Filter for the year
    df_year = df_merged[df_merged['Year'] == year][['Area_Std', 'NTL_Per_Capita']]
    
    # Merge Shapefile with Data
    merged_map = gdf.merge(df_year, left_on='name_std', right_on='Area_Std', how='left')
    
    # Check for missing data in the map
    missing = merged_map[merged_map['NTL_Per_Capita'].isna()]['name_std'].tolist()
    if missing:
        print(f"⚠️ Warning for {year}: These provinces are white: {missing}")

    fig, ax = plt.subplots(figsize=(14, 12), dpi=300)
    
    # Shared color scale for 2012 and 2024
    vmin = df_merged['NTL_Per_Capita'].min()
    vmax = df_merged['NTL_Per_Capita'].max()

    merged_map.plot(
        column='NTL_Per_Capita', 
        ax=ax, 
        cmap='OrRd', 
        edgecolor='black', 
        linewidth=0.5, 
        vmin=vmin, 
        vmax=vmax, 
        legend=True,
        legend_kwds={'label': "Nighttime Light per Capita Index", 'orientation': "vertical", 'shrink': 0.6}
    )

    # Add Province Labels
    for _, row in merged_map.iterrows():
        if row.geometry:
            centroid = row.geometry.representative_point()
            ax.text(centroid.x, centroid.y, row['name_std'], fontsize=8, ha='center', 
                    fontweight='bold', bbox=dict(facecolor='white', alpha=0.4, edgecolor='none'))

    ax.set_title(f'Iran Nighttime Light per Capita - Year {year}', fontsize=18, fontweight='bold', pad=25)
    ax.set_axis_off()
    
    save_path = os.path.join(output_folder, filename)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"✅ Map for {year} saved successfully at {filename}")

# --- Step 6: Generate Separate Images ---
save_single_map(2012, 'Map_NTL_PerCapita_2012.png')
save_single_map(2024, 'Map_NTL_PerCapita_2024.png')
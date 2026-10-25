import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# --- Step 1: Paths ---
# Ensure this matches your actual merged file path
input_file = str(ROOT / "data/Iran_Province_NTL_Annual/Iran_Annual_NTLperCapita_Master_2012_2024.csv")
# Save output in the same folder as the script or NTL folder
output_image = str(ROOT / "output/Province_NTL_graph/Province_NTLperCapita_bar_2013vs2024.png")
# --- Step 2: Load Data ---
if not os.path.exists(input_file):
    print(f"Error: File not found at {input_file}")
else:
    df = pd.read_csv(input_file)
    
    # --- Step 3: Filter for 2013 and 2024 ---
    y1, y2 = 2013, 2024
    df_filtered = df[df['Year'].isin([y1, y2])].copy()

    # Pivot: Index = Province (Area), Columns = Years, Values = Per Capita NTL
    plot_df = df_filtered.pivot(index='Area', columns='Year', values='NTL_Per_Capita')
    
    # Sort provinces by 2024 values for a professional look
    plot_df = plot_df.sort_values(by=y2, ascending=False)

    # --- Step 4: Visualization ---
    plt.style.use('ggplot') # Clean academic style
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)

    x = np.arange(len(plot_df.index))
    width = 0.35

    # Grouped Bars
    ax.bar(x - width/2, plot_df[y1], width, label=str(y1), color='#3498db', edgecolor='black', alpha=0.8)
    ax.bar(x + width/2, plot_df[y2], width, label=str(y2), color='#e74c3c', edgecolor='black', alpha=0.8)

    # Labels and Titles
    ax.set_ylabel('NTL per Capita (Radiance / Population)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparison of Nighttime Light per Capita by Province ({y1} vs {y2})', fontsize=16, pad=20, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df.index, rotation=45, ha='right', fontsize=10)
    ax.legend(title="Year", fontsize=12)

    # Formatting
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # --- Step 5: Save ---
    plt.savefig(output_image)
    print(f"✅ Success! Bar chart saved at:\n{output_image}")
    plt.show()
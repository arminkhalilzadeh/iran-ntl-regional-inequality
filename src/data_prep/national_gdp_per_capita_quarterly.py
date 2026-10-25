import os
import pandas as pd
import numpy as np

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


gdp_path = str(ROOT / "data/GDP/Iran_GDP_Quarterly.xlsx")
pop_path = str(ROOT / "data/Pop/Province_Population_1390_1404.xlsx")

out_dir = str(ROOT / "data/GDP_per_capita")
out_file = r"National_GDP_per_capita_Quarterly.xlsx"
out_path = os.path.join(out_dir, out_file)

os.makedirs(out_dir, exist_ok=True)

# -----------------------------
# 1) Read GDP quarterly (national) from Table 3 (constant prices)
# -----------------------------
# This sheet contains rows like 1390_1, 1390_2, ...
raw_gdp = pd.read_excel(gdp_path, sheet_name="3", header=None, engine="openpyxl")

time_col = raw_gdp.iloc[:, 1].astype(str).str.strip()
is_quarter = time_col.str.match(r"^\d{4}_\d$")

# Column 20: GDP (base prices) | Column 21: GDP (non-oil)
gdp_q = raw_gdp.loc[is_quarter, [1, 20, 21]].copy()
gdp_q.columns = ["YearQuarter", "GDP_total_bilRial", "GDP_non_oil_bilRial"]

gdp_q[["Year", "Quarter"]] = gdp_q["YearQuarter"].str.split("_", expand=True)
gdp_q["Year"] = pd.to_numeric(gdp_q["Year"], errors="coerce").astype("Int64")
gdp_q["Quarter"] = pd.to_numeric(gdp_q["Quarter"], errors="coerce").astype("Int64")

gdp_q["GDP_total_bilRial"] = pd.to_numeric(gdp_q["GDP_total_bilRial"], errors="coerce")
gdp_q["GDP_non_oil_bilRial"] = pd.to_numeric(gdp_q["GDP_non_oil_bilRial"], errors="coerce")

gdp_q = gdp_q.dropna(subset=["Year", "Quarter", "GDP_total_bilRial", "GDP_non_oil_bilRial"]).reset_index(drop=True)

# -----------------------------
# 2) Read population (provincial annual) and build NATIONAL annual
#    Fix: avoid double counting (remove "Iran / کل کشور" if present)
# -----------------------------
pop_wide = pd.read_excel(pop_path, engine="openpyxl")

prov_str = pop_wide["Province"].astype(str)

# Detect if a "national total" row exists
mask_total = prov_str.str.contains(r"کل\s*کشور|^Iran$|Iran\s*\(|^IRAN$|National", case=False, regex=True)

year_cols = [c for c in pop_wide.columns if str(c).strip().isdigit()]  # e.g., 1390..1404

if mask_total.any():
    # Use the national total row directly (no summing provinces)
    pop_total_row = pop_wide.loc[mask_total, year_cols].iloc[0]
    pop_nat = (
        pop_total_row
        .reset_index()
        .rename(columns={"index": "Year", 0: "Population"})
    )
    pop_nat["Year"] = pd.to_numeric(pop_nat["Year"], errors="coerce").astype("Int64")
    pop_nat["Population"] = pd.to_numeric(pop_nat["Population"], errors="coerce")
else:
    # Sum provinces to get national total
    pop_no_total = pop_wide.copy()
    pop_no_total[year_cols] = pop_no_total[year_cols].apply(pd.to_numeric, errors="coerce")
    pop_nat = pop_no_total[year_cols].sum(axis=0).reset_index()
    pop_nat.columns = ["Year", "Population"]
    pop_nat["Year"] = pd.to_numeric(pop_nat["Year"], errors="coerce").astype("Int64")
    pop_nat["Population"] = pd.to_numeric(pop_nat["Population"], errors="coerce")

pop_nat = pop_nat.dropna(subset=["Year", "Population"]).sort_values("Year").reset_index(drop=True)

# -----------------------------
# 3) Expand annual population to quarterly (assume constant within year)
# -----------------------------
pop_nat_q = pop_nat.loc[pop_nat["Year"].isin(gdp_q["Year"].unique())].copy()

pop_nat_q = pop_nat_q.loc[pop_nat_q.index.repeat(4)].reset_index(drop=True)
pop_nat_q["Quarter"] = np.tile([1, 2, 3, 4], int(len(pop_nat_q) / 4))

# -----------------------------
# 4) Merge and compute per-capita (Rial/person)
#    GDP is in billion Rial => multiply by 1e9
# -----------------------------
df = pd.merge(gdp_q, pop_nat_q, on=["Year", "Quarter"], how="left")

df["GDP_per_capita_Rial"] = (df["GDP_total_bilRial"] * 1e9) / df["Population"]
df["GDP_non_oil_per_capita_Rial"] = (df["GDP_non_oil_bilRial"] * 1e9) / df["Population"]

# Optional: in million Rial/person for easier reading
df["GDP_per_capita_millionRial"] = df["GDP_per_capita_Rial"] / 1e6
df["GDP_non_oil_per_capita_millionRial"] = df["GDP_non_oil_per_capita_Rial"] / 1e6

# Final tidy table
out = df[
    ["Year", "Quarter", "Population",
     "GDP_total_bilRial", "GDP_non_oil_bilRial",
     "GDP_per_capita_Rial", "GDP_non_oil_per_capita_Rial",
     "GDP_per_capita_millionRial", "GDP_non_oil_per_capita_millionRial"]
].sort_values(["Year", "Quarter"]).reset_index(drop=True)

# -----------------------------
# 5) Save
# -----------------------------
out.to_excel(out_path, index=False)
print("Saved to:", out_path)
print(out.head())
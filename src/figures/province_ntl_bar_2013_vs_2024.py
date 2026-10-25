import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


# =========================
# Inputs (edit if needed)
# =========================
annual_path = Path(str(ROOT / "data/Iran_Province_NTL/Iran_Annual_NTLperCapita_Master_2012_2024.csv"))

Y0, Y1 = 2013, 2024
TOP_N = None  # set None for all provinces

# =========================
# Load + reshape
# =========================
a = pd.read_csv(annual_path)
a.columns = a.columns.str.strip()

df = a[["Area", "Year", "NTL_Per_Capita"]].copy()
df = df.rename(columns={"Area": "province", "Year": "year", "NTL_Per_Capita": "ntl per capita"})
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(int)
df["ntl"] = pd.to_numeric(df["ntl"], errors="coerce")

wide = (df[df["year"].isin([Y0, Y1])]
        .pivot_table(index="province", columns="year", values="ntl", aggfunc="first")
        .reset_index())

wide.columns.name = None
wide = wide.rename(columns={Y0: f"NTL_{Y0}", Y1: f"NTL_{Y1}"})

# Sort by end-year level
wide = wide.sort_values(f"NTL_{Y1}", ascending=False).reset_index(drop=True)
if TOP_N is not None:
    wide = wide.head(TOP_N)

# =========================
# Plot grouped bar chart
# =========================
x = np.arange(len(wide["province"]))
w = 0.40

fig, ax = plt.subplots(figsize=(12, 6), dpi=200)

ax.bar(x - w/2, wide[f"NTL_{Y0}"], width=w, label=f"NTL {Y0}")
ax.bar(x + w/2, wide[f"NTL_{Y1}"], width=w, label=f"NTL {Y1}")

ax.set_title(f"NTL by Province: {Y0} vs {Y1}")
ax.set_xlabel("Province")
ax.set_ylabel("NTL")

ax.set_xticks(x)
ax.set_xticklabels(wide["province"], rotation=90)

ax.legend()
fig.tight_layout()

# =========================
# Save output with your-style naming
# =========================
tag = f"Top{TOP_N}" if TOP_N is not None else "AllProvinces"
out_png = f"IRN_NTL_Province_Bar_Levels_{Y0}_vs_{Y1}_{tag}.png"

plt.savefig(out_png, bbox_inches="tight")
plt.show()

print("Saved:", out_png)

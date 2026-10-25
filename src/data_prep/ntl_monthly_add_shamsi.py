import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repository root


in_path  = str(ROOT / "data/Master_NTL/Iran_Monthly_sum&meanNTL_Master_2012_2024.csv")
out_path = str(ROOT / "data/Master_NTL/Iran_Monthly_sum&meanNTL_Master_2012_2024_withShamsi.csv")

df = pd.read_csv(in_path)

# اگر می‌خوای فقط استان‌ها:
# df = df[df["Type"].astype(str).str.lower().eq("province")].copy()

df["Shamsi_Year"] = df["Year"] - 621
df.loc[df["Month"].isin([1, 2]), "Shamsi_Year"] = df.loc[df["Month"].isin([1, 2]), "Year"] - 622

df["Shamsi_Month"] = df["Month"].map({
    3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 1:11, 2:12
})


df.to_csv(out_path, index=False, encoding="utf-8-sig")
print("Saved:", out_path)

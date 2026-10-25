# Data

Only small, redistributable files are tracked in this repository:

| Path | Description |
|---|---|
| `shapefile/iran.*` | Provincial boundaries of Iran (ESRI shapefile, 31 provinces) |
| `Province_growth_2013-2024/Province_growth_2013_2024.csv` | Provincial NTL change between 2013 and 2024 |

All other inputs are excluded by `.gitignore`. To reproduce the analysis, place them
in the folders below (paths are relative to the repository root):

| Expected path | Content | Source |
|---|---|---|
| `Master_NTL/Iran_Monthly_sum&meanNTL_Master_2012_2024.csv` | Monthly provincial nighttime-light sums and means, 2012–2024 | Satellite NTL composites aggregated to provinces |
| `Iran_Province_NTL_Annual/Iran_Annual_NTL_Master_2012_2024.csv` | Annual provincial NTL, 2012–2024 | Aggregated from the monthly series |
| `GDP/ts_hesab_mantagheii_jari_sabet_1390-1400-*.xlsx` | Provincial accounts (current and constant prices), 1390–1400 | Statistical Centre of Iran |
| `GDP/Iran_GDP_Quarterly.xlsx` | National quarterly GDP (total and non-oil) | Statistical Centre of Iran |
| `Pop/Population_90_95.xlsx` | Provincial population, 1390–1395 | Census of Population and Housing, Statistical Centre of Iran |
| `CPI/ts_national_*.xlsx` | National consumer price index | Statistical Centre of Iran |
| `Validation/HIES_exp_per_capita_provincial_real.xlsx` | Real household expenditure per capita by province | Household Income and Expenditure Survey (via `hbsir`) |

The intermediate files (`Iran_NTL/`, `GDP_per_capita/`, `Pop/Province_Population_1390_1404.xlsx`,
`Validation/*.dta`, …) are produced by the scripts in `src/data_prep/` and the notebooks.

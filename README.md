# Spatial Inequality in Iran: Evidence from Provincial GDP and Nighttime Lights

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Stata](https://img.shields.io/badge/Stata-regressions-1A5F91)
![Data: VIIRS](https://img.shields.io/badge/Data-VIIRS%20Nighttime%20Lights-0B3D91)
![Status](https://img.shields.io/badge/Status-proposal%20defended-success)

**M.Sc. thesis in Economics, Sharif University of Technology**<br>
**Author:** Armin Khalilzadeh · **Supervisor:** Dr. Saeed Tajrishy

This repository contains the code and results for my M.Sc. thesis on spatial inequality across Iran's
31 provinces. It validates VIIRS nighttime lights (2012–2024) against provincial GDP and household
expenditure, and computes population-weighted inequality indices with structural-break tests. To run it,
install `requirements.txt`, put the input data in `data/` as described in `data/README.md`, then run the
scripts in `src/data_prep/` and the notebooks in `notebooks/`.

## 📄 Documents

| | |
|---|---|
| **[Writing sample (PDF, 7 pp.)](docs/Khalilzadeh_Writing_Sample_NTL_Iran.pdf)** | *Measuring Spatial Inequality in Iran with Nighttime Lights: Validation, Gas Flaring and the Limits of a Satellite Proxy.* Preliminary results from this repository, November 2026. |
| **[Thesis proposal (PDF, 30 pp.)](docs/Khalilzadeh_Thesis_Proposal.pdf)** | *Places and People: The Evolution of Spatial Inequality in Iran and Its Relation to Interpersonal Inequality.* English version, November 2026 ([LaTeX source](docs/proposal_latex/)). |
| [Proposal summary](docs/proposal_summary.md) | A short English summary of the research design. |

<p align="center">
  <img src="output/Iran_NTL-overview/Iran_Pro_Map_2024.png" width="640" alt="VIIRS nighttime radiance over Iran, 2024">
</p>

## Abstract

Inequality has two dimensions that do not have to move together: **interpersonal inequality**, the
distribution of welfare across households, and **spatial inequality**, the gap in economic activity across
regions. Iran's national Gini coefficient has been reported since 1984. It stayed at about 0.42–0.43 until
the late 2000s, fell to 0.365 in 2013 and then rose again. No comparable long-run series exists for
spatial inequality, because official provincial GDP covers only part of the period.

This thesis aims to build such a series. So far it estimates the relationship between NTL and provincial
GDP over the years in which both are observed (2012–2021). The next step is to use that relationship to
predict provincial GDP for the missing years, following Lessmann & Seidel (2017). Population-weighted
inequality indices are computed for the years with data; extending them to the completed panel and
comparing them with the national Gini are planned. The aim is to find the turning points and
the periods in which the two kinds of inequality moved together or diverged.

📄 A fuller English summary of the proposal is in [`docs/proposal_summary.md`](docs/proposal_summary.md).

## Research question

> How has spatial inequality of economic activity in Iran changed over the past three decades, and how
> does its path compare with interpersonal inequality?

## Preliminary findings

| Validation test | Result |
|---|---|
| National: log quarterly GDP on log NTL (51 quarters) | Elasticity **0.239*** (SE 0.031), R² = 0.544 |
| National: non-oil GDP | Elasticity **0.246*** (SE 0.036), almost the same, so NTL does not just reflect oil activity |
| Provincial, per capita: pooled log GDP pc on log NTL pc (310 province-years) | Elasticity **0.637*** , R² = 0.499 |
| Provincial, total levels: pooled log GDP on log total radiance (310 province-years) | Elasticity **0.996*** (SE 0.040), R² = 0.674, Pearson r = 0.821, close to one-to-one |
| Provincial, two-way fixed effects (province and year) | Elasticity **0.361**\*\* (SE 0.138); 0.227 (n.s.) when the four gas-flare provinces are excluded |
| Provincial growth, 2012–2021 (1391–1400) | Slope **0.356**\*\* (SE 0.144), R² = 0.175 |
| Rank concordance (GDP pc vs NTL pc) | Spearman ρ between **0.52 and 0.67** in every year (p < 0.01) |

\*\*\* p < 0.01, \*\* p < 0.05.

Deviations from the NTL–GDP relationship follow a pattern. Dense provinces (Tehran, Alborz, Gilan) rank
lower on NTL per capita than on GDP per capita. Sparsely populated provinces (Sistan and Baluchestan,
South Khorasan) rank higher. This is why the planned prediction model includes province fixed effects.

Three further findings shape the design (details in the [writing sample](docs/Khalilzadeh_Writing_Sample_NTL_Iran.pdf)):

- **Gas flaring dominates measured inequality.** Excluding Bushehr, Khuzestan, Ilam and Kohgiluyeh and
  Boyer-Ahmad lowers the lights-based Gini from 0.393 to 0.245 (2012).
- **Places and people diverge.** Between-province inequality in real household expenditure (HIES, excluding
  flare provinces) rose from 0.160 in 2012 to 0.236 in 2024, while the GDP-based Gini stayed at 0.22–0.24
  over 2012–2021.
- **Lights are not welfare.** Within several provinces, lights rose while real expenditure fell (correlation
  −0.78 in East Azerbaijan, −0.63 in Lorestan). A 2017 jump in the lights-based Gini is probably a
  measurement artefact and is being checked. A structural-break test at 2018 is not significant.

<p align="center">
  <img src="output/Validation/Comovement%20of%20GDP%20and%20NTL%20(Quarterly).png" width="49%" alt="Quarterly co-movement of GDP and NTL">
  <img src="output/Inequality/Inequality_Gini_trend.png" width="49%" alt="Population-weighted Gini of NTL, GDP and expenditure">
</p>

## Methodology

1. **Building the panel.** Annual provincial NTL is extracted from VIIRS with Google Earth Engine for
   2012–2024 (1391–1403). It is merged with provincial GDP (Statistical Centre of Iran, constant 2021
   prices) and population. Extension to 1992 (1371) with harmonized DMSP data is the planned next step.
2. **Predicting provincial GDP from NTL.**

   $$\ln(GDP_{it}) = \alpha + \beta \ln(NTL_{it}) + \mu_i + \gamma t + \varepsilon_{it}$$

   The plan is to use this model to predict provincial GDP for years without official accounts and to test
   it by backcasting. A second series that combines GDP and NTL with optimal weights (Henderson,
   Storeygard & Weil, 2012) is planned as a robustness check.
3. **Spatial inequality indices.** Population-weighted Gini, Theil and generalized entropy
   (GE(−1), MLD), plus the coefficient of variation. Each is computed with and without gas-flare areas,
   and tested for a structural break at the 2018 U.S. withdrawal from the JCPOA (not significant).
4. **Comparing the two dimensions (planned).** Correlation in levels and first differences, turning points, and
   lead–lag co-movement between spatial inequality and the national Gini. The analysis is descriptive
   and makes no causal claims.

## Repository structure

```
.
├── data/                  # Inputs (only shapefile and small files tracked; see data/README.md)
├── docs/                  # Writing sample, thesis proposal (PDF + LaTeX) and summary
├── src/
│   ├── data_prep/         # Scripts that build the NTL, population and GDP panels
│   └── figures/           # Scripts for provincial bar charts and maps
├── notebooks/             # Validation and inequality analysis
├── stata/                 # Regression do-file (GDP on NTL)
└── output/                # Figures, tables and regression results
```

<details>
<summary><b>Reproducing the analysis</b></summary>

```bash
git clone https://github.com/arminkhalilzadeh/iran-ntl-regional-inequality.git
cd iran-ntl-regional-inequality
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Put the input data in `data/` as described in [`data/README.md`](data/README.md). All paths are
resolved relative to the repository root.

**1. Data preparation (`src/data_prep/`)**, in this order:

| # | Script | Output |
|---|---|---|
| 1 | `ntl_monthly_add_shamsi.py` | Monthly NTL with Shamsi dates |
| 2 | `ntl_quarterly.py` | National quarterly NTL |
| 3 | `population_1390_1395.py` | Provincial census population, 1390–1395 |
| 4 | `population_1390_1404.py` | Provincial population, interpolated and extrapolated to 1404 |
| 5 | `ntl_per_capita_annual.py` | Annual provincial NTL per capita |
| 6 | `province_gdp_panel.py` | Provincial GDP panel |
| 7 | `province_gdp_per_capita.py` | Provincial GDP per capita (alternative: `province_gdp_master_corrected.py`) |
| 8 | `national_gdp_per_capita.py`, `national_gdp_per_capita_quarterly.py` | National GDP per capita |

**2. Analysis (`notebooks/`)**

| Notebook | Content |
|---|---|
| `ntl_gdp_validation.ipynb` | National and provincial validation of NTL against GDP |
| `hies_gdp_ntl_master.ipynb` | Merges NTL, GDP and HIES expenditure into one provincial dataset |
| `ntl_gdp_expenditure_validation.ipynb` | NTL and GDP against real household expenditure per capita |
| `growth_rank_concordance.ipynb` | Growth and rank concordance |
| `inequality_indices.ipynb` | Inequality indices and structural-break tests |
| `province_ntl_graphs.ipynb` | Provincial NTL graphs |

**3. Regressions:** run `stata/ntl_gdp_validation.do` with the repository root as Stata's working directory.

</details>

## Data sources

- **Nighttime lights:** VIIRS (2012–2024), via Google Earth Engine; extension to 1992 with harmonized DMSP data is planned
- **Provincial and national accounts, population, CPI, national Gini:** Statistical Centre of Iran
- **Household expenditure:** Household Income and Expenditure Survey (HIES), via [`hbsir`](https://pypi.org/project/hbsir/)

## Citation

If you use this code, please cite it using the metadata in [`CITATION.cff`](CITATION.cff)
(GitHub's **Cite this repository** button).

## Contact

**Armin Khalilzadeh**, M.Sc. student in Economics, Sharif University of Technology<br>
Research interests: spatial and regional economics · political economy · microeconometrics<br>
✉️ arminkhalilzadeh@gmail.com · [LinkedIn](https://linkedin.com/in/armin-khalilzadeh)

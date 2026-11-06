# Proposal Summary

**The Evolution of Spatial Inequality in Iran over Three Decades and Its Comparison with Interpersonal
Inequality: An Approach Based on Provincial GDP and Nighttime Lights**

M.Sc. thesis proposal, Graduate School of Management and Economics, Sharif University of Technology
(September 2026)<br>
Author: Armin Khalilzadeh · Supervisor: Dr. Saeed Tajrishy

> This is a condensed summary. The full English proposal (November 2026) is
> [here (PDF)](Khalilzadeh_Thesis_Proposal.pdf), with its [LaTeX source](proposal_latex/).

## 1. Motivation

Economic policy can target **people** or **places**. People-based policies, such as cash transfers and
subsidies, are judged by their effect on the distribution of household welfare (interpersonal inequality),
and the usual measure is the Gini coefficient. Place-based policies, such as regional development budgets,
infrastructure and industrial zones, are judged by their effect on the gap in economic activity across
regions (spatial inequality). The two dimensions are related but can move in opposite directions. A stable
national Gini can hide a widening gap between provinces, and the reverse is also possible. A single
national index can therefore hide important distributional changes.

Measuring spatial inequality separately matters for three reasons:

- **Unequal opportunity.** Where a person lives shapes access to jobs, education, health care and
  infrastructure, whatever their own income.
- **Offsetting components.** The national Gini combines between-province and within-province inequality,
  and these can cancel each other out.
- **Policy evaluation.** Place-based policies need a measure at the same geographic level they target.

Iran makes this distinction especially important. High inflation, sanctions, exchange-rate shocks and a
large informal sector affect provinces differently, depending on their industrial, trade and oil exposure.

## 2. Research question

How has spatial inequality of economic activity in Iran changed over the past three decades, and how does
its path compare with interpersonal inequality?

The aim is to identify the direction of change, the turning points, and the periods in which the two
dimensions moved together or diverged. The analysis does not try to establish a causal link between them.

## 3. Literature and contribution

The project draws on five strands of literature:

1. **Theory of regional inequality.** Williamson's (1965) inverted-U, backwash and spread effects,
   agglomeration economies, and later extensions (Alonso 1980; Amos 1988; Magrini 2004).
2. **Spatial vs. interpersonal inequality.** Novotný (2007), Fratesi & Percoco (2014), Rey (2018) and
   Capello & Cerisola (2024).
3. **NTL as a measure of economic activity.** Chen & Nordhaus (2011), Henderson, Storeygard & Weil (2012),
   Pinkovskiy & Sala-i-Martin (2016) and Gibson et al. (2021).
4. **Measuring regional inequality with NTL.** Lessmann (2014), Lessmann & Seidel (2017), Mveyange (2015)
   and Galimberti et al. (2023).
5. **Empirical studies of Iran.** These use either official statistics with traditional regional methods,
   or NTL for other questions such as sanctions and the informal economy.

**Gap.** No study has built a long, consistent series of spatial inequality for Iran, or compared it
directly with the path of interpersonal inequality. The closest precedents are Rey (2018) for the US and
Capello & Cerisola (2024) for Europe. Neither covers a centralized, oil-dependent economy under heavy
external shocks. This project builds that series, with NTL filling the gaps in official provincial GDP.

## 4. Data

| Variable | Definition | Unit | Source |
|---|---|---|---|
| Total annual radiance | Sum of nighttime radiance within the province | nW/cm²/sr | VIIRS / DMSP |
| NTL per capita | Total radiance / population | nW per capita | Author's calculation |
| Provincial GDP | Constant 2021 (1400) prices | billion rials | Statistical Centre of Iran |
| GDP per capita | Provincial GDP / population | million rials | Author's calculation |
| National Gini | Household-weighted Gini | index | Statistical Centre of Iran |
| Population | Census and intercensal estimates | persons | Statistical Centre of Iran |

The panel covers 31 provinces (current administrative boundaries). It has 403 province-years for NTL
(2012–2024) and 310–341 for provincial GDP. The main period uses VIIRS (2012–2024). Extending it to 1992
with harmonized DMSP data is planned. All boundaries are kept fixed to the current provinces, so province splits over
time do not create artificial breaks.

## 5. Preliminary findings

- **National level.** Quarterly GDP has an elasticity of **0.239** with respect to total radiance
  (p < 0.01, R² = 0.544, 51 quarters). For non-oil GDP the elasticity is **0.246**, so NTL reflects
  general economic activity and not just oil-related lighting.
- **Provincial level.** In a pooled regression of total levels, the elasticity of GDP with respect to NTL
  is **0.996** (SE 0.040, R² = 0.674, 310 observations), close to proportional (per capita: 0.637). With
  province and year fixed effects it falls to **0.361** (SE 0.138), and to 0.227 (not significant) without
  the four gas-flare provinces, so the within-province signal is weaker.
- **Growth.** Annual growth in NTL per capita predicts growth in GDP per capita (slope 0.356, SE 0.144),
  but explains only part of the cross-provincial variation (R² = 0.175).
- **Ranks.** The Spearman correlation between provincial ranks by GDP per capita and by NTL per capita
  is 0.52–0.67 across years. The deviations follow a pattern: dense provinces (Tehran, Alborz, Gilan) look
  dimmer per capita than their output suggests, and sparse provinces (Sistan and Baluchestan,
  South Khorasan) look brighter. This supports including province fixed effects in the prediction model.

## 6. Methodology

1. **Building the panel.** Extract provincial NTL with Google Earth Engine, harmonize DMSP and VIIRS,
   and merge with provincial accounts and population.
2. **Predicting provincial GDP**, following Lessmann & Seidel (2017):
   $\ln(GDP_{it}) = \alpha + \beta\ln(NTL_{it}) + \mu_i + \gamma t + \varepsilon_{it}$, estimated on
   province-years with both GDP and NTL and used to predict the missing years. As an alternative series,
   official and NTL-based estimates are combined with optimal weights (Henderson et al., 2012).
3. **Inequality indices.** Population-weighted Gini, Theil (which splits into between- and
   within-province parts) and generalized entropy with a negative parameter. Unweighted versions are
   reported as a robustness check.
4. **Comparing the two dimensions.** Correlations in levels and first differences, turning points, and
   lead–lag co-movement with the national Gini. Generalized Dickey–Fuller tests are reported as extra
   evidence.

## 7. Robustness and limitations

**Robustness checks:** comparing results across inequality indices; backcasting tests (estimate on
2017–2021, predict 2012–2016); comparing the two GDP series; dropping structurally unusual provinces;
and weighted vs. unweighted indices.

**Limitations:**

- The analysis is descriptive and not causal.
- The annual series has a limited number of observations.
- Province-level aggregation hides inequality within provinces.
- Findings may not carry over to economies with a different structure.
- Harmonizing DMSP and VIIRS is difficult. If it fails, the core analysis can be limited to the VIIRS
  period.

## 8. Policy relevance

Separating the two dimensions makes it possible to assess policies whose effects differ by dimension:

- **The 2010 subsidy reform (cash transfers).** It should lower interpersonal inequality but may leave
  the spatial distribution of production unchanged.
- **Sanctions.** They hit border-trade, customs-dependent and export-oriented industrial provinces
  harder than others.
- **Place-based development budgets.** Their effect should appear in spatial inequality even if the
  national Gini does not change.

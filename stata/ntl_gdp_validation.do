* Run this do-file with the repository root as the working directory.
global ROOT "`c(pwd)'"

*************************************************
**** GDP regression on NTL  ****
*************************************************

********* Province level **********

clear 
set more off

* cd
cd "$ROOT/data/Validation"

* Import provincial validation dataset
use "province_ntl_gdp_validation_clean.dta", clear


* Check data
describe
summarize

* regression 
asdoc reg log_GDP_per_Capita log_NTL_Per_Capita, replace ///
save(province_validation.doc) ///
title(Provincial Validation: GDP per Capita on NTL per Capita)

********* National level **********
clear
set more off

* cd
cd "$ROOT/data/Validation"

* Import provincial validation dataset
use "national_ntl_gdp_validation_clean.dta", clear

* Check data
describe
summarize

* regression 
asdoc reg log_GDP_total_bilRial log_Sum_Radiance_sum, replace ///
save(national_validation.doc) ///
title(National Validation: Total GDP on Nighttime Light)

asdoc reg log_GDP_non_oil_bilRial log_Sum_Radiance_sum, append ///
save(national_validation.doc) ///
title(National Validation: Non-Oil GDP on Nighttime Light)

*************************************************
**** Residual regression  ****
*************************************************

* ========================
* Setup
* ========================
clear
set more off

cd "$ROOT/data/Validation"

use "hies_ntl_gdp_master.dta", clear

* ========================
* Prep: encode province as numeric, create log(Population)
* ========================
encode Province_EN, gen(province_id)

gen log_population = log(Population)

* ========================
* Regression 1: NTL on population, province FE (absorb), year FE (dummies)
* ========================
areg log_Annual_Sum log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_ntl, residuals

* Regression 2: Expenditure on population, province FE, year FE

areg log_real_exp_per_capita log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_exp, residuals


* Regression 3: GDP on population, province FE, year FE

areg log_GDP log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_gdp, residuals

* Correlation of residuals

pwcorr resid_ntl resid_exp, sig
pwcorr resid_ntl resid_gdp, sig

* Export regression table with asdoc

asdoc areg log_Annual_Sum log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results.doc) replace title(NTL on Population, Province and Year FE)

asdoc areg log_real_exp_per_capita log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results.doc) append title(Expenditure on Population, Province and Year FE)

asdoc areg log_GDP log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results.doc) append title(GDP on Population, Province and Year FE)
	
asdoc pwcorr resid_ntl resid_exp resid_gdp, sig ///
    save(regression_results.doc) append ///
    title(Correlation of Residuals: NTL, Expenditure, and GDP after controlling for Population and FE)

	

****************************************************************
* ****Robustness check: exclude flare-affected provinces ****
****************************************************************

* Flare-affected provinces: Bushehr, Khuzestan, Kohgiluyeh & Boyerahmad, Ilam
gen flare_province = inlist(Province_EN, "Bushehr", "Khuzestan", "Kohgiluyeh & Boyerahmad")

preserve
drop if flare_province == 1

* Regression 1: NTL on population, province FE, year FE
areg log_Annual_Sum log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_ntl_nf, residuals

* Regression 2: Expenditure on population, province FE, year FE
areg log_real_exp_per_capita log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_exp_nf, residuals

* Regression 3: GDP on population, province FE, year FE
areg log_GDP log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_gdp_nf, residuals

* Correlation of residuals, excluding flare provinces
pwcorr resid_ntl_nf resid_exp_nf resid_gdp_nf, sig

* Export
asdoc areg log_Annual_Sum log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results_noflare.doc) replace title(NTL on Population, excl. flare provinces)

asdoc areg log_real_exp_per_capita log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results_noflare.doc) append title(Expenditure on Population, excl. flare provinces)

asdoc areg log_GDP log_population i.Year, absorb(province_id) vce(cluster province_id) ///
    save(regression_results_noflare.doc) append title(GDP on Population, excl. flare provinces)

asdoc pwcorr resid_ntl_nf resid_exp_nf resid_gdp_nf, sig ///
    save(regression_results_noflare.doc) append title(Correlation of Residuals, excl. flare provinces)

restore

use "hies_ntl_gdp_master.dta", clear

**********************************************************************
**** Per-province trend: slope of expenditure & NTL over Year ****
**********************************************************************
statsby b_exp=_b[Year] se_exp=_se[Year] p_exp=_b[Year]/_se[Year], ///
    by(Province_EN) saving(trend_exp, replace): regress log_real_exp_per_capita Year

statsby b_ntl=_b[Year] se_ntl=_se[Year] p_ntl=_b[Year]/_se[Year], ///
    by(Province_EN) saving(trend_ntl, replace): regress log_NTL_Per_Capita Year

* Per-province correlation: NTL vs expenditure, within-province across years

statsby corr=r(rho) N=r(N), ///
    by(Province_EN) saving(province_corr, replace): correlate NTL_Per_Capita real_exp_per_capita

* Merge all three results together

use trend_exp, clear
merge 1:1 Province_EN using trend_ntl, nogenerate
merge 1:1 Province_EN using province_corr, nogenerate

gsort b_exp
list Province_EN b_exp b_ntl corr

* Export to Word with asdoc

asdoc list Province_EN b_exp b_ntl corr, ///
    save(province_trend_correlation.doc) replace ///
    title(Per-Province Trend in NTL and Expenditure, and Within-Province Correlation) ///
    dec(4)

	
use "hies_ntl_gdp_master.dta", clear

encode Province_EN, gen(province_id)
gen log_population = log(Population)

* Regenerate residuals
areg log_Annual_Sum log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_ntl, residuals

areg log_real_exp_per_capita log_population i.Year, absorb(province_id) vce(cluster province_id)
predict resid_exp, residuals

* Now the correlation by province will work
statsby corr_resid=r(rho) N=r(N), ///
    by(Province_EN) saving(province_corr_resid, replace): correlate resid_ntl resid_exp
	
use province_corr_resid, clear
list Province_EN corr_resid N


* ============================================================
**** GDP on NTL with fixed effects ****
* ============================================================

use "hies_ntl_gdp_master.dta", clear

encode Province_EN, gen(province_id)


areg log_GDP_per_Capita log_NTL_Per_Capita i.Year, absorb(province_id) vce(cluster province_id)

* Export
asdoc areg log_GDP_per_Capita log_NTL_Per_Capita i.Year, absorb(province_id) vce(cluster province_id) ///
    save(gdp_ntl_FE_validation.doc) replace title(Provincial Validation: GDP per Capita on NTL per Capita, Province and Year FE)
	
* ============================================================
* Robustness: GDP on NTL with FE, excluding flare provinces
* ============================================================

* IMPORTANT: make sure province names exactly match the dataset
tab Province_EN

gen flare_province = inlist(Province_EN, ///
    "Bushehr", ///
    "Khuzestan", ///
    "Kohgiluyeh & Boyerahmad")

preserve

drop if flare_province == 1

* Check remaining sample
tab Province_EN
count

* Simple correlation after excluding flare provinces
pwcorr log_GDP_per_Capita log_NTL_Per_Capita, sig obs

* Main FE validation regression
areg log_GDP_per_Capita log_NTL_Per_Capita i.Year, ///
    absorb(province_id) vce(cluster province_id)

* Export robustness regression
asdoc areg log_GDP_per_Capita log_NTL_Per_Capita i.Year, ///
    absorb(province_id) vce(cluster province_id) ///
    save(gdp_ntl_FE_validation.doc) append ///
    title(Provincial Validation: GDP per Capita on NTL per Capita, Excluding Flare Provinces)

restore

* ============================================================
**** ADDITIONAL CHECK: Total GDP on Total NTL with FE ****
* ============================================================

use "hies_ntl_gdp_master.dta", clear

encode Province_EN, gen(province_id)

* Main additional regression: total GDP on total NTL
areg log_GDP log_Annual_Sum i.Year, ///
    absorb(province_id) vce(cluster province_id)

* Export
asdoc areg log_GDP log_Annual_Sum i.Year, ///
    absorb(province_id) vce(cluster province_id) ///
    save(gdp_ntl_total_FE_validation.doc) replace ///
    title(Provincial Validation: Total GDP on Total NTL, Province and Year FE)


* ============================================================
**** Additional robustness: control for population ****
* ============================================================

capture drop log_population
gen log_population = log(Population)

areg log_GDP log_Annual_Sum log_population i.Year, ///
    absorb(province_id) vce(cluster province_id)

asdoc areg log_GDP log_Annual_Sum log_population i.Year, ///
    absorb(province_id) vce(cluster province_id) ///
    save(gdp_ntl_total_FE_validation.doc) append ///
    title(Total GDP on Total NTL, controlling for Population, Province and Year FE)
	
* ============================================================
**** ADDITIONAL CHECK: Total GDP on Total NTL - Pooled OLS ****
* ============================================================

use "hies_ntl_gdp_master.dta", clear

* Simple pooled regression: total GDP on total NTL
reg log_GDP log_Annual_Sum

* Export
asdoc reg log_GDP log_Annual_Sum, ///
    save(gdp_ntl_total_pooled_validation.doc) replace ///
    title(Provincial Validation: Total GDP on Total NTL - Pooled OLS)

* ============================================================
**** Scatter: Total Provincial GDP vs Total NTL ****
* ============================================================

* ============================================================
**** Scatter: Total Provincial GDP vs Total NTL ****
* ============================================================

use "hies_ntl_gdp_master.dta", clear

quietly correlate log_GDP log_Annual_Sum
local r = string(r(rho), "%4.3f")

* Get axis bounds for text placement
quietly summarize log_Annual_Sum
local xpos = r(min) + 0.05 * (r(max) - r(min))

quietly summarize log_GDP
local ypos = r(max) - 0.05 * (r(max) - r(min))

twoway ///
    (scatter log_GDP log_Annual_Sum, ///
        mcolor(navy%60) msize(small) msymbol(circle)) ///
    (lfit log_GDP log_Annual_Sum, ///
        lcolor(red) lwidth(medium)), ///
    title("Provincial Validation: GDP vs NTL (Total)", size(medium)) ///
    xtitle("log(Annual Sum of Radiance)", size(small)) ///
    ytitle("log(Total GDP - billion Rial)", size(small)) ///
    legend(off) ///
    text(`ypos' `xpos' "Pearson r = `r'", ///
        placement(e) size(small) color(navy)) ///
    note("Pooled province-year observations; 31 provinces, 1391-1400", size(vsmall)) ///
    graphregion(color(white)) bgcolor(white)

graph export "Scatter plot province NTL vs GDP.png", replace width(1200)




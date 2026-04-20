# US Homelessness & Housing Master Dataset — Feature Metadata

**File generated:** /mnt/data/feature_metadata.md

**Source dataset:** Final_National_Dataset.csv


## Overview

This document summarizes the column groups and feature-level descriptions for the `Final_National_Dataset.csv` (2007–2023). The dataset aggregates HUD Point-in-Time (PIT) counts at the Continuum of Care (CoC) level and joins ACS 5-Year estimates and associated margins of error (MOE) from the U.S. Census Bureau.

Use this metadata to understand variable groups, expected content, and MOE handling when building analysis or models.


## High-level groups and short descriptions

### Identifiers & Geography

CoC identifiers and geographic metadata: CoC name/id, state, county, FIPS or GEOID, and any crosswalk fields mapping CoCs to counties or places.

**Columns included (excerpt):**

- `CoC_Code`
- `CoC_Name`
- `State`


### Homelessness (HUD PIT/HIC)

HUD PIT/HIC counts — total homeless, sheltered, unsheltered counts, and related shelter inventory counts.

**Columns included (excerpt):**

- `Homeless_Count`
- `Sheltered_Count`
- `Unsheltered_Count`


### Economics (Census ACS)

Economic indicators from ACS: poverty counts and rates, unemployment rate, median household income, and other labor/income variables.

**Columns included (excerpt):**

- `Poverty_Count`
- `Unemployed_Count`
- `Poverty_Count_MOE`
- `Unemployed_Count_MOE`
- `Poverty_Rate`
- `Unemployment_Rate`


### Housing (Census ACS)

Housing stock and vacancy statistics: total housing units, vacant units, vacancy rates, ownership/rental splits, and housing unit characteristics.

**Columns included (excerpt):**

- `Vacant_Units`
- `Total_Housing_Units`
- `Vacant_Units_MOE`
- `Total_Housing_Units_MOE`
- `Vacancy_Rate`


### Rent Burden

Rent burden measures indicating share of households paying >=30%, 35%, 40%, and 50%+ of income on rent.

**Columns included (excerpt):**

- `Rent_Burden_30_35`
- `Rent_Burden_35_40`
- `Rent_Burden_40_50`
- `Rent_Burden_50_Plus`
- `Rent_Burden_30_35_MOE`
- `Rent_Burden_35_40_MOE`
- `Rent_Burden_40_50_MOE`
- `Rent_Burden_50_Plus_MOE`
- `Rent_Burden_Rate`


### Demographics

Population totals and breakdowns by race/ethnicity, age groups, veteran status, and other demographic variables.

_No columns detected matching this group by heuristic._

### Margins of Error (MOE)

ACS-provided margins of error for estimates. Aggregation MOEs were calculated using the root-sum-squared method when combining geographies.

**Columns included (excerpt):**

- `Total_Pop_MOE`


### Temporal

Year and survey period fields (PIT year, ACS 5-year period identifier).

**Columns included (excerpt):**

- `Year`


### Other / Metadata

Administrative or derived fields: rates calculated in-house (e.g., homeless rate per 10k), flags, notes, and any source/version fields.

**Columns included (excerpt):**

- `Area_Name`
- `Total_Pop`


## Technical notes

- **MOE handling**: All ACS MOEs in the dataset retain their original values. For aggregated fields the dataset uses the root-sum-square method to compute MOEs (as documented in the dataset description).

- **Missing / error codes**: Census error codes (-999, -666, etc.) were cleaned and converted to NA/null in numeric columns.

- **Units**: Counts are raw counts unless suffixed (`_rate`, `_pct`) which indicate percentages. Some rates are expressed as proportions (0-1) while others are percentage points (0-100); check the column name suffix for clarity.

- **License**: CC0 (public domain). Source data: HUD PIT/HIC and ACS 5-year estimates.


## Example rows (first 5 rows)

| CoC_Code   | CoC_Name                                             |   Homeless_Count |   Sheltered_Count |   Unsheltered_Count |   Year | State   | Area_Name                                        |   Total_Pop |   Poverty_Count |   Unemployed_Count |   Vacant_Units |   Total_Housing_Units |   Rent_Burden_30_35 |   Rent_Burden_35_40 |   Rent_Burden_40_50 |   Rent_Burden_50_Plus |   Total_Pop_MOE |   Poverty_Count_MOE |   Unemployed_Count_MOE |   Vacant_Units_MOE |   Total_Housing_Units_MOE |   Rent_Burden_30_35_MOE |   Rent_Burden_35_40_MOE |   Rent_Burden_40_50_MOE |   Rent_Burden_50_Plus_MOE |   Poverty_Rate |   Unemployment_Rate |   Vacancy_Rate |   Rent_Burden_Rate |
|:-----------|:-----------------------------------------------------|-----------------:|------------------:|--------------------:|-------:|:--------|:-------------------------------------------------|------------:|----------------:|-------------------:|---------------:|----------------------:|--------------------:|--------------------:|--------------------:|----------------------:|----------------:|--------------------:|-----------------------:|-------------------:|--------------------------:|------------------------:|------------------------:|------------------------:|--------------------------:|---------------:|--------------------:|---------------:|-------------------:|
| AK-500     | Anchorage CoC                                        |             1494 |              1369 |                 125 |   2022 | AK      | Anchorage                                        |      290674 |           27415 |               7747 |          11804 |                118938 |                3792 |                2529 |                3508 |                  7685 |           0     |             2611    |                732     |            876     |                   166     |                 461     |                 530     |                 519     |                   752     |      0.0943153 |           0.0266519 |       0.099245 |          0.0602531 |
| AK-501     | Alaska Balance of State CoC                          |              826 |               594 |                 232 |   2022 | AK      | Alaska Balance of State                          |      434533 |           47184 |              14878 |          47529 |                200926 |                3651 |                2734 |                4080 |                  8135 |         200.185 |             1803.08 |                849.662 |            980.498 |                   836.246 |                 452.83  |                 363.302 |                 486.37  |                   661.561 |      0.108586  |           0.0342391 |       0.23655  |          0.0428046 |
| AL-500     | Birmingham/Jefferson, St. Clair, Shelby Counties CoC |              943 |               601 |                 342 |   2022 | AL      | Birmingham/Jefferson, St. Clair, Shelby Counties |      987900 |          128760 |              23268 |          52765 |                436173 |               10250 |                7025 |                9398 |                 28030 |           0     |             5134.68 |               1570.56  |           1847.52  |                   192.72  |                 976.407 |                 727.408 |                 966.005 |                  1426.06  |      0.130337  |           0.023553  |       0.120973 |          0.055373  |
| AL-501     | Mobile City & County/Baldwin County CoC              |              585 |               388 |                 197 |   2022 | AL      | Mobile City & County/Baldwin County              |      647298 |           94798 |              14868 |          59551 |                309958 |                6794 |                4499 |                6465 |                 18757 |           0     |             4184.97 |               1068.53  |           1774.92  |                   141.4   |                 908.24  |                 742.082 |                 872.708 |                  1250.91  |      0.146452  |           0.0229693 |       0.192126 |          0.0564114 |
| AL-502     | Florence/Northwest Alabama CoC                       |              232 |               198 |                  34 |   2022 | AL      | Florence/Northwest Alabama                       |      269584 |           40538 |               4746 |          23166 |                128858 |                2428 |                1213 |                2051 |                  4253 |           0     |             2258.06 |                573.718 |           1087.42  |                   104.499 |                 489.277 |                 277.245 |                 388.308 |                   555.018 |      0.150372  |           0.0176049 |       0.179779 |          0.0368902 |


## Full column list

- `CoC_Code`
- `CoC_Name`
- `Homeless_Count`
- `Sheltered_Count`
- `Unsheltered_Count`
- `Year`
- `State`
- `Area_Name`
- `Total_Pop`
- `Poverty_Count`
- `Unemployed_Count`
- `Vacant_Units`
- `Total_Housing_Units`
- `Rent_Burden_30_35`
- `Rent_Burden_35_40`
- `Rent_Burden_40_50`
- `Rent_Burden_50_Plus`
- `Total_Pop_MOE`
- `Poverty_Count_MOE`
- `Unemployed_Count_MOE`
- `Vacant_Units_MOE`
- `Total_Housing_Units_MOE`
- `Rent_Burden_30_35_MOE`
- `Rent_Burden_35_40_MOE`
- `Rent_Burden_40_50_MOE`
- `Rent_Burden_50_Plus_MOE`
- `Poverty_Rate`
- `Unemployment_Rate`
- `Vacancy_Rate`
- `Rent_Burden_Rate`


---
Generated programmatically to assist exploratory analysis and modeling.

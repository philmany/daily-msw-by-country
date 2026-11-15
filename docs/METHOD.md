# Daily municipal solid waste (MSW) by country: method and log

**Built:** 14 Nov 2026 | **Scope:** 195 UN member states + observers (Holy See, Palestine)

## Source
World Bank, *What a Waste 3.0* country dataset (last updated 11 Mar 2026), CC BY 4.0.
File: What_a_Waste_3.0_COUNTRY_Dataset_&_Codebook.xlsx, sheet "Country dataset".
Country list: ISO 3166 independent states (datasets/country-codes), with Taiwan removed and Palestine added.

## Rules
1. Cutoff: data year must be 2022 or later (nothing older than 4 years).
2. If the country has a reported national MSW total with year >= 2022 -> use it (data_basis = reported).
3. Otherwise, if the World Bank's harmonised 2022 baseline exists -> use it (data_basis = modelled). The note column says whether an older reported figure was set aside.
4. Otherwise exclude and log (exclusion_log.csv).
5. tonnes_per_day = annual_tonnes / 365 (no leap-year adjustment).
6. kg_per_person_per_day is recomputed from the matching population year and is a sanity check only.
7. flag marks implausible kg/person/day (>2.5 or <0.05). Flagged rows are kept. They are tourism-heavy economies or Monaco, where visitors inflate per-resident figures.

## Caveats
- "MSW" definitions differ between countries (what counts as municipal, whether commercial waste is included). See point_of_measurement.
- Modelled values are World Bank estimates, not national statistics. Filter data_basis == reported for observed values only.
- Reported years run 2022-2024; the dataset is not a single-year snapshot.

# Daily municipal solid waste by country

Tonnes of municipal solid waste (MSW) produced per day, for every UN member state and observer with usable data from **2022 or later**. Built for the "Art out of Data" project.

- `data/daily_msw_tonnes_by_country.csv` - 193 countries: annual tonnes, tonnes/day (annual / 365), kg/person/day, data year, basis (reported or modelled), flags
- `data/exclusion_log.csv` - countries left out and why (North Korea, Vatican City: absent from the source)
- `docs/METHOD.md` - rules, caveats
- `scripts/build_dataset.py` - rebuilds both CSVs from the source workbook

## Rebuild
1. Download the "Country Level Data & Codebook" xlsx from the [World Bank data catalog](https://datacatalog.worldbank.org/search/dataset/0039597/what-a-waste-global-database) into `input/`.
2. Download [country-codes.csv](https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv) into `input/`.
3. `pip install pandas openpyxl` then `python scripts/build_dataset.py input data`

## Source and licence
World Bank, *What a Waste 3.0* (updated 11 Mar 2026), CC BY 4.0. Country list: datasets/country-codes. Derived data here is shared under CC BY 4.0 with attribution to the World Bank.

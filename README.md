# Income and Crime Rate Association with Housing Prices Across California Counties

This project combines three county level datasets for California:

- Zillow housing values
- ACS median household income
- California violent crime rates

The goal is to compare housing values with income and crime rates across California counties.

## How to Install the Requirements for the Project

From the project folder, installing the required packages:
```bash
pip install -r requirements.txt
```

In case of using `python3` and `pip3`:

```bash
pip3 install -r requirements.txt
```
## How to Run the Code

By running the files in this order:
```bash
python src/get_data.py
python src/clean_data.py
python src/integrate_data.py
python src/analyze_visualize.py
```

If `python` does not work, use `python3` instead of `python`.
## 1. How to Get the Data

By running:

```bash
python src/get_data.py
```

This downloads the raw data and saves it in this folder:

```text
data/raw/
```

Expected raw files:

```text
data/raw/zillow_county_zhvi_raw.csv
data/raw/zillow_full_download.csv
data/raw/acs_income_raw.json
data/raw/acs_income_raw.csv
data/raw/ca_violent_crime_raw.csv
```

### Data Sources

- Zillow county level ZHVI housing data
- ACS median household income data from the Census API
- California violent crime rate data

### ACS API Key

The ACS Census API key is not included in the code for privacy. In case of having a key, we should set it in Terminal before running the project:

```bash
export ACS_API_KEY="API_KEY_HERE"
```

A valid ACS Census API key is required before running the data download script.

## Zillow Scraper

The Zillow scraper can also be run by itself.

This command prints the full scraped Zillow dataset:

```bash
python src/scraper.py
```

This one prints only the first 10 rows:

```bash
python src/scraper.py --scrape 10
```

We can also save the scraped Zillow data to a CSV file:

```bash
python src/scraper.py --save src/my_scraped_data.csv
```

The scraper extracts California county housing values, and keeps these columns:

```text
county_name
state
zhvi
```

## 2. Clean the Data

Run:

```bash
python src/clean_data.py
```

This reads the raw files from `data/raw/`, cleans them, and saves the cleaned files in `data/processed/`.

The cleaning steps include:

- standardizing county names
- removing extra spaces
- removing `County` from county names
- keeping California county rows
- selecting the needed columns
- converting numeric columns
- keeping the latest crime year for each county

The expected cleaned files would be:

```text
data/processed/zillow_clean.csv
data/processed/acs_income_clean.csv
data/processed/crime_clean.csv
```

## 3. Integrate the Data

For running, we can simply use thid command:

```bash
python src/integrate_data.py
```

This combines the cleaned Zillow, ACS income, and crime datasets into one file using:

```text
county_name
```

The integrated dataset is saved as:

```text
data/processed/integrated_county_data.csv
```

Main columns in the final dataset:

```text
county_name
zhvi
median_income
violent_crime_rate
reportyear
```

## 4. Analysis and Visualization of Data

Running:

```bash
python src/analyze_visualize.py
```

This script reads the integrated dataset and creates summary outputs and charts.

The analysis includes:

- descriptive statistics
- top counties by housing value
- top counties by violent crime rate
- correlation between housing value, income, and crime
- scatter plots comparing income, crime, and housing value

Expected result files:

```text
results/correlation_heatmap.png
results/top_10_housing_counties.png
results/top_10_crime_counties.png
results/income_vs_housing.png
results/crime_vs_housing.png
```

## Notes

The project should be run from the main `project` folder. The scripts expect the `data/` and `results/` folders to stay in the same structure.

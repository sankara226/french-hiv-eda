# French HIV/AIDS Diagnostic Registry - Exploratory Data Analysis (EDA)

A structured, modular data engineering and exploratory profiling pipeline assessing HIV/AIDS diagnosis registries in France.

## Pipeline Structural Features

- **Robust Ingestion Engine**: Automated data parsing, programmatic column isolation, and strict dtype enforcement.
- **Mathematical Bound Assertions**: Automated data validation verifying inequality bounds ($Lower < Value < Upper$).
- **Statistical Stratification**: Automated variable cross-tabulation grouped by demographic categoricals.

## Execution Details

1. Place the historical data tracking CSV file into the `data/` subdirectory.
2. Install project dependencies: `pip install -r requirements.txt`
3. Execute the workflow runner: `python main.py`

French HIV/AIDS Diagnostic Registry - Exploratory Data Analysis (EDA)
A structured, modular data engineering and exploratory profiling pipeline assessing HIV/AIDS diagnosis registries in France.

Pipeline Structural Features
Robust Ingestion Engine: Automated data parsing, programmatic column isolation, and strict dtype enforcement.
Mathematical Bound Assertions: Automated data validation verifying inequality bounds ($Lower < Value < Upper$).
Statistical Stratification: Automated variable cross-tabulation grouped by demographic categoricals.
Execution Details
Place the historical data tracking CSV file into the data/ subdirectory.
Install project dependencies: 
pip install -r requirements.txt
Execute the workflow runner: 
python main.py

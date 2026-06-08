import pandas as pd

def perform_univariate_analysis(df: pd.DataFrame):
    """Extracts trend boundaries and temporal continuity across variables."""
    print("\n--- TIME TREND RANGE AUDIT ---")
    min_year, max_year = df["Year"].min(), df["Year"].max()
    print(f"Registry Timeline Span: {min_year} -> {max_year}")
    
    expected_timeline = set(range(min_year, max_year + 1))
    actual_timeline = set(df["Year"])
    omitted_years = expected_timeline - actual_timeline
    
    if not omitted_years:
        print("Timeline Continuity Check: Complete. No intervals omitted.")
    else:
        print(f"Alert: Temporal tracking gaps detected: {sorted(omitted_years)}")

    print("\n--- LOGISTIC DISTRIBUTION METRICS ---")
    print(df['Diagnosis Number'].describe())
    
    peak_record = df.loc[df['Diagnosis Number'].idxmax()]
    nadir_record = df.loc[df['Diagnosis Number'].idxmin()]
    
    print(f"\nHistorical Peak Cases:\nYear: {peak_record['Year']} | Group: {peak_record['Sex']} | Count: {peak_record['Diagnosis Number']}")
    print(f"Historical Nadir Cases:\nYear: {nadir_record['Year']} | Group: {nadir_record['Sex']} | Count: {nadir_record['Diagnosis Number']}")

def perform_stratified_analysis(df: pd.DataFrame):
    """Calculates granular aggregations and advanced epidemiological metrics."""
    print("\n--- CATEGORICAL DEMOGRAPHIC PROFILE COUNT ---")
    print(df['Sex'].value_counts(normalize=True))
    
    print("\n--- STRATIFIED DIAGNOSIS AGGREGATIONS ---")
    print(df.groupby('Sex')[['Diagnosis Number', 'Lower Bound', 'Upper Bound']].mean())

    # NEW ADVANCED METRICS
    print("\n--- ADVANCED EPIDEMIOLOGICAL METRICS ---")
    
    # 1. Year-over-Year Velocity Analysis
    print("\n[Velocity] Year-over-Year Net Shift in Diagnoses (by Sex):")
    sorted_df = df.sort_values(['Sex', 'Year']).copy()
    sorted_df['YoY_Change'] = sorted_df.groupby('Sex')['Diagnosis Number'].diff()
    print(sorted_df.dropna(subset=['YoY_Change'])[['Year', 'Sex', 'Diagnosis Number', 'YoY_Change']].tail(6))
    
    # 2. Risk Ratio Proxy (Male vs Female Mean Disparity)
    means = df.groupby('Sex')['Diagnosis Number'].mean()
    if 'Male' in means.index and 'Female' in means.index:
        risk_ratio_proxy = means['Male'] / means['Female']
        print(f"\n[Demographic Disparity] Male-to-Female Average Diagnosis Ratio: {risk_ratio_proxy:.2f}x")
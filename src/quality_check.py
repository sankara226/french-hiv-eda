import pandas as pd

def verify_data_integrity(df: pd.DataFrame) -> dict:
    """Executes code quality, emptiness evaluation and record duplication passes."""
    null_counts = df.isna().sum().to_dict()
    duplicate_records = int(df.duplicated().sum())
    
    print("\n--- SYSTEM QUALITY MATRIX VERIFICATION ---")
    print(f"Null Assertions Counter   : {null_counts}")
    print(f"Duplicated Row Detections : {duplicate_records}")
    
    # Analyze domain space ranges
    print("\nUnique Domain Values Evaluation:")
    for col in df.columns:
        print(f" - Element '{col}': {df[col].unique()}")
        
    return {"nulls": null_counts, "duplicates": duplicate_records}

def run_boundary_coherency_checks(df: pd.DataFrame):
    """Validates structural mathematical boundaries across confidence matrix calculations."""
    print("\n--- BOUNDARY COHERENCY ASSESSMENT ---")
    
    # Verification checks
    lower_vs_diagnosis = (df['Lower Bound'] <= df['Diagnosis Number']).all()
    lower_vs_upper = (df['Lower Bound'] <= df['Upper Bound']).all()
    upper_vs_diagnosis = (df['Upper Bound'] >= df['Diagnosis Number']).all()
    
    print(f"Assertion Pass: [Lower Bound <= Diagnosis Number] -> {lower_vs_diagnosis}")
    print(f"Assertion Pass: [Lower Bound <= Upper Bound]      -> {lower_vs_upper}")
    print(f"Assertion Pass: [Upper Bound >= Diagnosis Number] -> {upper_vs_diagnosis}")
    
    # Evaluate distribution interval widths
    interval_widths = df['Upper Bound'] - df['Lower Bound']
    print(f"Mean Confidence Interval Width   : {interval_widths.mean():.4f}")
    print(f"Standard Deviation Interval Width: {interval_widths.std():.4f}")

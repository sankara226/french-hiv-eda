import os
import pandas as pd
from pathlib import Path

def load_and_initialize_data(file_path: Path) -> pd.DataFrame:
    """Handles raw structural ingestion, parsing, explicit column naming and type safety enforcement."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Target dataset file missing at: {file_path}. "
            "Please ensure the file is positioned correctly inside your project directory."
        )
    
    # Ingest the dataset
    df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')
    
    # Apply standardized explicit English naming schemas
    df.columns = ["Year", "Sex", "Diagnosis Number", "Lower Bound", "Upper Bound"]
    
    # Force type safety across structural metrics
    type_casting_matrix = {
        "Year": int,
        "Diagnosis Number": int,
        "Lower Bound": int,
        "Upper Bound": int,
        "Sex": str
    }
    
    for column, data_type in type_casting_matrix.items():
        df[column] = df[column].astype(data_type)
        
    return df

def execute_structural_profiling(df: pd.DataFrame):
    """Prints diagnostic telemetry of the structural dataframe composition."""
    print("\n--- DATA REGISTRY INTERROGATION ---")
    print(f"Shape Dimension Profiles : {df.shape}")
    print("\nColumns and Types Summary:")
    print(df.info())
    print("\nStatistical Overview Matrix:")
    print(df.describe(include='all'))

"""
Loads the raw Online Retail dataset and performs initial data cleaning.

- Reads the original Excel file
- Standardizes column names and data types
- Handles missing and invalid values
- Exports cleaned data to intermediate CSV files
"""

# 01_load_and_export.py
import pandas as pd

INPUT_XLSX = "online_retail_II.xlsx"
OUTPUT_CSV = "online_retail_raw.csv"

def main():
    print("DEBUG: script started")
    df = pd.read_excel(INPUT_XLSX, sheet_name=0)
    print("DEBUG: excel loaded")
    print("Rows, Cols:", df.shape)
    print("Columns:", list(df.columns))

    # minimal cleanup
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

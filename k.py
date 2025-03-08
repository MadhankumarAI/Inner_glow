import pandas as pd
CSV_PATH = r"C:\Users\jaip7\Downloads\madhan\innergl\dataset\treatments.csv"
treatment_df = pd.read_csv(CSV_PATH)

print(treatment_df.head())  # Add this after reading the CSV

# this was for data preprocessing



import pandas as pd
CSV_PATH = r"your path"
treatment_df = pd.read_csv(CSV_PATH)

print(treatment_df.head())  # Add this after reading the CSV

# Import necessary libraries
from pathlib import Path
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("backend/mlops/data/processed/cleaned_accInfo.csv")
# Display basic information about the dataframe
print("DataFrame shape:", df.shape)
print("\
First few rows:")
print(df.head())

# Check column types
print("\
Column data types:")
print(df.dtypes)

# Check for NaN values
print("\
NaN values per column:")
print(df.isna().sum())

# Calculate percentage of NaN values per column
nan_percentage = df.isna().mean() * 100
print("\
Percentage of NaN values per column:")
print(nan_percentage)

plt.figure(figsize=(132, 7))  # Increase width significantly
sns.heatmap(df.isna(), cbar=False, yticklabels=False)
plt.xticks(rotation=90)  # Rotate column labels for better readability
plt.title('NaN Values Heatmap')
plt.tight_layout()
plt.show()


# Check which columns contain JSON data
json_columns = []
for col in df.columns:
    if df[col].dtype == 'object':
        # Check first non-null value
        first_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
        if first_val and isinstance(first_val, str):
            try:
                # Try to parse as JSON
                if first_val.startswith('{') or first_val.startswith('['):
                    json.loads(first_val)
                    json_columns.append(col)
            except Exception:
                pass

print("Columns containing JSON data:", json_columns)
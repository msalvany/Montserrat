import pandas as pd

# Load the CSV properly
df = pd.read_csv("data/agulles_full_data.csv")

# -----------------------------
# 4. Check for NaN values in the "Region" column
nan_regions = df[df["Region"].isna()]

# Print the rows with NaN values in the Region column
print("Rows with NaN in 'Region':")
print(nan_regions)

# Alternatively, count the NaN values
nan_count = df["Region"].isna().sum()
print(f"\nTotal NaN values in 'Region' column: {nan_count}")
import pandas as pd

# Load the CSV
df = pd.read_csv("data/agulles_full_data.csv")

df_deduped = df.drop_duplicates(subset="Name", keep="first")
df_deduped.to_csv("data/agulles_no_duplicates.csv", index=False)
print("✅ Saved deduplicated file.")
# Check for duplicates by Name
duplicates = df[df.duplicated(subset="Name", keep=False)].sort_values("Name")

if not duplicates.empty:
    print("❗ Found duplicated agulles by name:\n")
    print(duplicates[["Name", "Subregion", "Region", "Easting", "Northing"]])
    print(f"\n🔁 Total duplicates: {duplicates['Name'].nunique()} unique names")
else:
    print("✅ No duplicated agulles found.")
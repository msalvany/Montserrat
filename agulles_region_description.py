import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer

# -----------------------------
# 1. Load both datasets
# -----------------------------
df_coords = pd.read_csv("data/agulles_with_region.csv")
df_desc = pd.read_csv("data/agulles_full_data_from_description_pages.csv")

# -----------------------------
# 2. Merge by Name
# -----------------------------

# You can clean the “Name” column like this to ensure no leading or trailing spaces are present:
df_coords["Name"] = df_coords["Name"].str.strip()
df_desc["Name"] = df_desc["Name"].str.strip()

# Merging by name
df = pd.merge(df_coords, df_desc, on="Name", how="left")

# -----------------------------
# 3. Clean coordinates and convert to GeoDataFrame
# -----------------------------
df = df[pd.to_numeric(df["Easting"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["Northing"], errors="coerce").notnull()]
df["Easting"] = df["Easting"].astype(float)
df["Northing"] = df["Northing"].astype(float)

# inspect the rows that are excluded
invalid_coords = df[pd.to_numeric(df["Easting"], errors="coerce").isna() | pd.to_numeric(df["Northing"], errors="coerce").isna()]
print("Invalid Coordinates:")
print(invalid_coords)

# Convert UTM → Lat/Lon
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])])

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["Longitude"], df["Latitude"])],
    crs="EPSG:4326"
)

# -----------------------------
# 4. Find Matching & Non-Matching Agulles by Name
# -----------------------------

# Names only in df_coords
names_coords = set(df_coords["Name"])
names_desc = set(df_desc["Name"])

only_in_coords = names_coords - names_desc
only_in_desc = names_desc - names_coords
matched = names_coords & names_desc

print(f"✅ Matches: {len(matched)}")
print(f"❌ Only in coordinates file: {len(only_in_coords)}")
print(f"❌ Only in description file: {len(only_in_desc)}")

# Print the names that do not match
print("\n🔍 Agulles in coords but NOT in description:")
for name in sorted(only_in_coords):
    print("-", name)

print("\n🔍 Agulles in description but NOT in coords:")
for name in sorted(only_in_desc):
    print("-", name)



# -----------------------------
# 4. Check for NaN values in the "Region" column
nan_regions = df[df["Region"].isna()]
# -----------------------------
# Print the rows with NaN values in the Region column
print("Rows with NaN in 'Region':")
print(nan_regions)

# Alternatively, you can just count the NaN values
nan_count = df["Region"].isna().sum()
print(f"\nTotal NaN values in 'Region' column: {nan_count}")





# -----------------------------
# 4. Save as GeoJSON
# -----------------------------
gdf.to_file("data/agulles_with_region_description.geojson", driver="GeoJSON")
print("✅ GeoJSON saved to data/agulles_with_region_description.geojson")

# -----------------------------
# 5. Save as CSV (including Lat/Lon)
# -----------------------------
gdf.drop(columns="geometry").to_csv("data/agulles_with_region_description.csv", index=False)
print("📄 CSV saved to data/agulles_with_region_description.csv")
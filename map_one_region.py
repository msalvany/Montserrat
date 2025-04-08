import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
import os

from utils import plot_montserrat_map

# -----------------------------
# 1. Load and prepare data
# -----------------------------
print("📦 Loading agulles data...")
df = pd.read_csv("data/agulles_with_region.csv")

# Clean coordinates
df = df[pd.to_numeric(df["Easting"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["Northing"], errors="coerce").notnull()]
df["Easting"] = df["Easting"].astype(float)
df["Northing"] = df["Northing"].astype(float)

# Convert UTM to Lat/Lon
print("🔄 Converting UTM to Lat/Lon...")
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])])

# -----------------------------
# 2. Filter by region
# -----------------------------
target_region = "Ecos"
region_df = df[df["Region"] == target_region]

# 👇 Print number of agulles
print(f"📌 {len(region_df)} agulles found in region '{target_region}'")

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    region_df,
    geometry=gpd.points_from_xy(region_df.Longitude, region_df.Latitude),
    crs="EPSG:4326"
)

# -----------------------------
# 3. Plot and save
# -----------------------------
output_path = f"output/maps/{target_region.replace(' ', '_')}.png"
os.makedirs("output/maps", exist_ok=True)

print(f"🗺️ Plotting and saving map for {target_region}...")
plot_montserrat_map(gdf, region_name=target_region, sample_size=20, fast_mode=True, save_path=output_path)  # or 200, 50, etc.

print("✅ Done!")
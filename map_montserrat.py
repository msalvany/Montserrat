print("🔁 Starting conversion")

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
from pyproj import Transformer
import matplotlib.patheffects as pe

from utils import plot_montserrat_map


# -----------------------------
# 1. Load CSV, clen data and Convert UTM → Lat/Lon
# -----------------------------
print("📦 Loading CSV")

df = pd.read_csv("data/agulles_with_region.csv")

# Remove rows with missing or non-numeric coordinates
df = df[pd.to_numeric(df["Easting"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["Northing"], errors="coerce").notnull()]
df["Easting"] = df["Easting"].astype(float)
df["Northing"] = df["Northing"].astype(float)

# Convert UTM Zone 31T (EPSG:32631) to WGS84 (EPSG:4326)
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])])

# -----------------------------
# 2. Create GeoDataFrame
# -----------------------------
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
    crs="EPSG:4326"
)
gdf_web = gdf.to_crs(epsg=3857)

# -----------------------------
# 3. Plot the Map
# -----------------------------
print("📍 Plotting started")

plot_montserrat_map(gdf, fast_mode=True)  # or False for full beauty

print("✅ Done!")
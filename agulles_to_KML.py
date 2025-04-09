import pandas as pd
import simplekml
from shapely.geometry import Point
from pyproj import Transformer
from utils import get_kml_color

# -----------------------------
# 1. Load and Deduplicate
# -----------------------------
print("📦 Loading data...")
df = pd.read_csv("data/agulles_full_data.csv")

# Remove duplicates by name
duplicates = df[df.duplicated(subset="Name", keep=False)].sort_values("Name")
if not duplicates.empty:
    print(f"❗ Found {duplicates['Name'].nunique()} duplicated names. Deduplicating...")
    df = df.drop_duplicates(subset="Name", keep="first")

# -----------------------------
# 2. Fix Coordinate Errors (before any transformation)
# -----------------------------
print("🔧 Fixing known coordinate errors...")

df.loc[df["Name"] == "Veïna de baix de l'Arc de Guirló", ["Easting", "Northing"]] = [397991, 4606799]
df.loc[df["Name"] == "Les Tres Maries - cota 1", ["Easting", "Northing"]] = [398500, 4606200]
df.loc[df["Name"] == "El Braguer", ["Easting", "Northing"]] = [401120, 4606083]
df.loc[df["Name"] == "Roca de la Trumfa", ["Easting", "Northing"]] = [402588, 4605456]
df.loc[df["Name"].str.contains("Cap del Gat", case=False, na=False), ["Easting", "Northing"]] = [403887, 4605332]


# Ensure Easting and Northing are numeric
df["Easting"] = pd.to_numeric(df["Easting"], errors="coerce")
df["Northing"] = pd.to_numeric(df["Northing"], errors="coerce")

# Drop rows with invalid coordinates
df = df[df["Easting"].notna() & df["Northing"].notna()]

# -----------------------------
# 3. Convert to Latitude/Longitude
# -----------------------------
print("🌍 Converting UTM → Lat/Lon...")
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[
    transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])
])

# -----------------------------
# 4. Flag Suspicious Locations
# -----------------------------
invalid = df[
    (df["Latitude"] < 41) | (df["Latitude"] > 42) |
    (df["Longitude"] < 1.4) | (df["Longitude"] > 2.2)
]
if not invalid.empty:
    print(f"🚨 Found {len(invalid)} agulles with suspicious coordinates:")
    print(invalid[["Name", "Easting", "Northing", "Latitude", "Longitude"]])
else:
    print("✅ All agulles fall within expected Montserrat boundaries.")

# -----------------------------
# 5. Create KML File
# -----------------------------
print("🗂️ Creating KML...")
kml = simplekml.Kml()
folders = {}

for (region, subregion), group in df.groupby(["Region", "Subregion"]):
    if region not in folders:
        folders[region] = kml.newfolder(name=region)
    subfolder = folders[region].newfolder(name=subregion)

    for _, row in group.iterrows():
        pnt = subfolder.newpoint()
        pnt.name = ""  # Don't show label
        pnt.coords = [(row["Longitude"], row["Latitude"])]
        pnt.description = f"<b>{row['Name']} ({region} - {subregion})</b><br>{row.get('Description', '') or ''}"
        pnt.style.iconstyle.color = get_kml_color(region)
        pnt.style.iconstyle.scale = 1.3
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"

kml.save("output/montserrat_cleaned.kml")
print("✅ KML saved as output/montserrat_cleaned.kml")

# -----------------------------
# 6. Save Clean CSV
# -----------------------------
df.to_csv("data/agulles_full_data_cleaned.csv", index=False)
print("💾 Clean CSV saved as data/agulles_full_data_cleaned.csv")

# -----------------------------
# 7. Final Report
# -----------------------------
print("\n📊 Region/Subregion overview:")
print(df[["Region", "Subregion"]].drop_duplicates().sort_values(["Region", "Subregion"]))
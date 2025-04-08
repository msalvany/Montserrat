import pandas as pd
import simplekml
from shapely.geometry import Point
from pyproj import Transformer
from utils import get_kml_color

# Load your agulles data
df = pd.read_csv("data/agulles_full_data.csv")

# Clean missing coordinate values
df = df[df["Easting"].notna() & df["Northing"].notna()]
df["Easting"] = df["Easting"].astype(float)
df["Northing"] = df["Northing"].astype(float)

# Convert UTM → Lat/Lon
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])])

# Create KML
kml = simplekml.Kml()

# 🗂️ Build folder structure and store it in a dict
folders = {}

for (region, subregion), group in df.groupby(["Region", "Subregion"]):
    if region not in folders:
        folders[region] = kml.newfolder(name=region)
    subfolder = folders[region].newfolder(name=subregion)
    
    for _, row in group.iterrows():
        pnt = subfolder.newpoint()
        pnt.name = ""  # Don't show label
        pnt.coords = [(row["Longitude"], row["Latitude"])]
        pnt.description = f"<b>{row['Name']} ({row['Region']} - {row['Subregion']})</b><br>{row.get('Description', '')}"
        
        # Apply color
        color = get_kml_color(row.get("Region", ""))
        pnt.style.iconstyle.color = color
        pnt.style.iconstyle.scale = 1.3
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"

# Save the file
kml.save("output/montserrat_colored_final.kml")
print("✅ KML exported to output/montserrat_colored_final.kml")

print("🧠 Unique Region/Subregion combos:", df[["Region", "Subregion"]].drop_duplicates().shape[0])
print(df[["Region", "Subregion"]].drop_duplicates().sort_values(["Region", "Subregion"]))

print(df[df["Region"] == "Unknown"][["Name", "Subregion", "Region", "SourceURL"]])

from urllib.parse import urlparse

df["Slug"] = df["SourceURL"].apply(lambda url: urlparse(url).path.strip("/").split("/")[-1])
unknown_slugs = df[df["Region"] == "Unknown"]["Slug"].value_counts()
print("🔍 Slugs causing 'Unknown':")
print(unknown_slugs)
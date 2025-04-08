import pandas as pd
import simplekml
from shapely.geometry import Point
from pyproj import Transformer
from utils import get_kml_color

# Load your agulles with region + description
df = pd.read_csv("data/agulles_with_region_description.csv")

# Filter missing values
df = df[df["Easting"].notna() & df["Northing"].notna()]

# Convert UTM → Lat/Lon
transformer = Transformer.from_crs("epsg:32631", "epsg:4326", always_xy=True)
df["Longitude"], df["Latitude"] = zip(*[transformer.transform(e, n) for e, n in zip(df["Easting"], df["Northing"])])

# Create KML
kml = simplekml.Kml()

# Group by Region and Subregion
for (region, subregion), group in df.groupby(["Region", "Subregion"]):
    region_folder = kml.newfolder(name=region)
    subregion_folder = region_folder.newfolder(name=subregion)

for _, row in df.iterrows():
    pnt = kml.newpoint(name=row["Name"])
    pnt.coords = [(row["Longitude"], row["Latitude"])]
    pnt.name = ""  # No label visible on map
    pnt.description = f"<b>{row['Name']} ({region} - {subregion})</b><br>{row.get('Description', '')}"
    
    # Color by region
    region = row.get("Region", "")
    color = get_kml_color(region)
    
    pnt.style.iconstyle.color = color
    pnt.style.iconstyle.scale = 1.3
    pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"

# Save
kml.save("output/montserrat_colored_2.kml")
print("✅ KML exported to output/montserrat_colored_2.kml")
import zipfile
import os

# Paths
kml_path = "output/montserrat_cleaned.kml"
icon_path = "output/placemark_circle.png"  # path to your local icon
kmz_path = "output/montserrat_complete.kmz"

# Create KMZ
with zipfile.ZipFile(kmz_path, 'w') as kmz:
    kmz.write(kml_path, arcname=os.path.basename(kml_path))
    if os.path.exists(icon_path):
        kmz.write(icon_path, arcname=os.path.basename(icon_path))

print(f"✅ KMZ saved to {kmz_path}")
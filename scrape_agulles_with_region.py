import requests
from bs4 import BeautifulSoup
import pandas as pd

# -----------------------------
# 1. Set up region mapping
# -----------------------------
region_mapping = {
    "Sant Pau Vell": "Agulles",
    "Els Pallers": "Agulles",
    "Saques": "Agulles",
    "Bola De La Partió": "Agulles",
    "Centenar": "Frares Encantats",
    "Frares": "Frares Encantats",
    "Miranda Del Príncep": "Frares Encantats",
    "Comes": "Ecos",
    "Naps": "Ecos",
    "Roca Roja": "Ecos",
    "Palomera": "Sant Jeroni",
    "Faró": "Sant Jeroni",
    "Montgròs": "Sant Jeroni",
    "Ecos": "Sant Jeroni",
    "Sant Jeroni": "Sant Jeroni",
    "Serrat Del Moro": "Sant Jeroni",
    "Sant Antoni": "Sant Jeroni",
    "Albarda": "Sant Jeroni",
    "Vinya Nova": "Magdalenes",
    "Pollegons": "Magdalenes",
    "Bellavista": "Magdalenes",
    "La Plantació": "Magdalenes",
    "Sant Pere": "Magdalenes",
    "Les Gorres": "Magdalenes",
    "Sant Joan": "Magdalenes",
    "Serrat Dels Monjos": "Magdalenes",
    "Serra Llarga": "Magdalenes",
    "Sant Miquel": "Magdalenes",
    "Santa Cova": "Magdalenes",
    "Monestir O Sant Benet": "Sant Salvador",
    "Mullapans": "Sant Salvador",
    "Torrent Escuder": "Sant Salvador",
    "Flautats": "Sant Salvador",
    "Cavall Bernat": "Sant Salvador"
}

# -----------------------------
# 2. Scrape agulles from alphabetical list
# -----------------------------
url = "https://totmontserrat.cat/muntanya/agulles/agulles-ordenades-alfabeticament/"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# Initialize agulles list
agulles = []

# Find the main table
table = soup.find("table")
rows = table.find_all("tr")[1:]  # Skip header row


# Parse each row
for row in rows:
    cols = row.find_all("td")
    if len(cols) < 6:
        continue  # skip malformed rows

    subregion = cols[5].get_text(strip=True)
    name = cols[0].get_text(strip=True)
    code = cols[1].get_text(strip=True)
    altitude = cols[2].get_text(strip=True)
    utm_e = cols[3].get_text(strip=True)
    utm_n = cols[4].get_text(strip=True)

    region = region_mapping.get(subregion, "")

    agulles.append({
        "Name": name,
        "Code": code,
        "Altitude": altitude,
        "Easting": utm_e,
        "Northing": utm_n,
        "Subregion": subregion,
        "Region": region
    })

# -----------------------------
# 3. Save to CSV
# -----------------------------
df = pd.DataFrame(agulles)
df.to_csv("data/agulles_with_region.csv", index=False)

print(f"✅ Scraped and saved {len(df)} agulles to data/agulles_with_region.csv")
print(df.head())

# -----------------------------
# Check for NaN values in the "Region" column
nan_regions = df[df["Region"].isna()]
# -----------------------------
# Print the rows with NaN values in the Region column
print("Rows with NaN in 'Region':")
print(nan_regions)

# Alternatively, you can just count the NaN values
nan_count = df["Region"].isna().sum()
print(f"\nTotal NaN values in 'Region' column: {nan_count}")
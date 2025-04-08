import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

# -----------------------------
# 1. Get all section URLs
# -----------------------------
index_url = "https://totmontserrat.cat/muntanya/agulles/"
res = requests.get(index_url)
soup = BeautifulSoup(res.text, 'html.parser')

section_links = []
for a in soup.find_all("a", href=True):
    href = a['href']
    if "/muntanya/agulles/seccio" in href and href not in section_links:
        full_url = href if href.startswith("http") else f"https://totmontserrat.cat{href}"
        section_links.append(full_url)

print(f"🔗 Found {len(section_links)} sections")

# -----------------------------
# 2. Obtain info of zone and subzone based on URL info
# -----------------------------

# Some URLS are not clearly stated, let's correct them

slug_to_subregion = {
    "seccio-de-sant-pau-vell": "Sant Pau Vell",
    "seccio-dels-pallers": "Els Pallers",
    "seccio-iii-saques": "Saques",
    "seccio-iv": "Bola",
    "seccio-v-centenar": "Centenar",
    "seccio-vi-frares": "Frares",
    "seccio-vii-miranda-del-princep": "Miranda del Príncep",
    "seccio-viii-comes": "Comes",
    "seccio-ix-naps": "Naps",
    "seccio-x-roca-roja": "Roca Roja",
    "seccio-xi-palomera": "Palomera",
    "seccio-xii-faro": "Faró",
    "seccio-xiii-montgros-2": "Montgròs",
    "seccio-xiv-ecos": "Ecos",
    "seccio-xv-sant-jeroni": "Sant Jeroni",
    "seccio-xvi-serrat-del-moro": "Serrat del Moro",
    "seccio-xvii-sant-antoni": "Sant Antoni",
    "seccio-xviii-albarda": "Albarda",
    "seccio-xix-vinya-nova": "Vinya Nova",
    "seccio-xx-pollegons": "Pollegons",
    "seccio-xxi-bellavista": "Bellavista",
    "seccio-xxii-la-plantacio": "La Plantació",
    "seccio-xxiii-sant-pere": "Sant Pere",
    "seccio-xxiv": "Les Gorres",
    "seccio-xxv-sant-joan": "Sant Joan",
    "seccio-xxvii-serrat-dels-monjos": "Serrat dels Monjos",
    "seccio-xxviii": "Serra Llarga",
    "seccio-xxix-sant-miquel": "Sant Miquel",
    "seccio-xxx-santa-cova": "Santa Cova",
    "seccio-xxxi-monestir-o-sant-benet": "Monestir o Sant Benet",
    "seccio-xxxii-mullapans": "Mullapans",
    "seccio-xxxiii-torrent-escuder": "Torrent Escuder",
    "seccio-xxxiv-flautats": "Flautats",
    "seccio-xxxv-cavall-bernat": "Cavall Bernat",
    "seccio-x": "Roca Roja",
    "seccio-12-faro": "Faró",
    "seccio-de-boirafua-1": "De Boirafua 1",
    "seccio-xxiii": "Sant Pere",
    "seccio-xxxii": "Mullapans",
    "seccio-xxvii": "Serrat dels Monjos"
}

# Now let's ddd the subregion_to_region dictionary

subregion_to_region = {
    "Sant Pau Vell": "Agulles",
    "Els Pallers": "Agulles",
    "Saques": "Agulles",
    "Bola": "Agulles",
    "Centenar": "Frares Encantats",
    "Frares": "Frares Encantats",
    "Miranda del Príncep": "Frares Encantats",
    "Comes": "Ecos",
    "Naps": "Ecos",
    "Roca Roja": "Ecos",
    "Palomera": "Sant Jeroni",
    "Faró": "Sant Jeroni",
    "Montgròs": "Sant Jeroni",
    "Ecos": "Sant Jeroni",
    "Sant Jeroni": "Sant Jeroni",
    "Serrat del Moro": "Sant Jeroni",
    "Sant Antoni": "Sant Jeroni",
    "Albarda": "Sant Jeroni",
    "Vinya Nova": "Magdalenes",
    "Pollegons": "Magdalenes",
    "Bellavista": "Magdalenes",
    "La Plantació": "Magdalenes",
    "Sant Pere": "Magdalenes",
    "Les Gorres": "Magdalenes",
    "Sant Joan": "Magdalenes",
    "Serrat dels Monjos": "Magdalenes",
    "Serra Llarga": "Magdalenes",
    "Sant Miquel": "Magdalenes",
    "Santa Cova": "Magdalenes",
    "Monestir o Sant Benet": "Sant Salvador",
    "Mullapans": "Sant Salvador",
    "Torrent Escuder": "Sant Salvador",
    "Flautats": "Sant Salvador",
    "Cavall Bernat": "Sant Salvador",
    "De Boirafua 1": "Sant Salvador"
}

# We can now use it in our scraping loop


# -----------------------------
# 3. Extract full Agulla info from each section
# -----------------------------
agulles_data = []

for url in section_links:
    print(f"🔍 Processing: {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Get slug from URL
    slug = urlparse(url).path.strip("/").split("/")[-1]
    subregion = slug_to_subregion.get(slug, "Unknown")
    region = subregion_to_region.get(subregion, "Unknown")

    table = soup.find("table")
    if not table:
        continue

    rows = table.find_all("tr")[1:]  # skip header row

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        name = cols[0].get_text(strip=True)
        code = cols[1].get_text(strip=True)
        altitude = cols[2].get_text(strip=True)
        easting = cols[3].get_text(strip=True)
        northing = cols[4].get_text(strip=True)
        description = cols[5].get_text(strip=True)

        if not name or name.lower() == "nom agulla":
            continue

        agulles_data.append({
            "Name": name,
            "Code": code,
            "Altitude": altitude,
            "Easting": easting,
            "Northing": northing,
            "Description": description,
            "Subregion": subregion,
            "Region": region,
            "SourceURL": url
        })

print(f"✅ Extracted {len(agulles_data)} agulles")

# -----------------------------
# 4. Save as CSV
# -----------------------------
df = pd.DataFrame(agulles_data)
df.to_csv("data/agulles_full_data.csv", index=False, encoding='utf-8-sig')
print("💾 Saved to data/agulles_full_data.csv")
print("\n🔎 Sample agulles:")
print(df.head(5))
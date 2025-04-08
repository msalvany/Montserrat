import requests
from bs4 import BeautifulSoup
import pandas as pd

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
# 2. Extract name + description
# -----------------------------
agulles_data = []

for url in section_links:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Section-level description (if you ever want it, we can use it)
    # desc_div = soup.find("div", class_="et_pb_text_inner")
    # section_description = desc_div.get_text(strip=True) if desc_div else ""

    # Table
    table = soup.find("table")
    if not table:
        continue

    rows = table.find_all("tr")[1:]  # skip header row

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        name = cols[0].get_text(strip=True)
        description = cols[5].get_text(strip=True)

        # Clean up blank rows
        if not name or name.lower() == "nom agulla":
            continue

        agulles_data.append({
            "Name": name,
            "Description": description
        })

print(f"✅ Extracted {len(agulles_data)} agulles")

# -----------------------------
# 3. Save as CSV
# -----------------------------
df = pd.DataFrame(agulles_data)
df.to_csv("data/agulles_name_description.csv", index=False)
print("💾 Saved to data/agulles_name_description.csv")
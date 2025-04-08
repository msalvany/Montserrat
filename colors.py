import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Define base colors per region
REGION_COLORS = {
    "Agulles": "#e76f51",           # Terracotta red
    "Frares Encantats": "#2a9d8f",  # Teal green
    "Ecos": "#f4a261",              # Soft orange
    "Sant Jeroni": "#264653",       # Deep blue-gray
    "Magdalenes": "#8ecae6",        # Sky blue
    "Sant Salvador": "#ffb703",     # Warm gold
}

# Define some subregions to demonstrate
SUBREGIONS = {
    "Agulles": ["Sant Pau Vell", "Els Pallers", "Saques", "Bola de la Partió"],
    "Frares Encantats": ["Frares", "Miranda del Príncep"],
    "Ecos": ["Comes", "Naps", "Roca Roja"],
    "Sant Jeroni": ["Palomera", "Faró", "Montgròs"],
    "Magdalenes": ["Vinya Nova", "Pollegons", "Bellavista"],
    "Sant Salvador": ["Monestir O Sant Benet", "Mullapans", "Torrent Escuder", "Flautats", "Cavall Bernat"]
}

# Function to adjust brightness for subregions
def adjust_brightness(hex_color, factor):
    import matplotlib.colors as mcolors
    rgb = mcolors.to_rgb(hex_color)
    adjusted = tuple(min(1, c * factor) for c in rgb)
    return mcolors.to_hex(adjusted)

# Create the legend with regions and subregions
def print_color_legend():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Loop through each region
    for i, (region, hex_color) in enumerate(REGION_COLORS.items()):
        # Plot main region color
        ax.barh(i, 1, color=hex_color)
        ax.text(0.05, i, region, va='center', fontsize=12, color='white' if region != "Sant Salvador" else 'black')

        # Loop through subregions and add color with brightness adjustments
        subregions = SUBREGIONS.get(region, [])
        for j, subregion in enumerate(subregions):
            subregion_color = adjust_brightness(hex_color, 0.8 + j * 0.1)  # Slightly darker for each subregion
            ax.barh(i + 0.1 * (j + 1), 1, color=subregion_color)
            ax.text(0.05, i + 0.1 * (j + 1), f"{subregion}", va='center', fontsize=10, color='white')

    # Hide ticks and add title
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Region and Subregion Color Legend")
    plt.tight_layout()

    # Show the legend without plotting any data
    plt.show()

# Call the function to display the legend
print_color_legend()
import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.patheffects as pe
from adjustText import adjust_text

# Define base colors per region
REGION_COLORS = {
    "Agulles": "#e76f51",           # Terracotta red
    "Frares Encantats": "#2a9d8f",  # Teal green
    "Ecos": "#f4a261",              # Soft orange
    "Sant Jeroni": "#264653",       # Deep blue-gray
    "Magdalenes": "#8ecae6",        # Sky blue
    "Sant Salvador": "#ffb703",     # Warm gold
}

# Optional: subregion variants (shades of main color)
def get_kml_color(region):
    """
    Convert a HEX color to KML color (AABBGGRR)
    """
    hex_color = REGION_COLORS.get(region, "#888888").lstrip("#")
    rr, gg, bb = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"ff{bb}{gg}{rr}"  # KML format: AABBGGRR

def adjust_brightness(hex_color, factor):
    import matplotlib.colors as mcolors
    rgb = mcolors.to_rgb(hex_color)
    adjusted = tuple(min(1, c * factor) for c in rgb)
    return adjusted

import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.patheffects as pe
from adjustText import adjust_text

def plot_montserrat_map(gdf, region_name=None, fast_mode=True, save_path=None):
    gdf_web = gdf.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(16, 14))

    # Optional: Color by Subregion
    subregions = gdf_web["Subregion"].unique()
    colors = plt.cm.tab20.colors  # Up to 20 unique subregion colors

    for i, sub in enumerate(subregions):
        gdf_web[gdf_web["Subregion"] == sub].plot(
            ax=ax, color=colors[i % len(colors)], markersize=40, label=sub
        )

    texts = []
    for x, y, label in zip(gdf_web.geometry.x, gdf_web.geometry.y, gdf_web['Name']):
        # Circle with square inside
        ax.scatter(x, y, color='white', s=100, edgecolors='black', marker='s', alpha=0.5)  # Square
        ax.scatter(x, y, color='blue', s=40, edgecolors='black', marker='o', alpha=1)  # Circle inside
        
        # Add label text, ensuring it's placed properly without overlap
        texts.append(ax.text(x, y, label,
                             fontsize=10, ha='right', color='black',
                             path_effects=[pe.withStroke(linewidth=2, foreground='white')]))

    if not fast_mode:
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black', lw=1))

    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom=17)
    ax.set_title(f"🗺️ Region: {region_name}", fontsize=16)
    ax.legend(loc="lower left", fontsize=9)
    ax.axis("off")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved map to {save_path}")
        plt.close()
    else:
        plt.show()
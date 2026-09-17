import os

import geopandas as gpd
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm
from shapely.geometry import Point

try:
    from adjustText import adjust_text
except ImportError:
    adjust_text = None


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SHAPEFILE_PATH = os.path.join(
    SCRIPT_DIR,
    "cb_2018_us_state_20m",
    "cb_2018_us_state_20m.shp",
)
CSV_PATH = os.path.join(SCRIPT_DIR, "Fig1A.csv")
OUTPUT_DIR = SCRIPT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

REQUIRED_COLUMNS = {
    "city",
    "overall_mobility_asymmetry",
    "mobility_gini_coefficient",
    "mobility_coefficient_variation",
    "asymmetry_std",
    "Tot_Population_ACS_15_19",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": 14,
    "axes.unicode_minus": False,
})

CITY_COORDS = {
    "Los Angeles": (34.0522, -118.2437),
    "San Diego": (32.7157, -117.1611),
    "Phoenix": (33.4484, -112.0740),
    "Washington, D.C": (38.9072, -77.0369),
    "Miami": (25.7617, -80.1918),
    "Atlanta": (33.7490, -84.3880),
    "Chicago": (41.8781, -87.6298),
    "San Francisco": (37.7749, -122.4194),
    "Boston": (42.3601, -71.0589),
    "Detroit": (42.3314, -83.0458),
    "St. Louis": (38.6270, -90.1994),
    "New York": (40.7128, -74.0060),
    "Pittsburgh": (40.4406, -79.9959),
    "Philadelphia": (39.9526, -75.1652),
    "Dallas": (32.7767, -96.7970),
    "Houston": (29.7604, -95.3698),
}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def load_data():
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    validate_columns(df, REQUIRED_COLUMNS, CSV_PATH)

    df = df.copy()
    df["city"] = df["city"].astype(str).str.strip()

    missing_coords = sorted(set(df["city"]) - set(CITY_COORDS))
    if missing_coords:
        raise ValueError(f"Missing coordinates for cities: {missing_coords}")

    numeric_columns = REQUIRED_COLUMNS - {"city"}
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["city_label"] = df["city"]
    df["lat"] = df["city"].map(lambda city: CITY_COORDS[city][0])
    df["lon"] = df["city"].map(lambda city: CITY_COORDS[city][1])
    df["population"] = df["Tot_Population_ACS_15_19"]

    return df.dropna(subset=["lat", "lon", "population", "overall_mobility_asymmetry"])


def plot_pro_map(data, pop_col, title_text, filename, style="academic"):
    if style == "academic":
        bg_color, land_color, border_color = "white", "#F5F5F5", "#CCCCCC"
        text_color, dot_edge_color = "#222222", "#333333"
        cmap_name = "YlOrRd"
    else:
        bg_color, land_color, border_color = "#222222", "#333333", "#555555"
        text_color, dot_edge_color = "#EEEEEE", "white"
        cmap_name = "magma_r"

    usa = gpd.read_file(SHAPEFILE_PATH)
    usa = usa[~usa["STUSPS"].isin(["AK", "HI", "PR"])]

    map_height = 2500000
    usa = usa.to_crs("EPSG:5070")
    usa["geometry"] = usa.geometry.buffer(0)

    geometry = [Point(xy) for xy in zip(data.lon, data.lat)]
    geo_df = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326").to_crs(usa.crs)

    fig, ax = plt.subplots(1, 1, figsize=(16, 11), dpi=300)
    fig.patch.set_facecolor(bg_color)
    ax.set_axis_off()

    usa.plot(ax=ax, color=land_color, edgecolor=border_color, linewidth=1.0, zorder=1)

    asym_vals = data["overall_mobility_asymmetry"].values
    min_size, max_size = 100, 800
    sizes = (
        (asym_vals - asym_vals.min())
        / (asym_vals.max() - asym_vals.min() + 1e-9)
        * (max_size - min_size)
        + min_size
    )

    val = data[pop_col].values
    norm = LogNorm(vmin=300000, vmax=11000000)

    std_vals = data["asymmetry_std"].fillna(0).values
    max_std = std_vals.max() if std_vals.max() > 0 else 1.0
    scale_factor = (map_height * 0.06) / max_std
    yerr_scaled = std_vals * scale_factor

    scatter = ax.scatter(
        geo_df.geometry.x,
        geo_df.geometry.y,
        s=sizes,
        c=val,
        cmap=cmap_name,
        norm=norm,
        edgecolor=dot_edge_color,
        linewidth=1.0,
        alpha=0.9,
        zorder=3,
    )

    ax.errorbar(
        geo_df.geometry.x,
        geo_df.geometry.y,
        yerr=yerr_scaled,
        fmt="none",
        ecolor="black",
        elinewidth=1.8,
        capsize=3,
        alpha=0.9,
        zorder=4,
    )

    texts = []
    offsets = {
        "New York": (10000, 20000),
        "Philadelphia": (10000, -20000),
        "Detroit": (20000, 10000),
        "Chicago": (-30000, 0),
        "Boston": (20000, 20000),
    }

    for x, y, label in zip(geo_df.geometry.x, geo_df.geometry.y, geo_df["city_label"]):
        dx, dy = offsets.get(label, (0, 0))
        texts.append(ax.text(x + dx, y + dy, label, fontsize=14, color=text_color, zorder=10))

    if adjust_text:
        adjust_text(
            texts,
            ax=ax,
            expand_points=(2.0, 2.0),
            force_text=(0.2, 0.5),
            arrowprops=dict(
                arrowstyle="-",
                color="gray",
                lw=0.6,
                alpha=0.6,
                shrinkA=5,
                shrinkB=5,
            ),
            save_steps=False,
        )

    cax = fig.add_axes([0.35, 0.12, 0.3, 0.025])
    cbar = plt.colorbar(scatter, cax=cax, orientation="horizontal")
    cbar.outline.set_visible(False)
    cbar.set_ticks([300000, 1000000, 3000000, 10000000])
    cbar.set_ticklabels(["300K", "1M", "3M", "10M"])
    cbar.ax.tick_params(labelsize=14, color=text_color, labelcolor=text_color)
    cbar.set_label("Total population (log scale)", fontsize=16, color=text_color, labelpad=8)

    handles = []
    levels = [np.min(asym_vals), np.median(asym_vals), np.max(asym_vals)]
    meaning_labels = ["Min", "Median", "Max"]

    for value, meaning_label in zip(levels, meaning_labels):
        size = (
            (value - asym_vals.min())
            / (asym_vals.max() - asym_vals.min() + 1e-9)
            * (max_size - min_size)
            + min_size
        )
        handles.append(
            mlines.Line2D(
                [],
                [],
                color=text_color,
                marker="o",
                linestyle="None",
                markersize=np.sqrt(size),
                markerfacecolor="None",
                markeredgewidth=1.2,
                markeredgecolor=text_color,
                alpha=0.8,
                label=f"{value:.2f} ({meaning_label})",
            )
        )

    legend = ax.legend(
        handles=handles,
        title="Flow asymmetry ($FA$)",
        loc="lower left",
        bbox_to_anchor=(0.03, 0.04),
        frameon=False,
        labelspacing=1.2,
        fontsize=14,
    )

    plt.setp(legend.get_title(), fontsize=16, color=text_color)
    for text in legend.get_texts():
        text.set_color(text_color)

    save_path = os.path.join(OUTPUT_DIR, f"{filename}.svg")
    plt.savefig(save_path, bbox_inches="tight", dpi=300, facecolor=bg_color)
    plt.savefig(save_path.replace(".svg", ".png"), bbox_inches="tight", dpi=300, facecolor=bg_color)
    print(f"[{style}] Saved figure: {filename}")
    plt.close()


if __name__ == "__main__":
    try:
        df_clean = load_data()
        plot_pro_map(
            df_clean,
            "population",
            "Urban Scale & Mobility Asymmetry",
            "Fig1A_Pop_Academic",
            style="academic",
        )
    except Exception:
        import traceback

        traceback.print_exc()

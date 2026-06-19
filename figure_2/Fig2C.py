# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:22:05 2026

@author: Dell
"""

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FixedLocator
from scipy import stats


plt.style.use("default")
plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE_FILE = os.path.join(SCRIPT_DIR, "Fig2BC.csv")
DATA_DIR = os.path.join(SCRIPT_DIR, "Fig2BC_city", "LPW_to_HPM")
OUTPUT_DIR = SCRIPT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASELINE_COLUMN = "log_HPM"
FLOW_SHARE_COLUMN = "log_flow_share_LPW_to_HPM"
REQUIRED_REFERENCE_COLUMNS = {"city", BASELINE_COLUMN}
REQUIRED_CITY_COLUMNS = {FLOW_SHARE_COLUMN}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


reference_df = pd.read_csv(REFERENCE_FILE)
validate_columns(reference_df, REQUIRED_REFERENCE_COLUMNS, REFERENCE_FILE)

reference_values = (
    reference_df.dropna(subset=["city", BASELINE_COLUMN])
    .assign(city=lambda frame: frame["city"].astype(str).str.strip())
    .set_index("city")[BASELINE_COLUMN]
    .astype(float)
    .to_dict()
)

csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
city_data = {}

for file_path in csv_files:
    city = os.path.splitext(os.path.basename(file_path))[0]
    df = pd.read_csv(file_path)
    validate_columns(df, REQUIRED_CITY_COLUMNS, file_path)
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.strip()
    df[FLOW_SHARE_COLUMN] = pd.to_numeric(df[FLOW_SHARE_COLUMN], errors="coerce")
    values = df[FLOW_SHARE_COLUMN].dropna().values
    if len(values) > 1:
        city_data[city] = values

if not city_data:
    raise ValueError(f"No usable city data found in {DATA_DIR}")

city_means = {city: np.mean(data) for city, data in city_data.items()}
city_order = sorted(city_means.keys(), key=lambda city: city_means[city], reverse=True)

fig, ax = plt.subplots(figsize=(14, 12))
fig.patch.set_facecolor("white")

n_cities = len(city_order)
colors = plt.cm.Blues(np.linspace(0.3, 0.9, n_cities))

all_values = np.concatenate([city_data[city] for city in city_order])
x_min_data, x_max_data = np.min(all_values), np.max(all_values)
matching_refs = [reference_values[city] for city in city_order if city in reference_values]
max_ref_value = max(matching_refs) if matching_refs else x_max_data
min_ref_value = min(matching_refs) if matching_refs else x_min_data
x_min, x_max = min(x_min_data, min_ref_value), max(x_max_data, max_ref_value)
buffer = (x_max - x_min) * 0.05
x_min_plot, x_max_plot = x_min - buffer, x_max + buffer

ridge_height, y_spacing, overlap = 0.7, 1.2, 0.65
ref_line_height_factor = 0.8

for i, city in enumerate(city_order):
    data = city_data[city]
    density = stats.gaussian_kde(data)
    x_range = np.linspace(x_min_plot, x_max_plot, 500)
    y_density = density(x_range)
    y_density = y_density / y_density.max() * ridge_height
    y_pos = (n_cities - 1 - i) * y_spacing

    ax.plot([x_min_plot, x_max_plot], [y_pos, y_pos], color="black", linewidth=0.5, alpha=0.6)

    median = np.median(data)
    q25, q75 = np.percentile(data, [25, 75])

    for quantile, line_width in zip([median, q25, q75], [2.5, 1.5, 1.5]):
        q_y = y_pos + y_density[np.argmin(np.abs(x_range - quantile))]
        ax.plot(
            [quantile, quantile],
            [y_pos, q_y],
            color="white",
            linewidth=line_width,
            alpha=0.9,
            linestyle="--" if quantile == median else "-",
        )

    ax.fill_between(x_range, y_pos, y_pos + y_density, color=colors[i], alpha=0.95, linewidth=0)
    ax.plot(x_range, y_pos + y_density, color="black", linewidth=1.2)

first_ref = True
for i, city in enumerate(city_order):
    if city in reference_values:
        ref_value = reference_values[city]
        data = city_data[city]
        median = np.median(data)
        y_pos = (n_cities - 1 - i) * y_spacing

        line_height = ridge_height * ref_line_height_factor
        y_bottom = y_pos
        y_top = y_pos + line_height
        x_start, x_end = sorted([ref_value, median])
        ax.fill_betweenx([y_bottom, y_top], x_start, x_end, color="#1f77b4", alpha=0.2, zorder=1)

        if first_ref:
            ax.vlines(
                ref_value,
                y_pos,
                y_top,
                color="#d62728",
                linewidth=2.0,
                alpha=1.0,
                label="Share of City Population in HPM CBGs (population baseline)",
            )
            first_ref = False
        else:
            ax.vlines(ref_value, y_pos, y_top, color="#d62728", linewidth=2.0, alpha=1.0)

ax.set_xlim(x_min_plot, x_max_plot)
ax.set_ylim(-0.5, (n_cities - 1) * y_spacing + ridge_height + 0.8)
y_ticks = [(n_cities - 1 - i) * y_spacing + ridge_height * overlap for i in range(n_cities)]
ax.set_yticks(y_ticks)
ax.set_yticklabels(city_order, fontsize=22, fontweight="medium", ha="right", x=-0.01)

target_percentages = [0.2, 0.5, 1, 2, 5, 10, 20]
target_xticks = np.log(np.array(target_percentages) / 100)
ax.xaxis.set_major_locator(FixedLocator(target_xticks))
ax.set_xticklabels([f"{p}%" for p in target_percentages], fontsize=22)

minor_percentages = [0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 3, 4, 6, 7, 8, 9, 15]
minor_xticks = np.log(np.array(minor_percentages) / 100)
ax.xaxis.set_minor_locator(FixedLocator(minor_xticks))

ax.set_xlabel("Flow ratio ($P_{LH}$)", fontsize=24, labelpad=15)

ax.tick_params(axis="both", which="major", labelsize=22, width=1.2)
ax.tick_params(axis="x", which="major", length=8)
ax.tick_params(axis="x", which="minor", length=4, color="gray")

ax.grid(axis="x", which="major", linestyle="--", alpha=0.3, linewidth=0.6)
ax.grid(axis="x", which="minor", linestyle=":", alpha=0.15, linewidth=0.5)

ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1.2)
ax.spines["bottom"].set_linewidth(1.2)

ax.legend(loc="upper left", fontsize=22, frameon=False)

plt.tight_layout()

png_path = os.path.join(OUTPUT_DIR, "Fig2C.png")
svg_path = os.path.join(OUTPUT_DIR, "Fig2C.svg")
plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(svg_path, bbox_inches="tight", facecolor="white")

plt.show()
print(f"Figure saved: {png_path}")

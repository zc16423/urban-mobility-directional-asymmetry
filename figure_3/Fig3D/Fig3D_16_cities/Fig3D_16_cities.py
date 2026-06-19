# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:52:36 2026

@author: Dell
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch


plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["axes.unicode_minus"] = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
base_dirs = {
    "Real": os.path.join(SCRIPT_DIR, "real"),
    "Gravity model": os.path.join(SCRIPT_DIR, "gravity"),
}

CITY_NAMES = [
    "Los Angeles",
    "San Diego",
    "Washington, D.C",
    "Miami",
    "Atlanta",
    "Chicago",
    "Boston",
    "Detroit",
    "New York",
    "Pittsburgh",
    "Philadelphia",
    "Dallas",
    "San Francisco",
    "Houston",
    "Phoenix",
    "St. Louis",
]

FLOW_LPW_TO_HPM = "LPW_to_HPM"
FLOW_HPM_TO_LPW = "HPM_to_LPW"
FLOW_COLUMN_MAP = {
    FLOW_LPW_TO_HPM: "total_od_flow_LPW_to_HPM",
    FLOW_HPM_TO_LPW: "total_od_flow_HPM_to_LPW",
}
FLOW_DISPLAY = {
    FLOW_LPW_TO_HPM: "LPW to HPM",
    FLOW_HPM_TO_LPW: "HPM to LPW",
}
flow_order = [FLOW_LPW_TO_HPM, FLOW_HPM_TO_LPW]
model_order = ["Real", "Gravity model"]


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


all_data = []
sorted_cities = sorted(CITY_NAMES)

print("Reading data...")

for city in sorted_cities:
    for model_name in model_order:
        folder_path = base_dirs[model_name]
        file_path = os.path.join(folder_path, f"{city}.csv")

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                validate_columns(df, set(FLOW_COLUMN_MAP.values()), file_path)

                for flow_type, column_name in FLOW_COLUMN_MAP.items():
                    temp_df = df[[column_name]].copy()
                    temp_df.columns = ["flow_count"]
                    temp_df["flow_type"] = flow_type
                    temp_df["Model"] = model_name
                    temp_df["city"] = city
                    all_data.append(temp_df)

            except Exception as exc:
                print(f"Read error for {city}: {exc}")

if not all_data:
    raise ValueError("No data were loaded. Check input paths.")

plot_data = pd.concat(all_data, ignore_index=True)

color_map = {
    (FLOW_LPW_TO_HPM, "Real"): "#A7B9D7",
    (FLOW_LPW_TO_HPM, "Gravity model"): "#A7B9D7",
    (FLOW_HPM_TO_LPW, "Real"): "#E4908E",
    (FLOW_HPM_TO_LPW, "Gravity model"): "#E4908E",
}

alpha_map = {
    (FLOW_LPW_TO_HPM, "Real"): 0.5,
    (FLOW_LPW_TO_HPM, "Gravity model"): 1.0,
    (FLOW_HPM_TO_LPW, "Real"): 0.5,
    (FLOW_HPM_TO_LPW, "Gravity model"): 1.0,
}

sns.set_style("ticks")

fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(18, 16), sharey=False)
axes = axes.flatten()

for i, city in enumerate(sorted_cities):
    if i >= len(axes):
        break

    ax = axes[i]
    city_data = plot_data[plot_data["city"] == city]

    if city_data.empty:
        ax.set_title(f"{city} (No Data)")
        continue

    sns.violinplot(
        data=city_data,
        x="flow_type",
        y="flow_count",
        hue="Model",
        ax=ax,
        split=True,
        inner="quart",
        cut=0,
        order=flow_order,
        hue_order=model_order,
        palette=["#000000", "#000000"],
        linewidth=1,
    )

    ax.tick_params(axis="both", which="major", width=1, length=4, direction="out", colors="black")

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)

    for idx, violin in enumerate(ax.collections):
        try:
            x_idx = idx // 2
            model_idx = idx % 2
            if x_idx < len(flow_order) and model_idx < len(model_order):
                current_flow = flow_order[x_idx]
                current_model = model_order[model_idx]
                color = color_map.get((current_flow, current_model), "gray")
                alpha = alpha_map.get((current_flow, current_model), 1.0)
                violin.set_facecolor(color)
                violin.set_alpha(alpha)
                violin.set_edgecolor("black")
                violin.set_linewidth(0.5)
        except Exception:
            pass

    ax.set_title(city, fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Flow volume", fontsize=12)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([FLOW_DISPLAY[FLOW_LPW_TO_HPM], FLOW_DISPLAY[FLOW_HPM_TO_LPW]], fontsize=12)

    if ax.get_legend():
        ax.legend_.remove()

for j in range(len(sorted_cities), len(axes)):
    fig.delaxes(axes[j])

custom_legend = [
    Patch(facecolor="#A7B9D7", edgecolor="black", linewidth=0.5, alpha=0.5, label="Real: LPW to HPM"),
    Patch(facecolor="#A7B9D7", edgecolor="black", linewidth=0.5, alpha=1.0, label="Gravity model: LPW to HPM"),
    Patch(facecolor="#E4908E", edgecolor="black", linewidth=0.5, alpha=0.5, label="Real: HPM to LPW"),
    Patch(facecolor="#E4908E", edgecolor="black", linewidth=0.5, alpha=1.0, label="Gravity model: HPM to LPW"),
]

fig.legend(
    handles=custom_legend,
    loc="lower center",
    ncol=2,
    fontsize=14,
    bbox_to_anchor=(0.5, 0.01),
    frameon=False,
)
plt.tight_layout(rect=[0, 0.05, 1, 1])

output_path = os.path.join(SCRIPT_DIR, "Fig3D_16_city_real_vs_gravity.svg")
plt.savefig(output_path, format="svg", dpi=300)
plt.show()

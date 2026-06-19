# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 11:35:08 2026

@author: Dell
"""

import glob
import os

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
daily_folder = os.path.join(SCRIPT_DIR, "Fig3A_day")
yearly_file = os.path.join(SCRIPT_DIR, "Fig3A_year.csv")
output_folder = SCRIPT_DIR
os.makedirs(output_folder, exist_ok=True)

YEARLY_COLUMNS = {
    "city",
    "flow_type",
    "Sum_Observed_Flow",
    "Sum_Predicted_Flow",
    "Realization_Ratio_R",
}
DAILY_COLUMNS = {"flow_type", "Realization_Ratio_R"}

FLOW_HPM_TO_LPW = "HPM_to_LPW"
FLOW_LPW_TO_HPM = "LPW_to_HPM"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 12
plt.rcParams["axes.linewidth"] = 1.0
plt.rcParams["xtick.major.width"] = 1.0
plt.rcParams["ytick.major.width"] = 1.0
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"

COLOR_H2L = "#D35450"
COLOR_L2H = "#4E79A7"
COLOR_LINK = "#bdbdbd"

LABEL_H2L = "HPM to LPW"
LABEL_L2H = "LPW to HPM"


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


print("Reading data...")

df_yearly = pd.read_csv(yearly_file)
validate_columns(df_yearly, YEARLY_COLUMNS, yearly_file)
df_yearly["city"] = df_yearly["city"].astype(str).str.strip()
df_yearly["flow_type"] = df_yearly["flow_type"].astype(str).str.strip()
df_yearly["Realization_Ratio_R"] = pd.to_numeric(
    df_yearly["Realization_Ratio_R"],
    errors="coerce",
)

daily_stats = []
daily_files = glob.glob(os.path.join(daily_folder, "*.csv"))

for file_path in daily_files:
    filename = os.path.basename(file_path)
    daily_city = os.path.splitext(filename)[0]
    try:
        df_d = pd.read_csv(file_path)
        validate_columns(df_d, DAILY_COLUMNS, file_path)
        df_d["city"] = daily_city
        df_d["flow_type"] = df_d["flow_type"].astype(str).str.strip()
        df_d["Realization_Ratio_R"] = pd.to_numeric(
            df_d["Realization_Ratio_R"],
            errors="coerce",
        )

        grouped = (
            df_d.groupby(["city", "flow_type"])["Realization_Ratio_R"]
            .std()
            .reset_index()
        )
        grouped.rename(columns={"Realization_Ratio_R": "R_Std"}, inplace=True)
        daily_stats.append(grouped)
    except Exception as exc:
        print(f"Failed to process daily file {filename}: {exc}")

if daily_stats:
    df_daily_std = pd.concat(daily_stats, ignore_index=True)
else:
    print("WARNING: no daily data found; error bars will be set to zero.")
    df_daily_std = pd.DataFrame(columns=["city", "flow_type", "R_Std"])

df_merged = pd.merge(df_yearly, df_daily_std, on=["city", "flow_type"], how="left")
df_merged["R_Std"] = df_merged["R_Std"].fillna(0)

df_h2l = df_merged[df_merged["flow_type"] == FLOW_HPM_TO_LPW][
    ["city", "Realization_Ratio_R", "R_Std"]
].copy()
df_l2h = df_merged[df_merged["flow_type"] == FLOW_LPW_TO_HPM][
    ["city", "Realization_Ratio_R", "R_Std"]
].copy()

df_h2l.rename(columns={"Realization_Ratio_R": "R_H2L", "R_Std": "Std_H2L"}, inplace=True)
df_l2h.rename(columns={"Realization_Ratio_R": "R_L2H", "R_Std": "Std_L2H"}, inplace=True)

df_plot = pd.merge(df_h2l, df_l2h, on=["city"])

df_plot.sort_values("R_L2H", ascending=True, inplace=True)
df_plot.reset_index(drop=True, inplace=True)

print("Plotting...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

y_pos = np.arange(len(df_plot))
plot_city_labels = df_plot["city"]

ax.axvline(x=1.0, color="black", linestyle="--", linewidth=1, alpha=1.0, zorder=0)

ax.text(
    0.625,
    1.01,
    "$R=1.0$",
    color="black",
    fontsize=12,
    ha="right",
    va="top",
    transform=ax.transAxes,
)

ax.hlines(
    y=y_pos,
    xmin=df_plot["R_L2H"],
    xmax=df_plot["R_H2L"],
    color=COLOR_LINK,
    alpha=1.0,
    linewidth=1.5,
    zorder=1,
)

ax.errorbar(
    x=df_plot["R_H2L"],
    y=y_pos,
    xerr=df_plot["Std_H2L"],
    fmt="o",
    color=COLOR_H2L,
    ecolor=COLOR_H2L,
    markersize=8,
    capsize=4,
    capthick=1,
    elinewidth=1,
    label=LABEL_H2L,
    zorder=3,
)

ax.errorbar(
    x=df_plot["R_L2H"],
    y=y_pos,
    xerr=df_plot["Std_L2H"],
    fmt="o",
    color=COLOR_L2H,
    ecolor=COLOR_L2H,
    markersize=8,
    capsize=4,
    capthick=1,
    elinewidth=1,
    label=LABEL_L2H,
    zorder=3,
)

ax.set_yticks(y_pos)
ax.set_yticklabels(plot_city_labels, fontsize=12)

ax.set_xlabel("Realization ratio ($R$)", fontsize=14, labelpad=10)
max_val = max(df_plot["R_H2L"].max(), df_plot["R_L2H"].max())
ax.set_xlim(0.3, max_val * 1.2)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(True)

ax.grid(axis="x", linestyle=":", alpha=0.4)
ax.set_axisbelow(True)

legend_elements = [
    mlines.Line2D([], [], color=COLOR_H2L, marker="o", linestyle="None", markersize=8, label=r"HPM $\to$ LPW"),
    mlines.Line2D([], [], color=COLOR_L2H, marker="o", linestyle="None", markersize=8, label=r"LPW $\to$ HPM"),
    mlines.Line2D([], [], color=COLOR_LINK, lw=1.5, label="Directional gap"),
]

ax.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),
    ncol=3,
    frameon=False,
    fontsize=14,
)

svg_path = os.path.join(output_folder, "Fig3A.svg")
plt.savefig(svg_path, format="svg", bbox_inches="tight")
png_path = os.path.join(output_folder, "Fig3A.png")
plt.savefig(png_path, dpi=300, bbox_inches="tight")
print(f"Figure saved to:\n - {png_path}")
plt.show()

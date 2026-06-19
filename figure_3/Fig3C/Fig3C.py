# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 17:27:59 2026

@author: Dell
"""

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
file_pred = os.path.join(SCRIPT_DIR, "Fig3C_gravity_year.csv")
file_real = os.path.join(SCRIPT_DIR, "Fig3C_real_year.csv")
daily_folder = os.path.join(SCRIPT_DIR, "Fig3C_real_day")
output_folder = SCRIPT_DIR
os.makedirs(output_folder, exist_ok=True)

TARGET_FLOW = "LPW_to_HPM"
YEARLY_COLUMNS = {"city", "flow_type", "weighted_avg_asymmetry"}
DAILY_COLUMNS = {"Date", "Day of Week", "total_flow", "weighted_avg_asymmetry"}

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 12
plt.rcParams["axes.linewidth"] = 1.0
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


print("1. Reading yearly data...")
df_pred = pd.read_csv(file_pred)
df_real = pd.read_csv(file_real)
validate_columns(df_pred, YEARLY_COLUMNS, file_pred)
validate_columns(df_real, YEARLY_COLUMNS, file_real)

df_pred["city"] = df_pred["city"].astype(str).str.strip()
df_real["city"] = df_real["city"].astype(str).str.strip()
df_pred["flow_type"] = df_pred["flow_type"].astype(str).str.strip()
df_real["flow_type"] = df_real["flow_type"].astype(str).str.strip()

df_pred_sub = df_pred[df_pred["flow_type"] == TARGET_FLOW][
    ["city", "weighted_avg_asymmetry"]
].copy()
df_real_sub = df_real[df_real["flow_type"] == TARGET_FLOW][
    ["city", "weighted_avg_asymmetry"]
].copy()

df_pred_sub.rename(columns={"weighted_avg_asymmetry": "FA_Pred"}, inplace=True)
df_real_sub.rename(columns={"weighted_avg_asymmetry": "FA_Obs"}, inplace=True)
df_plot = pd.merge(df_real_sub, df_pred_sub, on="city")

print("2. Calculating daily error bars...")
std_results = []
daily_files = glob.glob(os.path.join(daily_folder, "*.csv"))

if daily_files:
    for file_path in daily_files:
        try:
            city = os.path.splitext(os.path.basename(file_path))[0]
            df_d = pd.read_csv(file_path)
            validate_columns(df_d, DAILY_COLUMNS, file_path)
            df_d["weighted_avg_asymmetry"] = pd.to_numeric(
                df_d["weighted_avg_asymmetry"],
                errors="coerce",
            )
            # Daily files are not filtered by flow_type because the verified daily
            # schema does not contain flow_type; they are treated as pre-filtered
            # or aggregated cross-boundary asymmetry series.
            std_results.append({
                "city": city,
                "FA_Obs_Std": df_d["weighted_avg_asymmetry"].std(),
            })
        except Exception as exc:
            print(f"Failed to process daily file {file_path}: {exc}")

if std_results:
    df_std = pd.DataFrame(std_results)
    df_plot = pd.merge(df_plot, df_std, on="city", how="left")
    df_plot["FA_Obs_Std"] = df_plot["FA_Obs_Std"].fillna(0)
else:
    df_plot["FA_Obs_Std"] = 0

print("3. Plotting final figure...")

fig, ax = plt.subplots(figsize=(9, 9.8), dpi=300)
limit_min, limit_max = 0.2, 0.82

ax.plot(
    [limit_min, limit_max],
    [limit_min, limit_max],
    color="#444444",
    linestyle="--",
    linewidth=1.5,
    alpha=0.9,
    zorder=1,
)
ax.text(
    limit_max - 0.01,
    limit_max - 0.1,
    "$FA_{\\mathrm{Real}} = FA_{\\mathrm{Gravity}}$",
    ha="right",
    va="bottom",
    fontsize=14,
    color="black",
)

x_vals = np.linspace(limit_min, limit_max, 100)
ax.fill_between(x_vals, x_vals, limit_max, color="#e7298a", alpha=0.05, zorder=0)

ax.errorbar(
    df_plot["FA_Pred"],
    df_plot["FA_Obs"],
    yerr=df_plot["FA_Obs_Std"],
    fmt="none",
    ecolor="black",
    elinewidth=1.0,
    capsize=3,
    alpha=0.9,
    zorder=2,
)

ax.scatter(
    df_plot["FA_Pred"],
    df_plot["FA_Obs"],
    s=150,
    color="#7570b3",
    alpha=0.85,
    edgecolors="white",
    linewidth=1.0,
    zorder=3,
)

texts = []
for _, row in df_plot.iterrows():
    texts.append(
        ax.text(
            row["FA_Pred"],
            row["FA_Obs"],
            row["city"],
            fontsize=12,
            color="black",
            fontfamily="Arial",
        )
    )

adjust_text(
    texts,
    ax=ax,
    arrowprops=dict(arrowstyle="-", color="black", lw=0.5, alpha=0.8),
    expand_points=(1.2, 1.2),
)

ax.set_xlabel("Predicted asymmetry ($FA_{\\mathrm{Gravity}}$)", fontsize=14, labelpad=10)
ax.set_ylabel("Observed asymmetry ($FA_{\\mathrm{Real}}$)", fontsize=14, labelpad=10)
ax.set_xlim(limit_min, limit_max)
ax.set_ylim(limit_min, limit_max)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.text(
    limit_max - 0.45,
    limit_max - 0.35,
    "$FA_{\\mathrm{Real}} > FA_{\\mathrm{Gravity}}$",
    fontsize=14,
    color="#e7298a",
    alpha=0.7,
    ha="right",
    va="top",
)

png_path = os.path.join(output_folder, "Fig3C.png")
svg_path = os.path.join(output_folder, "Fig3C.svg")
plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.savefig(svg_path, format="svg", bbox_inches="tight")

print(f"Figure saved:\nPNG: {png_path}")
plt.show()

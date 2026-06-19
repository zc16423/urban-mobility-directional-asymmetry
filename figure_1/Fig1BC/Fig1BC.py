# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 20:37:54 2026

@author: Dell
"""

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "Fig1BC.csv")
OUTPUT_DIR = SCRIPT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

REQUIRED_COLUMNS = {
    "city",
    "origin_geoid",
    "pct_Prs_Blw_Pov_Lev_ACS_15_19",
    "pct_NH_White_alone_ACS_15_19",
    "weighted_avg_asymmetry",
    "net_flow",
}

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.unicode_minus": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "axes.linewidth": 1.2,
    "legend.frameon": False,
})


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def calculate_binned_stats(df, x_col, y_col):
    sub_df = df[[x_col, y_col]].dropna()
    x_data = sub_df[x_col]
    y_data = sub_df[y_col]

    q_low, q_high = x_data.quantile(0.01), x_data.quantile(0.99)
    bins = np.linspace(q_low, q_high, 15)

    bin_centers_ref = (bins[:-1] + bins[1:]) / 2
    bin_indices = np.digitize(x_data, bins)

    bin_medians = []
    bin_errors = []
    valid_centers = []

    for i in range(1, len(bins)):
        mask = bin_indices == i
        if np.sum(mask) > 100:
            vals = y_data[mask]
            vals = vals[(vals > vals.quantile(0.025)) & (vals < vals.quantile(0.975))]

            if len(vals) > 20:
                bin_medians.append(vals.median())
                bin_errors.append(vals.std() / np.sqrt(len(vals)))
                valid_centers.append(bin_centers_ref[i - 1])

    return np.array(valid_centers), np.array(bin_medians), np.array(bin_errors)


def plot_binned_trend(df, x_col, y_col, x_label, color, save_name):
    print(f"Processing: {x_label} ...")

    clean_data = df[[x_col, y_col]].dropna()
    centers, medians, errors = calculate_binned_stats(df, x_col, y_col)

    if len(centers) == 0:
        print(f"WARNING: insufficient data for {x_label}.")
        return

    r, p_value = stats.spearmanr(clean_data[x_col], clean_data[y_col])
    p_text = "p < 0.001" if p_value < 0.001 else f"p = {p_value:.3f}"
    stats_text = f"Spearman $r = {r:.2f}$\n{p_text}\n$N = {len(clean_data):,}$"

    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)

    ax.fill_between(
        centers,
        medians - errors,
        medians + errors,
        color=color,
        alpha=0.15,
        edgecolor="none",
        zorder=1,
    )

    ax.plot(centers, medians, color=color, linewidth=1.5, linestyle="-", alpha=0.6, zorder=2)

    ax.errorbar(
        centers,
        medians,
        yerr=errors,
        fmt="o",
        color=color,
        ecolor=color,
        elinewidth=1.5,
        capsize=3,
        markersize=8,
        markeredgecolor="white",
        markeredgewidth=1.2,
        zorder=3,
        label="Observed data (median $\\pm$ SEM)",
    )

    ax.text(
        0.05,
        0.95,
        stats_text,
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment="top",
        horizontalalignment="left",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9, edgecolor="#CCCCCC"),
    )

    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel("Flow asymmetry ($FA$)", fontsize=16)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f"{x:.0f}%"))

    sns.despine()
    ax.legend(fontsize=14, loc="lower right", frameon=False)

    plt.tight_layout()

    save_path_png = os.path.join(OUTPUT_DIR, f"{save_name}.png")
    save_path_svg = os.path.join(OUTPUT_DIR, f"{save_name}.svg")
    plt.savefig(save_path_png, bbox_inches="tight")
    plt.savefig(save_path_svg, bbox_inches="tight")
    print(f"  Saved: {save_path_png}")
    plt.close()


if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        print("Reading data...")
        df = pd.read_csv(INPUT_FILE)
        validate_columns(df, REQUIRED_COLUMNS, INPUT_FILE)

        plot_binned_trend(
            df,
            x_col="pct_NH_White_alone_ACS_15_19",
            y_col="weighted_avg_asymmetry",
            x_label="White population percentage",
            color="#4E79A7",
            save_name="Fig1C",
        )

        plot_binned_trend(
            df,
            x_col="pct_Prs_Blw_Pov_Lev_ACS_15_19",
            y_col="weighted_avg_asymmetry",
            x_label="Population below poverty level",
            color="#D35450",
            save_name="Fig1B",
        )
        print("Done.")
    else:
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

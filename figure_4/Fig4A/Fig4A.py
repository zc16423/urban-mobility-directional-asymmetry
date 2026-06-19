# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 11:03:24 2026

@author: Dell
"""

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = {
    "Gravity Model": os.path.join(SCRIPT_DIR, "Fig4A_real_gravity.csv"),
    "IOM Model": os.path.join(SCRIPT_DIR, "Fig4A_real_iom.csv"),
    "Choice-IOM Model ($\\theta = 0.5$)": os.path.join(SCRIPT_DIR, "Fig4A_real_choice.csv"),
}

OUTPUT_DIR = SCRIPT_DIR

FLOW_LPW_TO_HPM = "LPW_to_HPM"
FLOW_HPM_TO_LPW = "HPM_to_LPW"
FLOW_LABELS = [FLOW_LPW_TO_HPM, FLOW_HPM_TO_LPW]
FLOW_DISPLAY = {
    FLOW_LPW_TO_HPM: "LPW to HPM",
    FLOW_HPM_TO_LPW: "HPM to LPW",
}
PALETTE = {
    FLOW_LPW_TO_HPM: "#4E79A7",
    FLOW_HPM_TO_LPW: "#D35450",
}

FIG_SIZE = (10, 7)
REQUIRED_COLUMNS = {
    "city",
    "flow_type",
    "Sum_Observed_Flow",
    "Sum_Predicted_Flow",
    "Realization_Ratio_R",
}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def load_and_prepare_data(file_map):
    all_dfs = []
    for model_name, path in file_map.items():
        df = pd.read_csv(path)
        validate_columns(df, REQUIRED_COLUMNS, path)
        df = df.copy()
        df["Model"] = model_name
        df["flow_type"] = df["flow_type"].astype(str).str.strip()
        df["Realization_Ratio_R"] = pd.to_numeric(df["Realization_Ratio_R"], errors="coerce")
        df = df[df["flow_type"].isin(FLOW_LABELS)]
        all_dfs.append(df)

    if not all_dfs:
        return None

    combined_df = pd.concat(all_dfs, ignore_index=True)
    model_order = list(file_map.keys())
    combined_df["Model"] = pd.Categorical(combined_df["Model"], categories=model_order, ordered=True)
    combined_df["flow_type"] = pd.Categorical(combined_df["flow_type"], categories=FLOW_LABELS, ordered=True)
    return combined_df


def perform_statistical_tests(df):
    p_values = {}
    for model_name in df["Model"].unique():
        model_data = df[df["Model"] == model_name]
        r_red = model_data[model_data["flow_type"] == FLOW_HPM_TO_LPW]["Realization_Ratio_R"]
        r_blue = model_data[model_data["flow_type"] == FLOW_LPW_TO_HPM]["Realization_Ratio_R"]
        stat, p = wilcoxon(r_blue, r_red)
        p_values[model_name] = p
    return p_values


def p_value_to_stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


def create_and_save_plot(df, p_values):
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial"]
    plt.rcParams["xtick.direction"] = "out"
    plt.rcParams["ytick.direction"] = "out"

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=300)

    box_plot = sns.boxplot(
        data=df,
        x="Model",
        y="Realization_Ratio_R",
        hue="flow_type",
        palette=PALETTE,
        showfliers=False,
        width=0.55,
        ax=ax,
        hue_order=FLOW_LABELS,
        linewidth=1.5,
        zorder=10,
    )

    for patch in box_plot.patches:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.5))
        patch.set_edgecolor((r, g, b, 1.0))

    sns.stripplot(
        data=df,
        x="Model",
        y="Realization_Ratio_R",
        hue="flow_type",
        palette=PALETTE,
        dodge=True,
        jitter=True,
        size=6,
        edgecolor="white",
        linewidth=0.8,
        alpha=0.85,
        ax=ax,
        hue_order=FLOW_LABELS,
        zorder=20,
    )

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(ticker.NullLocator())

    global_max_y = df["Realization_Ratio_R"].max()
    max_plot_limit = global_max_y

    for i, model_name in enumerate(df["Model"].cat.categories):
        p_star = p_value_to_stars(p_values[model_name])
        model_data = df[df["Model"] == model_name]
        current_max = model_data["Realization_Ratio_R"].max()
        text_y_pos = current_max * 1.05

        ax.text(i, text_y_pos, p_star, ha="center", va="center", fontsize=20, color="black", zorder=30)

        if text_y_pos > max_plot_limit:
            max_plot_limit = text_y_pos

    ax.set_ylim(bottom=df["Realization_Ratio_R"].min() * 0.5, top=max_plot_limit * 1.05)

    ax.axhline(1.0, ls="--", color="#444444", lw=1.5, alpha=0.8, zorder=5)
    ax.text(0.02, 0.35, "$R$ = 1.0", transform=ax.transAxes, fontsize=14, ha="left", va="bottom")

    ax.set_xlabel("", fontsize=16)
    ax.set_ylabel("Realization ratio ($R$)", fontsize=16, labelpad=10)

    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(1.5)
        ax.spines[spine].set_color("black")

    sns.despine(top=True, right=True)

    ax.tick_params(axis="x", labelsize=14, width=1.5, length=6)
    ax.tick_params(axis="y", which="major", labelsize=14, width=1.5, length=6)
    ax.tick_params(axis="y", which="minor", width=1.0, length=3)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[:2],
        [FLOW_DISPLAY[label] for label in FLOW_LABELS],
        fontsize=14,
        loc="upper right",
        frameon=False,
        bbox_to_anchor=(1, 1),
    )

    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    png_path = os.path.join(OUTPUT_DIR, "Fig4A.png")
    svg_path = os.path.join(OUTPUT_DIR, "Fig4A.svg")

    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(svg_path, format="svg", bbox_inches="tight")

    print(f"Figure saved:\n  {png_path}\n  {svg_path}")
    plt.show()


if __name__ == "__main__":
    main_df = load_and_prepare_data(DATA_FILES)
    if main_df is not None:
        p_vals = perform_statistical_tests(main_df)
        create_and_save_plot(main_df, p_vals)

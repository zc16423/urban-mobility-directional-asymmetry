# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:40:25 2026

@author: Dell
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INTERMEDIATE_DIR = SCRIPT_DIR
OUTPUT_IMG_DIR = SCRIPT_DIR
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

FEATURE_IMPORTANCE_COLUMNS = {
    "Feature",
    "MDI_Importance",
    "Permutation_Importance_Mean",
    "Permutation_Importance_SD",
}

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.unicode_minus": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "axes.linewidth": 1.2,
    "legend.frameon": False,
    "legend.fontsize": 14,
})


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


feature_importance_path = os.path.join(INTERMEDIATE_DIR, "Fig4B_feature_importance_results.csv")
feat_imp = pd.read_csv(feature_importance_path)
validate_columns(feat_imp, FEATURE_IMPORTANCE_COLUMNS, feature_importance_path)


def plot_feature_importance_advanced(feat_imp_df, save_name):
    print("Plotting Panel B feature importance...")

    label_map = {
        "Delta_Race_White": "White population rate gap",
        "Delta_Poverty": "Poverty rate gap",
        "Delta_Edu_College": "College rate gap",
        "Delta_Age_65plus": "Age 65plus rate gap",
        "Delta_Housing_Owner": "Owner-Occupied housing rate gap",
        "Delta_POI_Count": "POI count difference",
        "Delta_Job_Density": "Gross employment density difference",
        "Delta_Pop_Density": "Gross population density difference",
        "Log_Distance": "Distance difference",
    }

    feat_imp_df = feat_imp_df.copy()
    feat_imp_df["Label"] = feat_imp_df["Feature"].map(lambda x: label_map.get(x, x))
    feat_imp_df = feat_imp_df.sort_values(by="MDI_Importance", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    palette = sns.color_palette("Spectral", n_colors=len(feat_imp_df))

    bars = sns.barplot(
        data=feat_imp_df,
        x="MDI_Importance",
        y="Label",
        palette=palette,
        edgecolor="black",
        linewidth=0.8,
        ax=ax,
    )

    for container in bars.containers:
        labels = [f"{v.get_width():.3f}" for v in container]
        ax.bar_label(
            container,
            labels=labels,
            label_type="edge",
            padding=8,
            fontsize=14,
            color="black",
        )

    ax.set_xlabel("Relative feature importance", fontsize=16)
    ax.set_ylabel("", fontsize=16)
    ax.set_xlim(0, feat_imp_df["MDI_Importance"].max() * 1.15)

    sns.despine(top=True, right=True)
    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_IMG_DIR, f"{save_name}.png"), bbox_inches="tight")
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, f"{save_name}.svg"), bbox_inches="tight")
    print(f"Panel B saved as {save_name}")


plot_feature_importance_advanced(feat_imp, "Fig4B")

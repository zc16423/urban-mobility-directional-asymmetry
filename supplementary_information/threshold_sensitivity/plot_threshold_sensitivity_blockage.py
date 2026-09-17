import matplotlib
matplotlib.use('Agg')
# -*- coding: utf-8 -*-
"""
Plotting Script: Threshold Sensitivity Analysis - Network Blockage Rate
Reproduces: Supplementary Figure S4 (Network Blockage Rate Sensitivity)
Data Source: threshold_sensitivity_blockage_data.csv
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure standard console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def plot_threshold_sensitivity_blockage():
    # Base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "threshold_sensitivity_blockage_data.csv")
    out_png = os.path.join(script_dir, "threshold_sensitivity_blockage.png")

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    df = pd.read_csv(data_file)

    # Global styling parameters
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial'],
        'font.size': 11,
        'axes.linewidth': 1.2,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.width': 1.2,
        'ytick.major.width': 1.2,
        'figure.dpi': 300
    })

    COLOR_H2L = '#D35450'  # Warm Red for HPM -> LPW
    COLOR_L2H = '#4E79A7'  # Slate Blue for LPW -> HPM

    models = ["Gravity", "IOM", "Choice_IOM"]
    model_titles = {
        "Gravity": "Gravity Model",
        "IOM": "Intervening Opportunities (IOM)",
        "Choice_IOM": "Choice-IOM ($\u03c4 = 0.5$)"
    }

    pov_thresholds = [20, 25, 30, 35, 40]
    comp_thresholds = [40, 45, 50, 55, 60]

    # Create figure with 2 rows x 3 columns
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.8), dpi=300, sharey=False)

    # -------------------------------------------------------------
    # Panel A: Poverty Threshold Sensitivity (Top Row)
    # -------------------------------------------------------------
    for col_idx, model in enumerate(models):
        ax = axes[0, col_idx]
        sub = df[(df["sensitivity_group"] == "poverty_threshold") & (df["model"] == model)]

        # Baseline vertical dashed line at 30%
        ax.axvline(30, color='#555555', linestyle='--', linewidth=1.2, alpha=0.8, 
                   label='Baseline (30%)' if col_idx == 0 else "")

        # Direction curves
        for d, color, marker, label in [("HPM_to_LPW", COLOR_H2L, 'o', "HPM \u2192 LPW"), 
                                        ("LPW_to_HPM", COLOR_L2H, 's', "LPW \u2192 HPM")]:
            dsub = sub[sub["direction"] == d].sort_values("poverty_threshold")
            ax.errorbar(
                dsub["poverty_threshold"], dsub["mean_blockage_pct"], yerr=dsub["sem_blockage_pct"],
                color=color, marker=marker, markersize=6, linewidth=2.0,
                capsize=3, capthick=1.2, label=label if col_idx == 0 else ""
            )

        ax.set_title(model_titles[model], fontsize=12, pad=8)
        ax.set_xlabel("Poverty Threshold (%)", fontsize=11, labelpad=6)
        if col_idx == 0:
            ax.set_ylabel("Blockage Rate (%)\nPanel A: Poverty Sensitivity", fontsize=11)
        
        ax.set_xticks(pov_thresholds)
        ax.set_xticklabels([f"{p}%" for p in pov_thresholds])
        ax.set_ylim(20, 65)
        ax.set_yticks([20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
        ax.grid(True, linestyle=':', alpha=0.4)

        if col_idx == 0:
            ax.legend(frameon=True, framealpha=0.9, edgecolor='#C0C0C0', loc='upper left', fontsize=10)

    # -------------------------------------------------------------
    # Panel B: Composition Threshold Sensitivity (Bottom Row)
    # -------------------------------------------------------------
    for col_idx, model in enumerate(models):
        ax = axes[1, col_idx]
        sub = df[(df["sensitivity_group"] == "composition_threshold") & (df["model"] == model)]

        # Baseline vertical dashed line at 50%
        ax.axvline(50, color='#555555', linestyle='--', linewidth=1.2, alpha=0.8, 
                   label='Baseline (50%)' if col_idx == 0 else "")

        # Direction curves
        for d, color, marker, label in [("HPM_to_LPW", COLOR_H2L, 'o', "HPM \u2192 LPW"), 
                                        ("LPW_to_HPM", COLOR_L2H, 's', "LPW \u2192 HPM")]:
            dsub = sub[sub["direction"] == d].sort_values("composition_threshold")
            ax.errorbar(
                dsub["composition_threshold"], dsub["mean_blockage_pct"], yerr=dsub["sem_blockage_pct"],
                color=color, marker=marker, markersize=6, linewidth=2.0,
                capsize=3, capthick=1.2, label=label if col_idx == 0 else ""
            )

        ax.set_title(model_titles[model], fontsize=12, pad=8)
        ax.set_xlabel("Composition Threshold (%)", fontsize=11, labelpad=6)
        if col_idx == 0:
            ax.set_ylabel("Blockage Rate (%)\nPanel B: Composition Sensitivity", fontsize=11)

        ax.set_xticks(comp_thresholds)
        ax.set_xticklabels([f"{c}%" for c in comp_thresholds])
        ax.set_ylim(20, 65)
        ax.set_yticks([20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
        ax.grid(True, linestyle=':', alpha=0.4)

        if col_idx == 0:
            ax.legend(frameon=True, framealpha=0.9, edgecolor='#C0C0C0', loc='upper left', fontsize=10)

    plt.tight_layout()
    plt.savefig(out_png.replace(".png", ".svg"), format="svg", bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {out_png}")

if __name__ == "__main__":
    plot_threshold_sensitivity_blockage()

import matplotlib
matplotlib.use('Agg')
# -*- coding: utf-8 -*-
"""
Plotting Script: Threshold Sensitivity Analysis - Flow Asymmetry (FA)
Reproduces: Supplementary Figure S7/S8 (Flow Asymmetry Sensitivity)
Data Source: threshold_sensitivity_FA_data.csv
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure standard console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def plot_threshold_sensitivity_FA():
    # Base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "threshold_sensitivity_FA_data.csv")
    out_png = os.path.join(script_dir, "threshold_sensitivity_FA.png")

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    df = pd.read_csv(data_file)

    # 16 metropolitan areas
    city_cols = [
        "Los Angeles", "San Diego", "Washington, D.C", "Miami", "Atlanta", 
        "Chicago", "Boston", "Detroit", "New York", "Pittsburgh", 
        "Philadelphia", "Dallas", "San Francisco", "Houston", "Phoenix", "St. Louis"
    ]

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

    pov_thresholds = [20, 25, 30, 35, 40]
    comp_thresholds = [40, 45, 50, 55, 60]

    # Create figure with 1 row x 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

    # -------------------------------------------------------------
    # Panel A: Poverty Threshold Sensitivity
    # -------------------------------------------------------------
    sub_pov = df[df["sensitivity_group"] == "poverty_threshold"].sort_values("poverty_threshold")

    # 1. Plot individual 16 city trajectories as light gray lines
    for city in city_cols:
        ax1.plot(sub_pov["poverty_threshold"], sub_pov[city], 
                 color='#D3D3D3', alpha=0.6, linewidth=1.0)

    # 2. Baseline vertical dashed line at 30%
    ax1.axvline(30, color='#4A4A4A', linestyle='--', linewidth=1.2, alpha=0.8, 
                label='Baseline (30%)')

    # 3. 16-city mean ± SEM curve
    ax1.errorbar(
        sub_pov["poverty_threshold"], sub_pov["mean_FA"], yerr=sub_pov["sem_FA"],
        color='#2CA02C', marker='o', markersize=7, linewidth=2.5,
        capsize=4, capthick=1.5, label='16-City Mean FA (\u00b1 SEM)'
    )

    ax1.set_title("Panel A: Poverty Threshold vs. Flow Asymmetry", fontsize=12, pad=10)
    ax1.set_xlabel("Poverty Threshold (%)", fontsize=11)
    ax1.set_ylabel("Flow Asymmetry (FA)", fontsize=11)
    ax1.set_xticks(pov_thresholds)
    ax1.set_xticklabels([f"{p}%" for p in pov_thresholds])
    ax1.set_ylim(0.4, 0.9)
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper left', frameon=True, framealpha=0.9, edgecolor='#C0C0C0', fontsize=10)

    # -------------------------------------------------------------
    # Panel B: Composition Threshold Sensitivity
    # -------------------------------------------------------------
    sub_comp = df[df["sensitivity_group"] == "composition_threshold"].sort_values("composition_threshold")

    # 1. Plot individual 16 city trajectories as light gray lines
    for city in city_cols:
        ax2.plot(sub_comp["composition_threshold"], sub_comp[city], 
                 color='#D3D3D3', alpha=0.6, linewidth=1.0)

    # 2. Baseline vertical dashed line at 50%
    ax2.axvline(50, color='#4A4A4A', linestyle='--', linewidth=1.2, alpha=0.8, 
                label='Baseline (50%)')

    # 3. 16-city mean ± SEM curve
    ax2.errorbar(
        sub_comp["composition_threshold"], sub_comp["mean_FA"], yerr=sub_comp["sem_FA"],
        color='#1F77B4', marker='s', markersize=7, linewidth=2.5,
        capsize=4, capthick=1.5, label='16-City Mean FA (\u00b1 SEM)'
    )

    ax2.set_title("Panel B: Composition Threshold vs. Flow Asymmetry", fontsize=12, pad=10)
    ax2.set_xlabel("Composition Threshold (%)", fontsize=11)
    ax2.set_ylabel("Flow Asymmetry (FA)", fontsize=11)
    ax2.set_xticks(comp_thresholds)
    ax2.set_xticklabels([f"{c}%" for c in comp_thresholds])
    ax2.set_ylim(0.4, 0.9)
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.legend(loc='upper left', frameon=True, framealpha=0.9, edgecolor='#C0C0C0', fontsize=10)

    plt.tight_layout()
    plt.savefig(out_png.replace(".png", ".svg"), format="svg", bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {out_png}")

if __name__ == "__main__":
    plot_threshold_sensitivity_FA()

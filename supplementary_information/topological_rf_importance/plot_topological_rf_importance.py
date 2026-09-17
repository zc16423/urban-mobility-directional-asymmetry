"""
Plotting Script: Feature Importance for Topological Baselines (IOM & Choice-IOM)
Reproduces: Fig S11 (IOM RF Importance) and Fig S12 (Choice-IOM RF Importance)
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'axes.unicode_minus': False,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'axes.linewidth': 1.2,
})

LABEL_MAP = {
    "Delta_Race_White": "White population rate gap",
    "Delta_Poverty": "Poverty rate gap",
    "Delta_Job_Density": "Job density gap",
    "Delta_Pop_Density": "Population density gap",
    "Distance_Miles": "Physical distance",
    "Delta_Edu_College": "College rate gap",
    "Delta_Housing_Owner": "Owner-occupied housing gap",
    "Delta_POI_Count": "POI count gap",
    "Delta_Age_65plus": "Age 65+ gap",
    "Delta_Median_HHD_Income": "Median household income gap"
}


def plot_importance(csv_filename, title, out_prefix, bar_color):
    csv_path = os.path.join(SCRIPT_DIR, csv_filename)
    if not os.path.exists(csv_path):
        print(f"Missing {csv_path}")
        return
    df = pd.read_csv(csv_path)

    val_col = 'Mean_Delta_MSE' if 'Mean_Delta_MSE' in df.columns else df.columns[2]
    df['Label'] = df['Feature'].map(lambda x: LABEL_MAP.get(x, x))
    df = df.sort_values(by=val_col, ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    y = np.arange(len(df))

    ax.barh(y, df[val_col], color=bar_color, edgecolor='none', height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(df['Label'], fontsize=11)
    ax.set_xlabel(r'Predictive Importance ($\Delta\mathrm{MSE}$)', fontsize=12)
    ax.set_title(title, fontsize=13, pad=12)
    ax.grid(axis='x', linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, f"{out_prefix}.svg"), format='svg', bbox_inches='tight')
    plt.savefig(os.path.join(SCRIPT_DIR, f"{out_prefix}.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_prefix}.svg and {out_prefix}.png")


if __name__ == '__main__':
    plot_importance("iom_feature_importance_results.csv",
                    "Intervening Opportunities Model: Predictor Importance",
                    "FigS11_IOM_Feature_Importance", "#d95f02")
    plot_importance("choice_iom_feature_importance_results.csv",
                    r"Choice-IOM ($\tau = 0.5$): Predictor Importance",
                    "FigS12_Choice_IOM_Feature_Importance", "#7570b3")

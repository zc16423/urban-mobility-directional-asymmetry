"""
Plotting Script: Metropolitan Holdout Performance & Permutation Importance Comparison
Reproduces: metropolitan_holdout_performance.svg and permutation_importance_comparison.svg
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'dejavusans',
    'axes.unicode_minus': False,
})

COLOR_GRAVITY = '#2b5c8f'
COLOR_INTERVENING = '#d95f02'
COLOR_PATH = '#7570b3'

FEATURE_NAME_MAPPING = {
    'Delta_Race_White': 'White population rate gap',
    'Delta_Poverty': 'Poverty rate gap',
    'Delta_Edu_College': 'College rate gap',
    'Delta_Age_65plus': 'Age 65plus rate gap',
    'Delta_Housing_Owner': 'Owner occupied housing gap',
    'Delta_Job_Density': 'Job density gap',
    'Delta_Pop_Density': 'Population density gap',
    'Delta_Median_HHD_Income': 'Median household income gap',
    'Distance_Miles': 'Physical distance',
    'Delta_POI_Count': 'POI count gap'
}


def plot_metropolitan_holdout():
    csv_path = os.path.join(SCRIPT_DIR, "plot_data_metropolitan_holdout.csv")
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
    df = pd.read_csv(csv_path)

    cities = df['Metropolitan_Area'].tolist()
    y = np.arange(len(cities))
    bar_height = 0.25

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    ax.barh(y + bar_height, df['Gravity_R2'], height=bar_height,
            color=COLOR_GRAVITY, label='Gravity Model', edgecolor='none')
    ax.barh(y, df['Intervening_R2'], height=bar_height,
            color=COLOR_INTERVENING, label='Intervening Opportunities Model', edgecolor='none')
    ax.barh(y - bar_height, df['Path_R2'], height=bar_height,
            color=COLOR_PATH, label=r'Choice-IOM ($\tau = 0.5$)', edgecolor='none')

    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(cities, fontsize=10)
    ax.invert_yaxis()

    ax.set_xlabel(r'Held-out $R^2$', fontsize=12, labelpad=8)
    ax.set_title('Cross-Metropolitan Generalization (16 LOMAO Folds)', fontsize=13, pad=12)
    ax.legend(loc='lower right', frameon=True, framealpha=0.9, fontsize=10)
    ax.grid(axis='x', linestyle=':', alpha=0.5)

    plt.tight_layout()
    out_svg = os.path.join(OUTPUT_DIR, "metropolitan_holdout_performance.svg")
    out_png = os.path.join(OUTPUT_DIR, "metropolitan_holdout_performance.png")
    plt.savefig(out_svg, format='svg', bbox_inches='tight')
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_svg} and {out_png}")


def plot_permutation_importance():
    csv_path = os.path.join(SCRIPT_DIR, "plot_data_permutation_importance.csv")
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
    df = pd.read_csv(csv_path)

    # Pivot to get features as rows and models as columns
    df_grav = df[df['Model'] == 'Gravity'].set_index('Feature')
    df_iom = df[df['Model'].str.contains('Intervening')].set_index('Feature')
    df_path = df[df['Model'].str.contains('Path|Choice')].set_index('Feature')

    # Sort by Path importance
    features = df_path['Mean_Delta_MSE'].sort_values(ascending=True).index.tolist()
    labels = [FEATURE_NAME_MAPPING.get(f, f) for f in features]

    y = np.arange(len(features))
    bar_height = 0.25

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    grav_vals = [df_grav.loc[f, 'Mean_Delta_MSE'] if f in df_grav.index else 0 for f in features]
    grav_errs = [df_grav.loc[f, 'SD_Delta_MSE'] if f in df_grav.index else 0 for f in features]

    iom_vals = [df_iom.loc[f, 'Mean_Delta_MSE'] if f in df_iom.index else 0 for f in features]
    iom_errs = [df_iom.loc[f, 'SD_Delta_MSE'] if f in df_iom.index else 0 for f in features]

    path_vals = [df_path.loc[f, 'Mean_Delta_MSE'] if f in df_path.index else 0 for f in features]
    path_errs = [df_path.loc[f, 'SD_Delta_MSE'] if f in df_path.index else 0 for f in features]

    ax.barh(y + bar_height, grav_vals, height=bar_height, xerr=grav_errs,
            color=COLOR_GRAVITY, label='Gravity Model', edgecolor='none', capsize=3)
    ax.barh(y, iom_vals, height=bar_height, xerr=iom_errs,
            color=COLOR_INTERVENING, label='Intervening Opportunities Model', edgecolor='none', capsize=3)
    ax.barh(y - bar_height, path_vals, height=bar_height, xerr=path_errs,
            color=COLOR_PATH, label=r'Choice-IOM ($\tau = 0.5$)', edgecolor='none', capsize=3)

    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)

    ax.set_xlabel(r'Increase in Held-out MSE ($\Delta\mathrm{MSE}$)', fontsize=12, labelpad=8)
    ax.set_title('Cross-Metropolitan Permutation Feature Importance', fontsize=13, pad=12)
    ax.legend(loc='lower right', frameon=True, framealpha=0.9, fontsize=10)
    ax.grid(axis='x', linestyle=':', alpha=0.5)

    plt.tight_layout()
    out_svg = os.path.join(OUTPUT_DIR, "permutation_importance_comparison.svg")
    out_png = os.path.join(OUTPUT_DIR, "permutation_importance_comparison.png")
    plt.savefig(out_svg, format='svg', bbox_inches='tight')
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_svg} and {out_png}")


if __name__ == '__main__':
    plot_metropolitan_holdout()
    plot_permutation_importance()

"""
Plotting Script: Distribution of HPM and LPW CBGs across 16 Metropolitan Areas
Reproduces: Supplementary Figure S1
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(SCRIPT_DIR, "FigS1_cbg_demographic_counts.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Missing {csv_path}")

df = pd.read_csv(csv_path)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'axes.unicode_minus': False,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
})

df_lpw = df[df['Category_Label'] == 'LPW'].set_index('City')
df_hpm = df[df['Category_Label'] == 'HPM'].set_index('City')

cities = df_lpw.sort_values(by='Percentage_Val', ascending=False).index.tolist()

lpw_pct = [df_lpw.loc[c, 'Percentage_Val'] if c in df_lpw.index else 0 for c in cities]
hpm_pct = [df_hpm.loc[c, 'Percentage_Val'] if c in df_hpm.index else 0 for c in cities]

lpw_cnt = [int(df_lpw.loc[c, 'Count']) if c in df_lpw.index else 0 for c in cities]
hpm_cnt = [int(df_hpm.loc[c, 'Count']) if c in df_hpm.index else 0 for c in cities]

x = np.arange(len(cities))
width = 0.38

fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

rects1 = ax.bar(x - width/2, lpw_pct, width, label='Low-Poverty White (LPW)', color='#3684BE', edgecolor='black', linewidth=0.5)
rects2 = ax.bar(x + width/2, hpm_pct, width, label='High-Poverty Minority (HPM)', color='#EE4436', edgecolor='black', linewidth=0.5)

for rect, cnt in zip(rects1, lpw_cnt):
    height = rect.get_height()
    ax.annotate(f'{cnt}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

for rect, cnt in zip(rects2, hpm_cnt):
    height = rect.get_height()
    ax.annotate(f'{cnt}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Percentage of Metropolitan CBGs (%)', fontsize=12)
ax.set_title('Distribution of HPM and LPW CBGs Across 16 Metropolitan Areas', fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(cities, rotation=45, ha='right', fontsize=11)
ax.legend(frameon=True, framealpha=0.9, fontsize=11)
ax.grid(axis='y', linestyle=':', alpha=0.5)
ax.set_ylim(0, max(max(lpw_pct), max(hpm_pct)) * 1.15)

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "FigS1.svg"), format='svg', bbox_inches='tight')
plt.savefig(os.path.join(SCRIPT_DIR, "FigS1.png"), dpi=300, bbox_inches='tight')
plt.close()
print("Saved FigS1.svg and FigS1.png")

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch


plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": 16,
    "axes.unicode_minus": False,
})

sns.set_style("whitegrid")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(SCRIPT_DIR, "Fig1D.csv")
output_dir = SCRIPT_DIR
os.makedirs(output_dir, exist_ok=True)

TARGET_CITY = "Boston"
FLOW_LPW_TO_HPM = "LPW_to_HPM"
FLOW_HPM_TO_LPW = "HPM_to_LPW"
OTHER_FLOW = "Other"

REQUIRED_COLUMNS = {"city", "flow_type", "ratio"}

label_mapping = {
    FLOW_LPW_TO_HPM: "LPW to HPM",
    FLOW_HPM_TO_LPW: "HPM to LPW",
    OTHER_FLOW: "Other flow",
}

highlight_colors = {
    FLOW_LPW_TO_HPM: "#3684BE",
    FLOW_HPM_TO_LPW: "#EE4436",
    OTHER_FLOW: "#e0e0e0",
}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


fig, ax = plt.subplots(1, 1, figsize=(10, 10))
radius = 1.0

try:
    df_all = pd.read_csv(input_file_path)
    validate_columns(df_all, REQUIRED_COLUMNS, input_file_path)

    df_all["city"] = df_all["city"].astype(str).str.strip()
    df_all["flow_type"] = df_all["flow_type"].astype(str).str.strip()
    df_all["ratio"] = pd.to_numeric(df_all["ratio"], errors="coerce")

    print("Data file loaded successfully.")

except Exception as exc:
    print(f"Failed to read data file: {exc}")
    df_all = pd.DataFrame()

if df_all.empty:
    has_data = False
else:
    df_city = df_all[df_all["city"] == TARGET_CITY].copy()
    has_data = not df_city.empty

if not has_data:
    ax.text(
        0.5,
        0.5,
        f"No data found\n{TARGET_CITY}",
        ha="center",
        va="center",
        fontsize=16,
    )
    ax.set_title(TARGET_CITY, fontsize=16)
    ax.axis("off")
else:
    try:
        ratio_lpw_to_hpm = df_city[df_city["flow_type"] == FLOW_LPW_TO_HPM]["ratio"].sum()
        ratio_hpm_to_lpw = df_city[df_city["flow_type"] == FLOW_HPM_TO_LPW]["ratio"].sum()
        ratio_other = max(0, 1.0 - (ratio_lpw_to_hpm + ratio_hpm_to_lpw))

        plot_data = [
            {"label": FLOW_LPW_TO_HPM, "size": ratio_lpw_to_hpm},
            {"label": FLOW_HPM_TO_LPW, "size": ratio_hpm_to_lpw},
            {"label": OTHER_FLOW, "size": ratio_other},
        ]

        df_plot = pd.DataFrame(plot_data)
        df_plot = df_plot[df_plot["size"] > 0]

        labels = [label_mapping[x] for x in df_plot["label"]]
        sizes = df_plot["size"]
        colors_plot = [highlight_colors[x] for x in df_plot["label"]]

        explode = [
            0.1 if x in [FLOW_LPW_TO_HPM, FLOW_HPM_TO_LPW] else 0
            for x in df_plot["label"]
        ]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors_plot,
            startangle=90,
            wedgeprops={
                "edgecolor": "white",
                "linewidth": 1.5,
            },
            explode=explode,
            pctdistance=0.85,
            labeldistance=1.1,
            radius=radius,
            textprops={"fontsize": 16},
            counterclock=False,
        )

        if len(texts) >= 2:
            for text, label in zip(texts, labels):
                pos = list(text.get_position())
                if label == label_mapping[FLOW_LPW_TO_HPM]:
                    text.set_position((pos[0] - 0.50, pos[1] - 0.40))
                elif label == label_mapping[FLOW_HPM_TO_LPW]:
                    text.set_position((pos[0] + 0.05, pos[1] - 0.45))

        centre_circle = plt.Circle((0, 0), 0.5, fc="white", ec="none")
        ax.add_artist(centre_circle)

        for text in texts:
            text.set_fontsize(16)
            text.set_color("black")

        for autotext in autotexts:
            autotext.set_fontsize(16)
            autotext.set_color("black")

        ax.set_title(TARGET_CITY, fontsize=16, pad=10, color="black")
        ax.set_aspect("equal")

    except Exception as exc:
        ax.text(
            0.5,
            0.5,
            f"{TARGET_CITY}\nError:\n{str(exc)[:20]}",
            ha="center",
            va="center",
            fontsize=16,
        )
        ax.axis("off")

plt.tight_layout()
plt.subplots_adjust(
    top=0.92,
    bottom=0.06,
    left=0.02,
    right=0.98,
)

legend_elements = [
    Patch(
        facecolor=highlight_colors[FLOW_LPW_TO_HPM],
        edgecolor="none",
        label="LPW to HPM",
    ),
    Patch(
        facecolor=highlight_colors[FLOW_HPM_TO_LPW],
        edgecolor="none",
        label="HPM to LPW",
    ),
    Patch(
        facecolor=highlight_colors[OTHER_FLOW],
        edgecolor="none",
        label="Other flow",
    ),
]

fig.legend(
    handles=legend_elements,
    loc="lower center",
    bbox_to_anchor=(0.5, 0.01),
    ncol=3,
    frameon=False,
    fontsize=20,
    handlelength=2.0,
    handleheight=1.0,
)

png_path = os.path.join(output_dir, "Fig1D.png")
svg_path = os.path.join(output_dir, "Fig1D.svg")

plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(svg_path, format="svg", bbox_inches="tight")

print(f"Images saved at: {png_path}")

plt.show()

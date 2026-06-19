import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter


# =========================
# 0. File configuration
# =========================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "fig4B_processed_data_all_R_ge_0.csv")
OUTPUT_IMG_DIR = os.path.join(SCRIPT_DIR, "images")
OUTPUT_DATA_DIR = os.path.join(SCRIPT_DIR, "Fig4CD_data")

os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

# =========================
# 1. Global plotting style
# =========================
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
    "legend.fontsize": 13,
})

# =========================
# 2. Parameters
# =========================
CITY_COL = "city"
TARGET_COL = "Realization_Ratio_R"

N_BINS = 10
X_Q_LOW = 0.025
X_Q_HIGH = 0.975

MIN_PATHS_PER_CITY_BIN = 50
MIN_CITIES_PER_BIN = 8

EXPECTED_ACTIVE_ROWS = 1388358
EXPECTED_CITY_COUNT = 16


# =========================
# 3. Load and clean data
# =========================
print("Step 1: Loading data...")

df = pd.read_csv(INPUT_FILE)

required_cols = [
    CITY_COL,
    TARGET_COL,
    "Delta_Race_White",
    "Delta_Pop_Density",
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

for col in required_cols:
    if col != CITY_COL:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fig. 4C/D use active LPW-to-HPM paths only: R > 0
df_active = df[df[TARGET_COL] > 0].copy()
df_active = df_active.dropna(
    subset=[CITY_COL, TARGET_COL, "Delta_Race_White", "Delta_Pop_Density"]
)

print(f"Total rows in input file: {len(df):,}")
print(f"Active rows with R > 0 after cleaning: {len(df_active):,}")
print(f"Number of cities: {df_active[CITY_COL].nunique()}")

if len(df_active) != EXPECTED_ACTIVE_ROWS:
    print(
        f"WARNING: active row count is {len(df_active):,}, "
        f"not expected {EXPECTED_ACTIVE_ROWS:,}. "
        "This may be due to missing values in Fig. 4C/D variables."
    )

if df_active[CITY_COL].nunique() != EXPECTED_CITY_COUNT:
    print(
        f"WARNING: city count is {df_active[CITY_COL].nunique()}, "
        f"not expected {EXPECTED_CITY_COUNT}."
    )


# =========================
# 4. City-equalized binned median
# =========================
def compute_city_equalized_binned_median(
    data,
    feature_col,
    target_col=TARGET_COL,
    city_col=CITY_COL,
    n_bins=N_BINS,
    x_q_low=X_Q_LOW,
    x_q_high=X_Q_HIGH,
    min_paths_per_city_bin=MIN_PATHS_PER_CITY_BIN,
    min_cities_per_bin=MIN_CITIES_PER_BIN,
):
    """
    Compute binned median R in two stages:
    1. Within each city and bin, compute the median realization ratio.
    2. Across cities, summarize city-level medians using median and IQR.

    This gives each city equal weight in the visualized relationship.
    """
    use_df = data[[city_col, feature_col, target_col]].dropna().copy()

    q_low = use_df[feature_col].quantile(x_q_low)
    q_high = use_df[feature_col].quantile(x_q_high)

    if pd.isna(q_low) or pd.isna(q_high):
        raise ValueError(f"{feature_col}: quantile range contains NaN.")

    if q_low == q_high:
        raise ValueError(f"{feature_col}: quantile range collapsed; cannot create bins.")

    bins = np.linspace(q_low, q_high, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    use_df = use_df[
        (use_df[feature_col] >= q_low)
        & (use_df[feature_col] <= q_high)
    ].copy()

    use_df["bin_id"] = pd.cut(
        use_df[feature_col],
        bins=bins,
        labels=False,
        include_lowest=True,
    )

    use_df = use_df.dropna(subset=["bin_id"])
    use_df["bin_id"] = use_df["bin_id"].astype(int)

    city_bin = (
        use_df
        .groupby([city_col, "bin_id"], observed=True)
        .agg(
            city_bin_median_R=(target_col, "median"),
            city_bin_n=(target_col, "size"),
        )
        .reset_index()
    )

    city_bin = city_bin[
        city_bin["city_bin_n"] >= min_paths_per_city_bin
    ].copy()

    rows = []

    for bin_id in range(n_bins):
        one_bin = city_bin[city_bin["bin_id"] == bin_id].copy()

        vals = one_bin["city_bin_median_R"].dropna().to_numpy()
        city_ns = one_bin["city_bin_n"].dropna().to_numpy()

        n_cities = len(vals)

        if n_cities >= min_cities_per_bin:
            rows.append({
                "bin_id": bin_id,
                "bin_center": bin_centers[bin_id],
                "bin_left": bins[bin_id],
                "bin_right": bins[bin_id + 1],
                "median_across_cities": np.median(vals),
                "iqr_low_across_cities": np.percentile(vals, 25),
                "iqr_high_across_cities": np.percentile(vals, 75),
                "n_cities": n_cities,
                "total_active_paths_in_valid_city_bins": int(np.sum(city_ns)),
                "min_city_bin_n": int(np.min(city_ns)) if len(city_ns) > 0 else np.nan,
                "max_city_bin_n": int(np.max(city_ns)) if len(city_ns) > 0 else np.nan,
            })

    summary = pd.DataFrame(rows)

    return summary, city_bin, {
        "q_low": q_low,
        "q_high": q_high,
        "bins": bins,
        "bin_centers": bin_centers,
    }


# =========================
# 5. Axis formatting
# =========================
def format_x_axis(ax, feature_col):
    """
    Apply feature-specific x-axis formatting.
    """
    if feature_col == "Delta_Race_White":
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100))

    if feature_col == "Delta_Pop_Density":
        # Delta_Pop_Density is interpreted as:
        # log10(origin population density / destination population density)
        multipliers = [1 / 12, 1 / 6, 1 / 3, 1, 2, 6]
        ticks = [np.log10(m) for m in multipliers]
        labels = [
            "1/12x",
            "1/6x",
            "1/3x",
            "1x\nEquality",
            "2x",
            "6x",
        ]

        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)

        ax.axvline(
            0,
            linestyle="--",
            color="#555555",
            linewidth=1.4,
            alpha=0.8,
            zorder=1,
        )


# =========================
# 6. Plotting function
# =========================
def plot_city_equalized_relationship(
    data,
    feature_col,
    x_label,
    panel_label,
    save_suffix,
    color_theme,
):
    print(f"\nStep 2: Plotting Fig. 4{panel_label}: {feature_col}")

    summary, city_bin, bin_info = compute_city_equalized_binned_median(
        data=data,
        feature_col=feature_col,
    )

    if summary.empty:
        raise ValueError(
            f"No valid bins for {feature_col}. "
            "Try lowering MIN_PATHS_PER_CITY_BIN or MIN_CITIES_PER_BIN."
        )

    summary_path = os.path.join(
        OUTPUT_DATA_DIR,
        f"Fig4{panel_label}_city_equalized_binned_summary_{save_suffix}.csv",
    )
    city_bin_path = os.path.join(
        OUTPUT_DATA_DIR,
        f"Fig4{panel_label}_city_bin_medians_{save_suffix}.csv",
    )

    summary.to_csv(summary_path, index=False)
    city_bin.to_csv(city_bin_path, index=False)

    print(f"  Saved binned summary: {summary_path}")
    print(f"  Saved city-bin medians: {city_bin_path}")
    print(f"  Valid bins: {len(summary)}")
    print(f"  Cities per bin range: {summary['n_cities'].min()} - {summary['n_cities'].max()}")
    print(
        "  Active paths per valid city-bin range: "
        f"{summary['min_city_bin_n'].min()} - {summary['max_city_bin_n'].max()}"
    )

    x = summary["bin_center"].to_numpy()
    y = summary["median_across_cities"].to_numpy()
    y_low = summary["iqr_low_across_cities"].to_numpy()
    y_high = summary["iqr_high_across_cities"].to_numpy()

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

    ax.fill_between(
        x,
        y_low,
        y_high,
        color=color_theme,
        alpha=0.22,
        linewidth=0,
        label="Interquartile range across cities",
        zorder=2,
    )

    ax.plot(
        x,
        y,
        color=color_theme,
        linewidth=2.6,
        zorder=4,
        label="Median across cities",
    )

    ax.scatter(
        x,
        y,
        s=70,
        color=color_theme,
        edgecolor="white",
        linewidth=0.9,
        zorder=5,
    )

    ax.axhline(
        1.0,
        linestyle=":",
        color="black",
        linewidth=2,
        alpha=1.0,
        zorder=1,
    )

    ax.text(
        0.04,
        0.50,
        r"$R$ = 1.0",
        transform=ax.transAxes,
        fontsize=14,
        ha="left",
        va="center",
    )

    format_x_axis(ax, feature_col)

    ax.set_xlabel(x_label, fontsize=16, labelpad=10)
    ax.set_ylabel(r"Realization ratio ($R$)", fontsize=16, labelpad=10)

    x_min = summary["bin_left"].min()
    x_max = summary["bin_right"].max()
    x_pad = 0.03 * (x_max - x_min)
    ax.set_xlim(x_min - x_pad, x_max + x_pad)

    y_min = np.nanmin(y_low)
    y_max = np.nanmax(y_high)
    y_range = y_max - y_min

    if y_range <= 0:
        y_range = max(y_max, 1.0) * 0.1

    ax.set_ylim(
        bottom=max(0, y_min - 0.10 * y_range),
        top=y_max + 0.15 * y_range,
    )

    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=13,
    )

    sns.despine()
    plt.tight_layout()

    save_name = f"Figure_4{panel_label}"

    png_path = os.path.join(OUTPUT_IMG_DIR, f"{save_name}.png")
    svg_path = os.path.join(OUTPUT_IMG_DIR, f"{save_name}.svg")

    plt.savefig(png_path, dpi=300)
    plt.savefig(svg_path)

    plt.close(fig)

    print(f"  Saved figure: {png_path}")
    print(f"  Saved figure: {svg_path}")


# =========================
# 7. Execute Fig. 4C and Fig. 4D
# =========================

plot_city_equalized_relationship(
    data=df_active,
    feature_col="Delta_Race_White",
    x_label="White population share gap (origin - destination)",
    panel_label="C",
    save_suffix="RacialGap",
    color_theme="#4E79A7",
)

plot_city_equalized_relationship(
    data=df_active,
    feature_col="Delta_Pop_Density",
    x_label="origin/destination population density ratio",
    panel_label="D",
    save_suffix="PopulationDensityRatio",
    color_theme="#D35450",
)

print("\nFig. 4C/D city-equalized active-path analysis complete.")

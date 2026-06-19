import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from scipy import stats


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

real_folder = os.path.join(SCRIPT_DIR, "real")
pred_folder = os.path.join(SCRIPT_DIR, "gravity")
ref_folder = os.path.join(ROOT_DIR, "city_population_poi")
output_folder = SCRIPT_DIR

CITY_NAMES = [
    "Washington, D.C",
    "Miami",
    "Atlanta",
    "Chicago",
    "Boston",
    "Detroit",
    "New York",
    "Pittsburgh",
    "Philadelphia",
    "Dallas",
    "Houston",
    "Los Angeles",
    "San Diego",
    "San Francisco",
    "Phoenix",
    "St. Louis",
]

TYPE_LPW = "LPW"
TYPE_HPM = "HPM"
FLOW_HPM_TO_LPW = "HPM_to_LPW"
FLOW_LPW_TO_HPM = "LPW_to_HPM"
THRESHOLD_PRED = 0

COLOR_H2L = "#D35450"
COLOR_L2H = "#4E79A7"
COLOR_GRAY = "#333333"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 12


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def validate_matrix(df, source_name):
    if df.empty:
        raise ValueError(f"{source_name} is empty.")
    if df.index.empty or df.columns.empty:
        raise ValueError(f"{source_name} must contain an origin index and destination columns.")


def load_type_map(city):
    ref_path = os.path.join(ref_folder, f"{city}.csv")
    if not os.path.exists(ref_path):
        matches = glob.glob(os.path.join(ref_folder, f"*{city}*.csv"))
        ref_path = matches[0] if matches else None

    if not ref_path:
        raise FileNotFoundError(f"No attribute file found for {city}")

    type_map = pd.read_csv(ref_path, dtype={"origin_geoid": str})
    validate_columns(type_map, {"origin_geoid", "origin_geoid_type"}, ref_path)
    type_map["origin_geoid_type"] = type_map["origin_geoid_type"].astype(str).str.strip()
    return dict(zip(type_map["origin_geoid"], type_map["origin_geoid_type"]))


def load_matrix(path):
    df = pd.read_csv(path, index_col=0, dtype={0: str})
    validate_matrix(df, path)
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    df.index.name = "origin_geoid"
    return df.apply(pd.to_numeric, errors="coerce").fillna(0)


def get_link_data_and_stats():
    all_active_data = []
    stats_counter = {
        FLOW_HPM_TO_LPW: {"total": 0, "blocked": 0},
        FLOW_LPW_TO_HPM: {"total": 0, "blocked": 0},
    }

    print(f"Extracting link data with predicted flow > {THRESHOLD_PRED}...")

    for city in CITY_NAMES:
        try:
            f_real = os.path.join(real_folder, f"{city}.csv")
            f_pred = os.path.join(pred_folder, f"{city}.csv")

            if not (os.path.exists(f_real) and os.path.exists(f_pred)):
                print(f"Missing real or predicted matrix for {city}; skipping.")
                continue

            type_dict = load_type_map(city)
            df_r = load_matrix(f_real)
            df_p = load_matrix(f_pred)

            idx = df_r.index.intersection(df_p.index)
            col = df_r.columns.intersection(df_p.columns)
            df_r = df_r.loc[idx, col]
            df_p = df_p.loc[idx, col]

            series_r = df_r.stack()
            series_p = df_p.stack()

            df_link = pd.concat([series_r, series_p], axis=1, keys=["Obs", "Pred"])
            df_link.index.names = ["origin_block", "destination_block"]
            df_link = df_link.reset_index()

            df_valid = df_link[df_link["Pred"] > THRESHOLD_PRED].copy()
            if df_valid.empty:
                continue

            df_valid["O_Type"] = df_valid["origin_block"].map(type_dict)
            df_valid["D_Type"] = df_valid["destination_block"].map(type_dict)
            df_valid = df_valid.dropna(subset=["O_Type", "D_Type"])

            h2l_all = df_valid[(df_valid["O_Type"] == TYPE_HPM) & (df_valid["D_Type"] == TYPE_LPW)]
            stats_counter[FLOW_HPM_TO_LPW]["total"] += len(h2l_all)
            stats_counter[FLOW_HPM_TO_LPW]["blocked"] += len(h2l_all[h2l_all["Obs"] == 0])

            l2h_all = df_valid[(df_valid["O_Type"] == TYPE_LPW) & (df_valid["D_Type"] == TYPE_HPM)]
            stats_counter[FLOW_LPW_TO_HPM]["total"] += len(l2h_all)
            stats_counter[FLOW_LPW_TO_HPM]["blocked"] += len(l2h_all[l2h_all["Obs"] == 0])

            active_links = df_valid[df_valid["Obs"] > 0].copy()

            h2l_active = active_links[
                (active_links["O_Type"] == TYPE_HPM) & (active_links["D_Type"] == TYPE_LPW)
            ].copy()
            h2l_active["flow_type"] = FLOW_HPM_TO_LPW

            l2h_active = active_links[
                (active_links["O_Type"] == TYPE_LPW) & (active_links["D_Type"] == TYPE_HPM)
            ].copy()
            l2h_active["flow_type"] = FLOW_LPW_TO_HPM

            combined = pd.concat([h2l_active, l2h_active])
            if not combined.empty:
                combined["LogRatio"] = np.log10(combined["Obs"] / combined["Pred"])
                all_active_data.append(combined[["flow_type", "LogRatio"]])

        except Exception as exc:
            print(f"Error processing {city}: {exc}")
            continue

    df_ecdf = pd.concat(all_active_data, ignore_index=True) if all_active_data else pd.DataFrame()
    return df_ecdf, stats_counter


if __name__ == "__main__":
    df_plot, blockage_stats = get_link_data_and_stats()

    if not df_plot.empty:
        rate_h2l = (
            blockage_stats[FLOW_HPM_TO_LPW]["blocked"]
            / blockage_stats[FLOW_HPM_TO_LPW]["total"]
        )
        rate_l2h = (
            blockage_stats[FLOW_LPW_TO_HPM]["blocked"]
            / blockage_stats[FLOW_LPW_TO_HPM]["total"]
        )

        print(f"HPM to LPW blockage rate: {rate_h2l:.2%}")
        print(f"LPW to HPM blockage rate: {rate_l2h:.2%}")

        fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)

        sns.ecdfplot(
            data=df_plot,
            x="LogRatio",
            hue="flow_type",
            palette={FLOW_HPM_TO_LPW: COLOR_H2L, FLOW_LPW_TO_HPM: COLOR_L2H},
            linewidth=3,
            ax=ax,
        )

        x_grid = np.linspace(-5, 5, 1000)
        vals_h2l = df_plot[df_plot["flow_type"] == FLOW_HPM_TO_LPW]["LogRatio"].values
        vals_l2h = df_plot[df_plot["flow_type"] == FLOW_LPW_TO_HPM]["LogRatio"].values

        def compute_ecdf_y(data, x):
            return np.mean(data[:, None] <= x, axis=0)

        y_h2l = compute_ecdf_y(vals_h2l, x_grid)
        y_l2h = compute_ecdf_y(vals_l2h, x_grid)

        ax.fill_between(
            x_grid,
            y_h2l,
            y_l2h,
            where=(y_l2h > y_h2l),
            color="gray",
            alpha=0.25,
            label="Asymmetry gap",
        )

        med_h2l = np.median(vals_h2l)
        med_l2h = np.median(vals_l2h)

        ax.axhline(0.5, color="gray", linestyle=":", alpha=1.0)
        ax.plot(med_h2l, 0.5, "o", color=COLOR_H2L, markersize=6)
        ax.plot(med_l2h, 0.5, "o", color=COLOR_L2H, markersize=6)

        y_at_0_h2l = np.mean(vals_h2l <= 0)
        y_at_0_l2h = np.mean(vals_l2h <= 0)

        ax.axvline(0, color=COLOR_GRAY, linestyle="--", alpha=0.8, label="$T_{obs}=T_{pred}$")

        ax.annotate(
            f"{y_at_0_h2l:.1%} < Pred",
            xy=(0, y_at_0_h2l),
            xytext=(0.5, y_at_0_h2l - 0.05),
            arrowprops=dict(arrowstyle="->", color=COLOR_H2L),
            color=COLOR_H2L,
            fontsize=12,
        )
        ax.annotate(
            f"{y_at_0_l2h:.1%} < Pred",
            xy=(0, y_at_0_l2h),
            xytext=(-1.2, y_at_0_l2h + 0.05),
            arrowprops=dict(arrowstyle="->", color=COLOR_L2H),
            color=COLOR_L2H,
            fontsize=12,
        )

        ks_stat, p_val = stats.ks_2samp(vals_h2l, vals_l2h)
        p_text = "p < 0.001" if p_val < 0.001 else f"p = {p_val:.3f}"
        stats_text = f"Two-sample KS test\n$D={ks_stat:.3f}, {p_text}$"
        ax.text(
            0.97,
            0.68,
            stats_text,
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
        )

        ax.text(0.5, 0.95, "$R = 1.0$", transform=ax.transAxes, ha="right", va="top", fontsize=12)

        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel(r"Realization ratio ($\log R$)", fontsize=14)
        ax.set_ylabel("Cumulative probability", fontsize=14)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        legend_elements = [
            Line2D([0], [0], color=COLOR_H2L, lw=3, label="HPM to LPW"),
            Line2D([0], [0], color=COLOR_L2H, lw=3, label="LPW to HPM"),
        ]
        ax.legend(handles=legend_elements, loc="upper left", frameon=False)

        ax_inset = ax.inset_axes([0.62, 0.1, 0.3, 0.3])

        bars_labels = ["LPW\nto HPM", "HPM\nto LPW"]
        x_positions = [0, 1]
        rates = [rate_l2h, rate_h2l]
        colors = [COLOR_L2H, COLOR_H2L]

        ax_inset.bar(x_positions, rates, color=colors, alpha=0.9, width=0.6)
        ax_inset.set_xticks(x_positions)
        ax_inset.set_xticklabels(bars_labels)
        ax_inset.set_title("Blockage rate ($R=0$)", fontsize=12)
        ax_inset.set_ylim(0, 1)

        ax_inset.spines["top"].set_visible(False)
        ax_inset.spines["right"].set_visible(False)
        ax_inset.spines["left"].set_visible(False)
        ax_inset.get_yaxis().set_visible(False)

        for i, value in enumerate(rates):
            ax_inset.text(
                i,
                value + 0.05,
                f"{value:.1%}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
                color=colors[i],
            )

        ax_inset.tick_params(axis="x", labelsize=12, length=0)

        os.makedirs(output_folder, exist_ok=True)
        plt.savefig(os.path.join(output_folder, "Fig3B.png"), dpi=300, bbox_inches="tight")
        plt.savefig(os.path.join(output_folder, "Fig3B.svg"), format="svg", bbox_inches="tight")

        print("ECDF figure complete.")
        plt.show()

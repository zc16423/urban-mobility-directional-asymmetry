import os

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.unicode_minus": False,
})

plt.style.use("default")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ATTRIBUTE_FILE = os.path.join(SCRIPT_DIR, "Fig1EF_attributes.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "0")

FLOW_COLUMNS = {"flow_type", "origin_block", "destination_block", "flow_count"}
ATTRIBUTE_COLUMNS = {
    "origin_geoid",
    "pct_Prs_Blw_Pov_Lev_ACS_15_19",
    "Race",
    "Poverty",
    "origin_geoid_type",
}

CONFIGS = [
    {
        "name": "LPW_to_HPM",
        "flow_file": os.path.join(SCRIPT_DIR, "Fig1E.csv"),
        "poverty_file": ATTRIBUTE_FILE,
        "output_filename": "Fig1E",
        "title": "Boston Flow: LPW to HPM",
        "origin_type": "LPW",
        "dest_type": "HPM",
        "threshold": 1,
    },
    {
        "name": "HPM_to_LPW",
        "flow_file": os.path.join(SCRIPT_DIR, "Fig1F.csv"),
        "poverty_file": ATTRIBUTE_FILE,
        "output_filename": "Fig1F",
        "title": "Boston Flow: HPM to LPW",
        "origin_type": "HPM",
        "dest_type": "LPW",
        "threshold": 1,
    },
]


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def create_split_colormap():
    """
    Create a split poverty colormap: blue for low poverty and red for high poverty.
    """
    colors_low = plt.cm.Blues(np.linspace(0.2, 0.9, 128))
    colors_high = plt.cm.Reds(np.linspace(0.2, 0.9, 128))
    colors_combined = np.vstack((colors_low, colors_high))
    return mcolors.LinearSegmentedColormap.from_list("SplitBlueRed", colors_combined)


def map_value_to_norm(value):
    """
    Map low- and high-poverty percentage ranges into separate halves of the colormap.
    """
    low_min, low_max = 0, 3
    high_min, high_max = 35, 80

    if value < 30:
        ratio = (value - low_min) / (low_max - low_min)
        return 0.0 + ratio * 0.5

    ratio = (value - high_min) / (high_max - high_min)
    return 0.5 + ratio * 0.5


def load_data(flow_path, poverty_path, threshold, expected_flow_type):
    print(f"Loading: {os.path.basename(flow_path)}")
    try:
        df_flow = pd.read_csv(flow_path, dtype=str)
        validate_columns(df_flow, FLOW_COLUMNS, flow_path)

        df_flow["flow_type"] = df_flow["flow_type"].astype(str).str.strip()
        df_flow["flow_count"] = pd.to_numeric(df_flow["flow_count"], errors="coerce")
        df_flow = df_flow[df_flow["flow_type"] == expected_flow_type].copy()

        initial_len = len(df_flow)
        df_flow = df_flow[df_flow["flow_count"] >= threshold].copy()
        print(f"  - Flow filter: {initial_len} -> {len(df_flow)} (threshold {threshold})")

        df_pov = pd.read_csv(poverty_path, dtype=str)
        validate_columns(df_pov, ATTRIBUTE_COLUMNS, poverty_path)

        col_pov = "pct_Prs_Blw_Pov_Lev_ACS_15_19"
        df_pov[col_pov] = pd.to_numeric(df_pov[col_pov], errors="coerce")

        pov_dict = dict(zip(df_pov["origin_geoid"].astype(str), df_pov[col_pov]))

        df_flow["origin_poverty"] = df_flow["origin_block"].map(pov_dict)
        df_flow["dest_poverty"] = df_flow["destination_block"].map(pov_dict)

        df_flow = df_flow.dropna(subset=["origin_poverty", "dest_poverty"])
        return df_flow, pov_dict
    except Exception as exc:
        print(f"  Failed to load data: {exc}")
        return pd.DataFrame(), {}


def get_node_positions_simple(df, node_col, poverty_col, y_position):
    unique_nodes = df[[node_col, poverty_col]].drop_duplicates(subset=[node_col])
    unique_nodes = unique_nodes.sort_values(by=poverty_col)
    nodes = unique_nodes[node_col].tolist()
    vals = unique_nodes[poverty_col].tolist()
    count = len(nodes)
    pos = {}
    for i, node in enumerate(nodes):
        x = i / max(1, count - 1)
        pos[node] = (x, y_position)
    return pos, vals


def draw_bezier_curve(ax, p1, p2, color, alpha, linewidth):
    x1, y1 = p1
    x2, y2 = p2
    x_mid = (x1 + x2) / 2
    y_mid = 0.5
    t = np.linspace(0, 1, 100)
    x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * x_mid + t ** 2 * x2
    y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * y_mid + t ** 2 * y2
    ax.plot(x, y, color=color, alpha=alpha, linewidth=linewidth)


def visualize_flow(config):
    try:
        df, _ = load_data(
            config["flow_file"],
            config["poverty_file"],
            config["threshold"],
            config["name"],
        )
        if df.empty:
            return

        fig, ax = plt.subplots(figsize=(6.8, 7.0))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        if config["origin_type"] == "LPW":
            top_col, top_pov_col = "origin_block", "origin_poverty"
            bot_col, bot_pov_col = "destination_block", "dest_poverty"
            is_downward = True
            top_label = "LPW CBGs (top 50 wealthiest)"
            bot_label = "HPM CBGs (top 50 poorest)"
        else:
            top_col, top_pov_col = "destination_block", "dest_poverty"
            bot_col, bot_pov_col = "origin_block", "origin_poverty"
            is_downward = False
            top_label = "LPW CBGs (top 50 wealthiest)"
            bot_label = "HPM CBGs (top 50 poorest)"

        pos_top, vals_top = get_node_positions_simple(df, top_col, top_pov_col, 1.0)
        pos_bot, vals_bot = get_node_positions_simple(df, bot_col, bot_pov_col, 0.0)

        split_cmap = create_split_colormap()

        node_colors_top = [split_cmap(map_value_to_norm(v)) for v in vals_top]
        node_colors_bot = [split_cmap(map_value_to_norm(v)) for v in vals_bot]

        max_flow = df["flow_count"].max()
        min_flow = df["flow_count"].min()

        print("  - Drawing flow lines...")
        df = df.sort_values(by="flow_count", ascending=True)

        for _, row in df.iterrows():
            oid = row["origin_block"]
            did = row["destination_block"]
            flow_val = row["flow_count"]
            origin_pov = row["origin_poverty"]

            if is_downward:
                p_start = pos_top.get(oid)
                p_end = pos_bot.get(did)
            else:
                p_start = pos_bot.get(oid)
                p_end = pos_top.get(did)

            if p_start and p_end:
                lw = 0.1 + 5.0 * (flow_val - min_flow) / (max_flow - min_flow + 1e-6)
                line_color = split_cmap(map_value_to_norm(origin_pov))
                alpha = 0.4 if flow_val < (max_flow * 0.9) else 0.9
                draw_bezier_curve(ax, p_start, p_end, line_color, alpha, lw)

        ax.scatter(
            [p[0] for p in pos_top.values()],
            [p[1] for p in pos_top.values()],
            c=node_colors_top,
            s=100,
            zorder=10,
            edgecolors="black",
            linewidth=0.6,
        )

        ax.scatter(
            [p[0] for p in pos_bot.values()],
            [p[1] for p in pos_bot.values()],
            c=node_colors_bot,
            s=100,
            zorder=10,
            edgecolors="black",
            linewidth=0.6,
        )

        ax.text(-0.03, 0.81, top_label, rotation=90, va="center", ha="right", fontsize=12, color="black")
        ax.text(-0.03, 0.16, bot_label, rotation=90, va="center", ha="right", fontsize=12, color="black")

        sm = plt.cm.ScalarMappable(cmap=split_cmap, norm=mcolors.Normalize(vmin=0, vmax=1))
        sm.set_array([])

        cbar = plt.colorbar(sm, ax=ax, shrink=0.7, aspect=25, pad=0.01)
        cbar.set_label("Population below poverty level (%)", rotation=270, labelpad=25, fontsize=14)
        cbar.ax.axhline(y=0.5, c="white", linewidth=20, zorder=10)

        ticks_locs = [0.0, 0.25, 0.47, 0.53, 0.75, 1.0]
        ticks_labels = ["0", "1.5", "3", "36", "58", "80"]

        cbar.set_ticks(ticks_locs)
        cbar.set_ticklabels(ticks_labels)

        cbar.ax.set_ylim(0, 1)
        cbar.ax.invert_yaxis()

        ax.set_title(config["title"], fontsize=16, pad=5)
        ax.set_xlim(-0.1, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.axis("off")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        png_path = os.path.join(OUTPUT_DIR, f"{config['output_filename']}.png")
        svg_path = os.path.join(OUTPUT_DIR, f"{config['output_filename']}.svg")

        plt.tight_layout()
        plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
        plt.savefig(svg_path, format="svg", dpi=300, bbox_inches="tight")
        print(f"  [Done] Saved figure to: {png_path}")
        plt.close()

    except Exception as exc:
        print(f"  [Error] Failed to process {config['name']}: {exc}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("=== Starting batch flow-figure generation ===\n")
    for config in CONFIGS:
        visualize_flow(config)
        print("-" * 30)
    print("\n=== All tasks complete ===")

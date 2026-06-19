# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 16:13:00 2026

@author: Dell
"""

import gc
import os

import numpy as np
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DATA_DIR = os.path.join(SCRIPT_DIR, "basic_data")

LINK_LEVEL_FILE = os.path.join(BASE_DATA_DIR, "Link_Level_Realization_Ratio.csv")
STATIC_ATTR_FILE = os.path.join(BASE_DATA_DIR, "community_static_attributes.csv")
DIST_MATRIX_FOLDER = os.path.join(BASE_DATA_DIR, "distance_matrices")
OUTPUT_FILE = os.path.join(BASE_DATA_DIR, "Final_Regression_Dataset.csv")

LINK_COLUMNS = {
    "city",
    "origin_block",
    "destination_block",
    "flow_type",
    "Realization_Ratio_R",
}

STATIC_COLUMNS = {
    "origin_geoid",
    "pct_NH_White_alone_ACS_15_19",
    "pct_Prs_Blw_Pov_Lev_ACS_15_19",
    "pct_College_ACS_15_19",
    "total_poi",
    "pct_Pop_65plus_ACS_15_19",
    "pct_Owner_Occp_HU_ACS_15_19",
    "D1C",
    "D1B",
}

COL_MAPPING = {
    "pct_NH_White_alone_ACS_15_19": "Race_White",
    "pct_Prs_Blw_Pov_Lev_ACS_15_19": "Poverty",
    "pct_College_ACS_15_19": "Edu_College",
    "total_poi": "POI_Count",
    "pct_Pop_65plus_ACS_15_19": "Age_65plus",
    "pct_Owner_Occp_HU_ACS_15_19": "Housing_Owner",
    "D1C": "Job_Density",
    "D1B": "Pop_Density",
}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


print("1. Loading and cleaning static community attributes...")
static_df = pd.read_csv(STATIC_ATTR_FILE, dtype={"origin_geoid": str})
validate_columns(static_df, STATIC_COLUMNS, STATIC_ATTR_FILE)

cols_to_log = ["POI_Count", "Job_Density", "Pop_Density"]
for raw_col, new_name in COL_MAPPING.items():
    if new_name in cols_to_log and raw_col in static_df.columns:
        static_df[raw_col] = pd.to_numeric(static_df[raw_col], errors="coerce")
        static_df[raw_col] = np.log10(static_df[raw_col].fillna(0) + 1)

static_df = static_df.rename(columns=COL_MAPPING)
needed_cols = ["origin_geoid"] + list(COL_MAPPING.values())
available_cols = [c for c in needed_cols if c in static_df.columns]
static_df = static_df[available_cols].set_index("origin_geoid")

print(f" Static attributes loaded for {len(static_df)} communities.")

print("2. Loading link-level OD data...")
od_df = pd.read_csv(
    LINK_LEVEL_FILE,
    dtype={
        "city": str,
        "origin_block": str,
        "destination_block": str,
    },
)
validate_columns(od_df, LINK_COLUMNS, LINK_LEVEL_FILE)

target_label = "LPW_to_HPM"
od_df["flow_type"] = od_df["flow_type"].astype(str).str.strip()
od_df = od_df[od_df["flow_type"] == target_label].copy()

print(f"   After filtering {target_label}, {len(od_df)} rows remain.")

final_chunks = []
unique_cities = od_df["city"].dropna().unique()

for city in unique_cities:
    city = str(city)
    print(f"   Processing city: {city} ...")

    city_od = od_df[od_df["city"].astype(str) == city].copy()

    dist_file = os.path.join(DIST_MATRIX_FOLDER, f"{city}.csv")
    if not os.path.exists(dist_file):
        print(f"   [WARNING] Distance matrix not found for city {city}; skipping.")
        continue

    dist_mat = pd.read_csv(dist_file, index_col=0, dtype={0: str})
    dist_mat.index = dist_mat.index.astype(str)
    dist_mat.columns = dist_mat.columns.astype(str)

    valid_origins = [o for o in city_od["origin_block"].unique() if o in dist_mat.index]
    valid_dests = [d for d in city_od["destination_block"].unique() if d in dist_mat.columns]

    if not valid_origins or not valid_dests:
        print(f"   [INFO] City {city} has no matching OD distances; skipping.")
        continue

    subset_dist = dist_mat.loc[valid_origins, valid_dests].stack().reset_index()
    subset_dist.columns = ["origin_block", "destination_block", "Distance"]

    city_od = pd.merge(
        city_od,
        subset_dist,
        on=["origin_block", "destination_block"],
        how="inner",
    )

    city_od = city_od.join(static_df.add_suffix("_O"), on="origin_block", how="inner")
    city_od = city_od.join(static_df.add_suffix("_D"), on="destination_block", how="inner")

    features = [c[:-2] for c in city_od.columns if c.endswith("_O")]

    for feat in features:
        if f"{feat}_D" in city_od.columns:
            city_od[f"Delta_{feat}"] = city_od[f"{feat}_O"] - city_od[f"{feat}_D"]

    city_od["Log_Distance"] = np.log10(city_od["Distance"] + 0.1)

    delta_cols = [c for c in city_od.columns if c.startswith("Delta_")]
    cols_to_keep = [
        "city",
        "origin_block",
        "destination_block",
        "Realization_Ratio_R",
        "Log_Distance",
    ] + delta_cols

    final_chunks.append(city_od[cols_to_keep])

    del dist_mat, subset_dist, city_od
    gc.collect()

if final_chunks:
    print("4. Combining and saving final table...")
    final_df = pd.concat(final_chunks, ignore_index=True)

    final_df["Realization_Ratio_R"] = pd.to_numeric(
        final_df["Realization_Ratio_R"],
        errors="coerce",
    )
    final_df = final_df[final_df["Realization_Ratio_R"] >= 0]
    final_df = final_df.replace([np.inf, -np.inf], np.nan).dropna()

    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Total sample size: {len(final_df)}")
    print("Features:", [c for c in final_df.columns if c.startswith("Delta_") or c == "Log_Distance"])
else:
    print("No data generated. Check input paths and matching identifiers.")

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 11:38:04 2026

@author: Dell
"""

import glob
import os

import numpy as np
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BASE_DATA_DIR = os.path.join(SCRIPT_DIR, "basic_data")

real_folder = os.path.join(BASE_DATA_DIR, "real")
pred_folder = os.path.join(BASE_DATA_DIR, "gravity")
reference_folder = os.path.join(ROOT_DIR, "city_population_poi")
output_folder = BASE_DATA_DIR
os.makedirs(output_folder, exist_ok=True)

output_csv_path = os.path.join(output_folder, "Link_Level_Realization_Ratio.csv")

CITY_NAMES = [
    "Los Angeles",
    "San Diego",
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
    "San Francisco",
    "Houston",
    "Phoenix",
    "St. Louis",
]

TYPE_LPW = "LPW"
TYPE_HPM = "HPM"
FLOW_LPW_TO_HPM = "LPW_to_HPM"
FLOW_HPM_TO_LPW = "HPM_to_LPW"


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


def validate_matrix(df, source_name):
    if df.empty:
        raise ValueError(f"{source_name} is empty.")
    if df.index.empty or df.columns.empty:
        raise ValueError(f"{source_name} must contain an origin index and destination columns.")


def load_reference_data(city):
    ref_path = os.path.join(reference_folder, f"{city}.csv")
    if not os.path.exists(ref_path):
        files = glob.glob(os.path.join(reference_folder, f"*{city}*.csv"))
        ref_path = files[0] if files else None

    if not ref_path:
        print(f"  [WARNING] No reference file found for {city}; skipping.")
        return None

    df = pd.read_csv(ref_path, dtype={"origin_geoid": str})
    validate_columns(df, {"origin_geoid", "origin_geoid_type"}, ref_path)
    df["origin_geoid_type"] = df["origin_geoid_type"].astype(str).str.strip()
    return dict(zip(df["origin_geoid"], df["origin_geoid_type"]))


def load_matrix(path):
    df = pd.read_csv(path, index_col=0, dtype={0: str})
    validate_matrix(df, path)
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    df.index.name = "origin_geoid"
    return df.apply(pd.to_numeric, errors="coerce").fillna(0)


def process_city_links(city):
    print(f"Processing: {city}...")

    real_path = os.path.join(real_folder, f"{city}.csv")
    pred_path = os.path.join(pred_folder, f"{city}.csv")

    if not os.path.exists(real_path) or not os.path.exists(pred_path):
        print(f"  [ERROR] Missing real or predicted matrix file for {city}.")
        return None

    cbg_type_map = load_reference_data(city)
    if not cbg_type_map:
        return None

    try:
        df_real = load_matrix(real_path)
        df_pred = load_matrix(pred_path)
    except Exception as exc:
        print(f"  [ERROR] Failed to read matrix CSV: {exc}")
        return None

    shared_index = df_real.index.intersection(df_pred.index)
    shared_columns = df_real.columns.intersection(df_pred.columns)
    df_real = df_real.loc[shared_index, shared_columns]
    df_pred = df_pred.loc[shared_index, shared_columns]

    real_melt = df_real.stack().reset_index()
    real_melt.columns = ["origin_block", "destination_block", "Flow_real"]

    pred_melt = df_pred.stack().reset_index()
    pred_melt.columns = ["origin_block", "destination_block", "Flow_gravity"]

    merged = pd.merge(real_melt, pred_melt, on=["origin_block", "destination_block"], how="inner")
    merged = merged[merged["origin_block"] != merged["destination_block"]]
    merged = merged[merged["Flow_gravity"] > 0]

    merged["O_Type"] = merged["origin_block"].map(cbg_type_map)
    merged["D_Type"] = merged["destination_block"].map(cbg_type_map)
    merged = merged.dropna(subset=["O_Type", "D_Type"])

    condition_lh = (merged["O_Type"] == TYPE_LPW) & (merged["D_Type"] == TYPE_HPM)
    condition_hl = (merged["O_Type"] == TYPE_HPM) & (merged["D_Type"] == TYPE_LPW)

    final_df = merged[condition_lh | condition_hl].copy()

    if final_df.empty:
        return None

    final_df["Realization_Ratio_R"] = final_df["Flow_real"] / final_df["Flow_gravity"]
    final_df["flow_type"] = np.where(
        final_df["O_Type"] == TYPE_LPW,
        FLOW_LPW_TO_HPM,
        FLOW_HPM_TO_LPW,
    )

    final_df["city"] = city

    cols_to_keep = [
        "city",
        "origin_block",
        "destination_block",
        "flow_type",
        "Flow_real",
        "Flow_gravity",
        "Realization_Ratio_R",
    ]

    return final_df[cols_to_keep]


all_links_list = []

for city in CITY_NAMES:
    city_df = process_city_links(city)
    if city_df is not None:
        all_links_list.append(city_df)

if all_links_list:
    print("\nCombining all city data...")
    full_df = pd.concat(all_links_list, ignore_index=True)

    print(f"Total rows: {len(full_df)} OD links")

    full_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Processing complete. File saved to: {output_csv_path}")
    print("-" * 30)
    print("Preview:")
    print(full_df.head())

    print("\nDirectional summary:")
    print(full_df.groupby("flow_type")["Realization_Ratio_R"].describe())
else:
    print("No data generated.")

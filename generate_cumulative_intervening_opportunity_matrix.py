from pathlib import Path
import gc
import time
import traceback

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent
BASE_DISTANCE_PATH = ROOT_DIR / "city_distance_matrices"
BASE_POP_PATH = ROOT_DIR / "city_population_poi"
BASE_OUTPUT_PATH = ROOT_DIR / "basic_data" / "cumulative_intervening_opportunity_matrices"
REQUIRED_POP_COLUMNS = {"origin_geoid", "Tot_Population_ACS_15_19"}


def validate_columns(df, required_columns, source_path):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_path} is missing required columns: {', '.join(missing)}")


def ensure_str_index(df):
    """Keep wide matrix labels comparable during alignment."""
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    df.index.name = "origin_geoid"
    return df


def read_wide_matrix(path):
    df = pd.read_csv(path, index_col=0)
    if df.index.name != "origin_geoid":
        raise ValueError(f"{path} first column must be origin_geoid; found {df.index.name!r}")
    return ensure_str_index(df)


def compute_opportunity_matrix_optimized(distance_matrix, pop_values):
    """
    Compute cumulative intervening opportunities.

    For each origin row, CBGs are sorted by distance and the opportunity value
    for each target is the cumulative ACS count of closer CBGs, excluding the
    target itself.
    """
    num_points = distance_matrix.shape[0]
    opp_matrix = np.zeros_like(distance_matrix, dtype=float)
    pop_values = np.array(pop_values)

    print(f"    Running optimized matrix calculation: {num_points}x{num_points}")

    for i in range(num_points):
        if i % 500 == 0:
            print(f"    Progress: row {i}/{num_points}")

        dists_from_i = distance_matrix[i, :]

        current_pop = pop_values.copy()
        current_pop[i] = 0

        sorted_indices = np.argsort(dists_from_i)
        sorted_pop = current_pop[sorted_indices]

        cumsum_pop = np.cumsum(sorted_pop)
        s_values_sorted = cumsum_pop - sorted_pop

        row_opps = np.zeros(num_points)
        row_opps[sorted_indices] = s_values_sorted
        opp_matrix[i, :] = row_opps

    np.fill_diagonal(opp_matrix, 0)
    return opp_matrix


def main():
    BASE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    city_files = sorted(BASE_DISTANCE_PATH.glob("*.csv"))
    print(f"Detected {len(city_files)} cities: {[path.stem for path in city_files]}")

    for dist_file in city_files:
        start_time = time.time()
        city = dist_file.stem
        print("\n" + "=" * 50)
        print(f"Processing city: {city}")

        pop_file = BASE_POP_PATH / f"{city}.csv"
        save_path = BASE_OUTPUT_PATH / f"{city}_opportunity_matrix.csv"

        if save_path.exists():
            print("Result file already exists; skipping.")
            continue

        try:
            print("    Reading distance matrix...")
            distance_df = read_wide_matrix(dist_file)
            dist_mat = distance_df.to_numpy(dtype=float)
            b_ids = distance_df.index.tolist()

            print("    Reading and aligning ACS counts...")
            pop_df = pd.read_csv(pop_file, dtype={"origin_geoid": str})
            validate_columns(pop_df, REQUIRED_POP_COLUMNS, pop_file)
            pop_df["origin_geoid"] = pop_df["origin_geoid"].astype(str)
            pop_aligned = pop_df.set_index("origin_geoid").reindex(b_ids).fillna(0)
            pop_vec = pd.to_numeric(
                pop_aligned["Tot_Population_ACS_15_19"], errors="coerce"
            ).fillna(0).to_numpy()

            opp_mat = compute_opportunity_matrix_optimized(dist_mat, pop_vec)

            print("    Saving result...")
            opp_df = pd.DataFrame(opp_mat, index=b_ids, columns=b_ids)
            opp_df.index.name = "origin_geoid"
            opp_df.to_csv(save_path, encoding="utf-8-sig")

            del dist_mat, pop_vec, opp_mat, opp_df, distance_df, pop_df, pop_aligned
            gc.collect()

            elapsed = (time.time() - start_time) / 60
            print(f"City {city} completed in {elapsed:.2f} minutes.")

        except Exception as exc:
            print(f"City {city} failed: {exc}")
            traceback.print_exc()

    print("\nAll city cumulative-opportunity matrices are complete.")


if __name__ == "__main__":
    main()

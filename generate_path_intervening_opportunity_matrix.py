from pathlib import Path
import gc
import time
import traceback

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent
BASE_DISTANCE_PATH = ROOT_DIR / "city_distance_matrices"
BASE_POP_PATH = ROOT_DIR / "city_population_poi"
BASE_OUTPUT_PATH = ROOT_DIR / "basic_data" / "path_intervening_opportunity_matrices"
PATH_TOLERANCE = 0.5
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


def compute_path_based_matrix_matrixized(dist_mat, pop_vec, tolerance):
    """
    Compute path-based intervening opportunities S_ij.

    For each origin i and target j, the matrix sums all intermediate CBGs k
    whose detour path i -> k -> j stays within the configured tolerance.
    """
    num_points = dist_mat.shape[0]
    opp_matrix = np.zeros_like(dist_mat, dtype=float)
    pop_col = pop_vec.reshape(-1, 1)

    print(f"      Running matrix calculation: {num_points}x{num_points}")

    for i in range(num_points):
        if i % 100 == 0:
            print(f"      Progress: origin row {i}/{num_points}")

        d_ik_vec = dist_mat[i, :].reshape(-1, 1)
        d_ij_vec = dist_mat[i, :].reshape(1, -1)
        thresholds = d_ij_vec * (1 + tolerance)
        path_len_matrix = d_ik_vec + dist_mat
        mask = path_len_matrix < thresholds

        mask[i, :] = False
        np.fill_diagonal(mask, False)

        row_result = np.dot(mask.T, pop_col).flatten()
        opp_matrix[i, :] = row_result

        del path_len_matrix, mask, row_result

    np.fill_diagonal(opp_matrix, 0)
    return opp_matrix


def generate_baseline_flows(s_matrix_df, real_flow_df, L_param):
    """
    Build a counterfactual baseline flow matrix from an opportunity matrix.

    The diagonal is excluded when calculating observed outflow totals and
    assigning destination probabilities.
    """
    common_idx = s_matrix_df.index.intersection(real_flow_df.index)
    s_mat = s_matrix_df.loc[common_idx, common_idx].values
    t_real = real_flow_df.loc[common_idx, common_idx].values

    t_real_no_diag = t_real.copy()
    np.fill_diagonal(t_real_no_diag, 0)
    o_i = np.nansum(t_real_no_diag, axis=1)

    prob_score = np.exp(-L_param * s_mat)
    np.fill_diagonal(prob_score, 0)

    row_sums = np.nansum(prob_score, axis=1)
    row_sums[row_sums == 0] = 1e-12
    prob_matrix = prob_score / row_sums[:, np.newaxis]

    t_hat = o_i[:, np.newaxis] * prob_matrix
    return pd.DataFrame(t_hat, index=common_idx, columns=common_idx)


def main():
    BASE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    city_files = sorted(BASE_DISTANCE_PATH.glob("*.csv"))
    print(
        f"Preparing {len(city_files)} city path-opportunity matrices "
        f"(tolerance: {PATH_TOLERANCE})"
    )

    for dist_file in city_files:
        start_time = time.time()
        city = dist_file.stem
        print("\n" + "-" * 40)
        print(f"City: {city}")

        pop_file = BASE_POP_PATH / f"{city}.csv"
        save_path = BASE_OUTPUT_PATH / f"{city}_path_opportunity_matrix.csv"

        if save_path.exists():
            print(f"{city} already exists; skipping.")
            continue

        try:
            dist_df = read_wide_matrix(dist_file)
            b_ids = dist_df.index.tolist()
            dist_mat = dist_df.to_numpy(dtype=float)

            pop_df = pd.read_csv(pop_file, dtype={"origin_geoid": str})
            validate_columns(pop_df, REQUIRED_POP_COLUMNS, pop_file)
            pop_df["origin_geoid"] = pop_df["origin_geoid"].astype(str)
            pop_aligned = pop_df.set_index("origin_geoid").reindex(b_ids).fillna(0)
            pop_vec = pd.to_numeric(
                pop_aligned["Tot_Population_ACS_15_19"], errors="coerce"
            ).fillna(0).to_numpy()

            opp_mat = compute_path_based_matrix_matrixized(dist_mat, pop_vec, PATH_TOLERANCE)

            opp_df = pd.DataFrame(opp_mat, index=b_ids, columns=b_ids)
            opp_df.index.name = "origin_geoid"
            opp_df.to_csv(save_path, encoding="utf-8-sig")

            del dist_mat, pop_vec, opp_mat, opp_df, dist_df, pop_df, pop_aligned
            gc.collect()

            elapsed = (time.time() - start_time) / 60
            print(f"Completed in {elapsed:.2f} minutes.")

        except Exception as exc:
            print(f"City {city} failed: {exc}")
            traceback.print_exc()

    print("\nAll city path-opportunity matrices are complete.")


if __name__ == "__main__":
    main()

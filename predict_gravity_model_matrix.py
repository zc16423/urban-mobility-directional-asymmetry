from pathlib import Path
import gc
import time
import traceback
import warnings

import numpy as np
import pandas as pd
import scipy.optimize as opt


warnings.filterwarnings("ignore")

ROOT_DIR = Path(__file__).resolve().parent
BASE_OD_PATH = ROOT_DIR / "basic_data" / "real_year"
BASE_DISTANCE_PATH = ROOT_DIR / "city_distance_matrices"
BASE_POP_PATH = ROOT_DIR / "city_population_poi"
BASE_OUTPUT_PATH = ROOT_DIR / "basic_data" / "gravity_year"
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


def load_dest_pop(pop_file, b_ids):
    pop_df = pd.read_csv(pop_file, dtype={"origin_geoid": str})
    validate_columns(pop_df, REQUIRED_POP_COLUMNS, pop_file)
    pop_df["origin_geoid"] = pop_df["origin_geoid"].astype(str)
    pop_aligned = pop_df.set_index("origin_geoid").reindex(b_ids).fillna(0)
    return pd.to_numeric(
        pop_aligned["Tot_Population_ACS_15_19"], errors="coerce"
    ).fillna(0).to_numpy().reshape(1, -1)


def predict_gravity_production_constrained(dest_pop, distance_matrix, real_outflows, beta_param):
    """
    Production-constrained gravity model.

    T_ij = O_i * (P_j * exp(-beta * d_ij)) / sum_k(P_k * exp(-beta * d_ik)).
    The diagonal is forced to zero before row normalization.
    """
    decay = np.exp(-beta_param * distance_matrix)
    scores = dest_pop * decay
    np.fill_diagonal(scores, 0)

    row_sums = scores.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1e-10
    probs = scores / row_sums

    return real_outflows * probs


def objective_function_gravity(beta_param, dest_pop_vec, distance_matrix, real_interzonal_od, real_outflows):
    """Find the beta that minimizes RMSE on non-diagonal observed flows."""
    if beta_param <= 0:
        return 1e10

    try:
        pred_matrix = predict_gravity_production_constrained(
            dest_pop_vec, distance_matrix, real_outflows, beta_param
        )
        mse = np.mean((real_interzonal_od - pred_matrix) ** 2)
        return np.sqrt(mse)
    except Exception:
        return 1e10


def compute_metrics_fast(y_true, y_pred):
    valid = (y_true > 0) | (y_pred > 0)
    if np.sum(valid) <= 1:
        return np.nan, np.nan, np.nan

    yt, yp = y_true[valid], y_pred[valid]
    mae = np.mean(np.abs(yt - yp))
    rmse = np.sqrt(np.mean((yt - yp) ** 2))
    if np.std(yt) == 0 or np.std(yp) == 0:
        corr = 0
    else:
        corr = np.corrcoef(yt, yp)[0, 1]
    return mae, rmse, corr


def fit_city_gravity_model(city, od_file):
    start_time = time.time()
    print("\n" + "=" * 50)
    print(f"Processing city: {city}")

    city_dist_file = BASE_DISTANCE_PATH / f"{city}.csv"
    city_pop_file = BASE_POP_PATH / f"{city}.csv"
    save_path = BASE_OUTPUT_PATH / f"{city}.csv"

    print("  Reading base matrices...")
    dist_df = read_wide_matrix(city_dist_file)
    b_ids = dist_df.index.tolist()
    dist_mat = dist_df.to_numpy(dtype=float)

    if np.nanmean(dist_mat) > 5000:
        print("  Distance values are large; converting to kilometers for exponential decay.")
        dist_mat = dist_mat / 1000.0

    dest_pop_vec = load_dest_pop(city_pop_file, b_ids)

    real_od_df = read_wide_matrix(od_file)
    real_mat = real_od_df.reindex(index=b_ids, columns=b_ids).fillna(0).to_numpy(dtype=float)

    diag_vals = np.diag(real_mat)
    real_interzonal = real_mat.copy()
    np.fill_diagonal(real_interzonal, 0)
    real_outflows = real_interzonal.sum(axis=1).reshape(-1, 1)

    best_res = None
    best_f = np.inf
    initial_guesses = [0.01, 0.1, 0.5, 1.0, 2.0]
    bounds = [(1e-5, 10.0)]

    for start_beta in initial_guesses:
        try:
            res = opt.minimize(
                objective_function_gravity,
                x0=[start_beta],
                args=(dest_pop_vec, dist_mat, real_interzonal, real_outflows),
                method="L-BFGS-B",
                bounds=bounds,
            )
            if res.fun < best_f:
                best_res, best_f = res, res.fun
        except Exception:
            continue

    beta_opt = best_res.x[0] if best_res is not None else 0.1

    t_pred_interzonal = predict_gravity_production_constrained(
        dest_pop_vec, dist_mat, real_outflows, beta_opt
    )
    mae, rmse, corr = compute_metrics_fast(real_interzonal, t_pred_interzonal)

    final_pred_matrix = t_pred_interzonal + np.diag(diag_vals)
    output_df = pd.DataFrame(final_pred_matrix, index=b_ids, columns=b_ids).round(6)
    output_df.index.name = "origin_geoid"
    output_df.to_csv(save_path, encoding="utf-8-sig")

    elapsed = (time.time() - start_time) / 60
    print(
        f"Completed {city}: beta={beta_opt:.4f}, mae={mae:.2f}, "
        f"rmse={rmse:.2f}, corr={corr:.4f}, time={elapsed:.1f} minutes"
    )

    del dest_pop_vec, dist_mat, real_mat, real_interzonal, real_outflows, output_df
    gc.collect()


def main():
    BASE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    od_files = sorted(BASE_OD_PATH.glob("*.csv"))
    print(f"Starting production-constrained gravity fitting for {len(od_files)} city files.")

    for od_file in od_files:
        city = od_file.stem
        try:
            fit_city_gravity_model(city, od_file)
        except Exception as exc:
            print(f"City {city} failed: {exc}")
            traceback.print_exc()

    print("\nAll city gravity matrices are complete.")


if __name__ == "__main__":
    main()

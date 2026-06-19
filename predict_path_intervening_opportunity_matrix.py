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
BASE_OD_PATH = ROOT_DIR / "basic_data" / "real_day"
BASE_POP_PATH = ROOT_DIR / "city_population_poi"
BASE_OPPORTUNITY_PATH = ROOT_DIR / "basic_data" / "path_intervening_opportunity_matrices"
BASE_OUTPUT_PATH = ROOT_DIR / "basic_data" / "choice_iom_day"
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


def load_destination_acs_counts(pop_file, b_ids):
    pop_df = pd.read_csv(pop_file, dtype={"origin_geoid": str})
    validate_columns(pop_df, REQUIRED_POP_COLUMNS, pop_file)
    pop_df["origin_geoid"] = pop_df["origin_geoid"].astype(str)
    pop_aligned = pop_df.set_index("origin_geoid").reindex(b_ids).fillna(0)
    return pd.to_numeric(
        pop_aligned["Tot_Population_ACS_15_19"], errors="coerce"
    ).fillna(0).to_numpy().reshape(1, -1)


def discover_city_od_folders():
    if not BASE_OD_PATH.exists():
        return []

    folders = [path for path in BASE_OD_PATH.iterdir() if path.is_dir()]
    if folders:
        return sorted(folders, key=lambda path: path.name)

    return sorted({path.with_suffix("") for path in BASE_OD_PATH.glob("*.csv")}, key=lambda path: path.name)


def predict_interzonal_od_fast(origin_outflows, destination_pop, opportunity_matrix, lambda_param):
    """
    Generate production-constrained path-opportunity predictions.

    The diagonal is excluded so the model predicts cross-CBG flows only.
    """
    lambda_s = np.clip(-lambda_param * opportunity_matrix, -700, 700)
    lambda_sm = np.clip(-lambda_param * (opportunity_matrix + destination_pop), -700, 700)

    prob_score = np.maximum(0, np.exp(lambda_s) - np.exp(lambda_sm))
    np.fill_diagonal(prob_score, 0)

    row_sums = np.sum(prob_score, axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1e-12
    prob_norm = prob_score / row_sums

    return origin_outflows * prob_norm


def objective_function_fast(lambda_param, origin_outflows, destination_pop, opportunity_matrix, real_interzonal_od):
    """Minimize RMSE between predicted and observed interzonal flows."""
    if lambda_param <= 0:
        return 1e10

    try:
        pred_interzonal = predict_interzonal_od_fast(
            origin_outflows, destination_pop, opportunity_matrix, lambda_param
        )
        diff = real_interzonal_od - pred_interzonal
        mse = np.mean(diff ** 2)
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
    corr = np.corrcoef(yt, yp)[0, 1] if len(yt) > 1 else np.nan
    return mae, rmse, corr


def fit_daily_city(city_path):
    start_time = time.time()
    city = city_path.name
    print("\n" + "=" * 50)
    print(f"Fitting city: {city}")

    pop_file = BASE_POP_PATH / f"{city}.csv"
    opp_file = BASE_OPPORTUNITY_PATH / f"{city}_path_opportunity_matrix.csv"
    city_out_dir = BASE_OUTPUT_PATH / city
    city_matrix_dir = city_out_dir / "predicted_matrices"
    city_matrix_dir.mkdir(parents=True, exist_ok=True)

    if not opp_file.exists():
        print(f"Missing opportunity matrix: {opp_file}")
        return

    opp_df = read_wide_matrix(opp_file).astype(float)
    opp_mat = opp_df.to_numpy(dtype=float)
    b_ids = opp_df.index.tolist()

    destination_acs = load_destination_acs_counts(pop_file, b_ids)

    if city_path.is_dir():
        od_files = sorted(city_path.glob("*.csv"))
    else:
        od_files = [city_path.with_suffix(".csv")]

    city_results = []
    print(f"  Found {len(od_files)} OD files.")

    for idx, od_file in enumerate(od_files):
        real_od_df = read_wide_matrix(od_file)
        real_mat = real_od_df.reindex(index=b_ids, columns=b_ids).fillna(0).to_numpy(dtype=float)

        real_mat_no_diag = real_mat.copy()
        np.fill_diagonal(real_mat_no_diag, 0)

        origin_outflows = np.sum(real_mat_no_diag, axis=1, keepdims=True)

        best_res = None
        best_f = np.inf
        opts = {"maxiter": 1000, "ftol": 1e-9}

        for start_l in [0.0001, 0.001, 0.01]:
            try:
                res = opt.minimize(
                    objective_function_fast,
                    x0=[start_l],
                    args=(origin_outflows, destination_acs, opp_mat, real_mat_no_diag),
                    method="L-BFGS-B",
                    bounds=[(1e-9, 5.0)],
                    options=opts,
                )
                if res.fun < best_f:
                    best_res, best_f = res, res.fun
            except Exception:
                continue

        lambda_opt = best_res.x[0] if best_res is not None else 0.001

        pred_matrix = predict_interzonal_od_fast(origin_outflows, destination_acs, opp_mat, lambda_opt)

        mask = ~np.eye(pred_matrix.shape[0], dtype=bool)
        mae, rmse, corr = compute_metrics_fast(real_mat_no_diag[mask], pred_matrix[mask])

        final_pred_df = pd.DataFrame(pred_matrix, index=b_ids, columns=b_ids).round(4)
        final_pred_df.index.name = "origin_geoid"
        final_pred_df.to_csv(city_matrix_dir / f"PathIO_{od_file.name}", encoding="utf-8-sig")

        city_results.append(
            {
                "filename": od_file.name,
                "lambda": lambda_opt,
                "mae": mae,
                "rmse": rmse,
                "correlation": corr,
                "total_interzonal_flow": np.sum(real_mat_no_diag),
            }
        )

        if (idx + 1) % 20 == 0:
            print(f"    Progress: {idx + 1}/{len(od_files)} | Lambda: {lambda_opt:.6f} | Corr: {corr:.4f}")
            gc.collect()

    report_path = city_out_dir / f"{city}_PathIO_Report.csv"
    pd.DataFrame(city_results).to_csv(report_path, index=False, encoding="utf-8-sig")

    del opp_mat, destination_acs, city_results
    gc.collect()

    elapsed = (time.time() - start_time) / 60
    print(f"City {city} completed in {elapsed:.1f} minutes.")


def main():
    BASE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    city_paths = discover_city_od_folders()
    print(f"Starting path-opportunity daily fitting for {len(city_paths)} city inputs.")

    for city_path in city_paths:
        try:
            fit_daily_city(city_path)
        except Exception as exc:
            print(f"City {city_path.name} failed: {exc}")
            traceback.print_exc()

    print("\nAll path-opportunity city fitting is complete.")


if __name__ == "__main__":
    main()

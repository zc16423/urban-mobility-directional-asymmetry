import os
import time

import numpy as np
import pandas as pd


def calculate_gini(flows):
    """
    Calculate the Gini coefficient for positive flow values.
    """
    flows = np.array(flows).flatten()
    flows = flows[flows > 0]

    if len(flows) < 2:
        return 0.0

    flows_sorted = np.sort(flows)
    n = len(flows_sorted)
    index = np.arange(1, n + 1)
    gini = (2 * np.sum(index * flows_sorted)) / (n * np.sum(flows_sorted)) - (n + 1) / n

    return max(0.0, gini)


def calculate_cv(flows):
    """
    Calculate the coefficient of variation for positive flow values.
    """
    flows = np.array(flows).flatten()
    flows = flows[flows > 0]

    if len(flows) < 2:
        return 0.0

    mean_val = np.mean(flows)
    if mean_val == 0:
        return 0.0

    return np.std(flows) / mean_val


def validate_matrix(df, source_path):
    if df.empty:
        raise ValueError(f"{source_path} is empty.")
    if df.index.empty or df.columns.empty:
        raise ValueError(f"{source_path} must contain origin identifiers and destination columns.")


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(SCRIPT_DIR, "real_year")
output_folder = SCRIPT_DIR
os.makedirs(output_folder, exist_ok=True)

city_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
city_summary = []

print(f"Starting city-level metric calculation for {len(city_files)} files.")

for city_file in city_files:
    start_time = time.time()
    city = os.path.splitext(city_file)[0]
    city_path = os.path.join(input_folder, city_file)

    try:
        df = pd.read_csv(city_path, index_col=0)
        validate_matrix(df, city_path)

        matrix = df.apply(pd.to_numeric, errors="coerce").fillna(0).values

        if matrix.shape[0] != matrix.shape[1]:
            print(f"WARNING: {city} matrix is not square ({matrix.shape}); truncating to the smaller dimension.")
            min_dim = min(matrix.shape)
            matrix = matrix[:min_dim, :min_dim]

        np.fill_diagonal(matrix, 0)

        matrix_t = matrix.T
        diff_matrix = np.abs(matrix - matrix_t)
        sum_matrix = matrix + matrix_t

        total_diff_sum = np.sum(diff_matrix)
        total_flow_sum = np.sum(sum_matrix)

        if total_flow_sum > 0:
            city_asymmetry = total_diff_sum / total_flow_sum
        else:
            city_asymmetry = 0

        all_flows = matrix.flatten()

        gini = calculate_gini(all_flows)
        cv = calculate_cv(all_flows)

        total_pairs = np.count_nonzero(matrix)
        total_volume = np.sum(matrix)

        city_summary.append({
            "city": city,
            "total_flow_volume": total_volume,
            "active_links_count": total_pairs,
            "overall_mobility_asymmetry": city_asymmetry,
            "mobility_gini_coefficient": gini,
            "mobility_coefficient_variation": cv,
        })

        elapsed = time.time() - start_time
        print(f"{city}: asymmetry={city_asymmetry:.4f}, Gini={gini:.4f} ({elapsed:.2f}s)")

    except Exception as exc:
        print(f"ERROR: failed to process {city}: {exc}")

result_df = pd.DataFrame(city_summary)
result_df = result_df.sort_values(by="overall_mobility_asymmetry", ascending=False)

output_path = os.path.join(output_folder, "Fig1A_City_Level_Metrics.csv")
result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n" + "=" * 50)
print(f"Calculation complete. Output saved to: {output_path}")
print("Metrics: overall_mobility_asymmetry, mobility_gini_coefficient, mobility_coefficient_variation")
print("=" * 50)

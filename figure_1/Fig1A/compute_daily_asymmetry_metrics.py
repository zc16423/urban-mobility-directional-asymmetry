import os
import time
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


def calculate_gini(flows):
    """Calculate Gini coefficient for positive flows."""
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
    """Calculate coefficient of variation (CV) for positive flows."""
    flows = np.array(flows).flatten()
    flows = flows[flows > 0]
    if len(flows) < 2 or np.mean(flows) == 0:
        return 0.0
    return np.std(flows) / np.mean(flows)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_root_folder = os.path.join(script_dir, "real_year")
    output_folder = script_dir
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(input_root_folder):
        print(f"Input directory not found: {input_root_folder}. Raw daily matrices required.")
        return

    city_folders = [
        d for d in os.listdir(input_root_folder)
        if os.path.isdir(os.path.join(input_root_folder, d))
    ]

    city_stats_summary = []
    print(f"Processing daily data for {len(city_folders)} cities...")

    for city_name in sorted(city_folders):
        city_start_time = time.time()
        city_dir_path = os.path.join(input_root_folder, city_name)
        daily_files = [f for f in os.listdir(city_dir_path) if f.endswith(".csv")]
        print(f"City: {city_name} ({len(daily_files)} daily files)")

        daily_metrics_list = []

        for i, day_file in enumerate(sorted(daily_files)):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(daily_files)}...")

            day_path = os.path.join(city_dir_path, day_file)
            try:
                df = pd.read_csv(day_path, index_col=0)
                matrix = df.apply(pd.to_numeric, errors='coerce').fillna(0).values

                if matrix.shape[0] != matrix.shape[1]:
                    min_dim = min(matrix.shape)
                    matrix = matrix[:min_dim, :min_dim]

                np.fill_diagonal(matrix, 0)

                matrix_t = matrix.T
                diff_matrix = np.abs(matrix - matrix_t)
                sum_matrix = matrix + matrix_t

                total_diff = np.sum(diff_matrix)
                total_flow = np.sum(sum_matrix)

                if total_flow > 0:
                    daily_asymmetry = total_diff / total_flow
                else:
                    daily_asymmetry = np.nan

                all_flows = matrix.flatten()
                if np.sum(all_flows) > 0:
                    daily_gini = calculate_gini(all_flows)
                    daily_cv = calculate_cv(all_flows)
                else:
                    daily_gini = np.nan
                    daily_cv = np.nan

                daily_metrics_list.append({
                    "day_asymmetry": daily_asymmetry,
                    "day_gini": daily_gini,
                    "day_cv": daily_cv,
                    "daily_total_flow": total_flow / 2.0
                })

            except Exception as e:
                print(f"   Warning: failed to read {day_file}: {e}")
                continue

        if daily_metrics_list:
            df_metrics = pd.DataFrame(daily_metrics_list)
            stats = {
                "city_name": city_name,
                "days_count": len(df_metrics),
                "asymmetry_mean": df_metrics["day_asymmetry"].mean(),
                "asymmetry_std": df_metrics["day_asymmetry"].std(),
                "gini_mean": df_metrics["day_gini"].mean(),
                "gini_std": df_metrics["day_gini"].std(),
                "cv_mean": df_metrics["day_cv"].mean(),
                "cv_std": df_metrics["day_cv"].std(),
                "daily_flow_mean": df_metrics["daily_total_flow"].mean()
            }
            city_stats_summary.append(stats)
            elapsed = time.time() - city_start_time
            print(f"Completed {city_name} in {elapsed:.1f}s: Mean Asymmetry = {stats['asymmetry_mean']:.4f} +/- {stats['asymmetry_std']:.4f}")
        else:
            print(f"No valid data for {city_name}.")

    if city_stats_summary:
        final_df = pd.DataFrame(city_stats_summary)
        final_df = final_df.sort_values(by="asymmetry_mean", ascending=False)
        output_path = os.path.join(output_folder, "Fig1A_Daily_Stats_With_ErrorBars.csv")
        final_df.to_csv(output_path, index=False)
        print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
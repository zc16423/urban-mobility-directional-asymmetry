import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "basic_data", "Final_Regression_Dataset.csv")
OUTPUT_DIR = SCRIPT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

feature_cols = [
    "Delta_Race_White",
    "Delta_Poverty",
    "Delta_Edu_College",
    "Delta_POI_Count",
    "Delta_Age_65plus",
    "Delta_Housing_Owner",
    "Delta_Job_Density",
    "Delta_Pop_Density",
    "Log_Distance",
]

city_col = "city"
origin_col = "origin_block"
destination_col = "destination_block"
target_raw_col = "Realization_Ratio_R"
target_col = "Log_R_eps"

REQUIRED_COLUMNS = {
    city_col,
    origin_col,
    destination_col,
    target_raw_col,
    *feature_cols,
}


def validate_columns(df, required_columns, source_name):
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"{source_name} is missing required columns: {missing}")


print("Step 1: Loading data...")
df = pd.read_csv(INPUT_FILE)
validate_columns(df, REQUIRED_COLUMNS, INPUT_FILE)

df[target_raw_col] = pd.to_numeric(df[target_raw_col], errors="coerce")

for col in feature_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df[df[target_raw_col] >= 0]
df = df.dropna(subset=[city_col, target_raw_col] + feature_cols)

print(f"Rows after cleaning: {len(df):,}")
print(f"Nonzero R rows: {(df[target_raw_col] > 0).sum():,}")
print(f"Zero R rows: {(df[target_raw_col] == 0).sum():,}")
print(f"Share of zero R: {(df[target_raw_col] == 0).mean():.3f}")

expected_n = 4788895
if len(df) != expected_n:
    print(f"WARNING: cleaned row count is {len(df):,}, not {expected_n:,}.")
    print("This may be due to missing feature values removed by dropna().")

positive_R = df.loc[df[target_raw_col] > 0, target_raw_col]

if len(positive_R) == 0:
    raise ValueError("No positive R values found. Cannot define epsilon.")

min_positive_R = positive_R.min()
epsilon = 0.5 * min_positive_R

df[target_col] = np.log10(df[target_raw_col] + epsilon)

print("\n--- Log transform ---")
print(f"Min positive R: {min_positive_R}")
print(f"Epsilon: {epsilon}")
print(f"{target_col} range: [{df[target_col].min():.4f}, {df[target_col].max():.4f}]")

with open(os.path.join(OUTPUT_DIR, "log_transform_epsilon.txt"), "w", encoding="utf-8") as f:
    f.write(f"min_positive_R={min_positive_R}\n")
    f.write(f"epsilon={epsilon}\n")
    f.write("target=log10(R + epsilon)\n")

print("\nStep 2: Train-validation split...")

X = df[feature_cols]
y = df[target_col]

X_train, X_val, y_train, y_val, city_train, city_val = train_test_split(
    X,
    y,
    df[city_col],
    test_size=0.2,
    random_state=42,
    stratify=df[city_col],
)

print(f"Training rows: {len(X_train):,}")
print(f"Validation rows: {len(X_val):,}")

print("\nStep 3: Training random forest...")

rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,
    min_samples_leaf=50,
    max_features="sqrt",
    oob_score=True,
    bootstrap=True,
    n_jobs=-1,
    random_state=42,
    verbose=1,
)

rf.fit(X_train, y_train)

print(f"OOB R2 score: {rf.oob_score_:.4f}")
print(f"Validation R2 score: {rf.score(X_val, y_val):.4f}")

joblib.dump(rf, os.path.join(OUTPUT_DIR, "rf_fig4B_global_model.pkl"))

print("\nStep 4: Computing feature importance...")

feat_imp = pd.DataFrame({
    "Feature": feature_cols,
    "MDI_Importance": rf.feature_importances_,
})

N_PERM_SAMPLE = 1000000

if len(X_val) > N_PERM_SAMPLE:
    rng = np.random.RandomState(42)
    perm_indices = rng.choice(len(X_val), N_PERM_SAMPLE, replace=False)
    X_perm = X_val.iloc[perm_indices]
    y_perm = y_val.iloc[perm_indices]
    print(f"Using validation subsample for permutation importance: {N_PERM_SAMPLE:,} rows")
else:
    X_perm = X_val
    y_perm = y_val
    print(f"Using full validation set for permutation importance: {len(X_val):,} rows")

perm_result = permutation_importance(
    rf,
    X_perm,
    y_perm,
    n_repeats=10,
    random_state=42,
    n_jobs=-1,
    scoring="neg_mean_squared_error",
)

feat_imp["Permutation_Importance_Mean"] = perm_result.importances_mean
feat_imp["Permutation_Importance_SD"] = perm_result.importances_std

feat_imp = feat_imp.sort_values(
    by="Permutation_Importance_Mean",
    ascending=False,
)

feat_imp.to_csv(
    os.path.join(OUTPUT_DIR, "Fig4B_feature_importance_results.csv"),
    index=False,
)

print("\n--- Feature importance ranking ---")
print(feat_imp)

cols_to_save = [
    city_col,
    origin_col,
    destination_col,
] + feature_cols + [target_raw_col, target_col]

existing_cols_to_save = [c for c in cols_to_save if c in df.columns]

df[existing_cols_to_save].to_csv(
    os.path.join(OUTPUT_DIR, "Fig4B_processed_data_all_R_ge_0.csv"),
    index=False,
)

print("\nFig. 4B analysis complete.")

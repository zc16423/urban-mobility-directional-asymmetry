# Supplementary Information Analysis & Replication Guide

This directory contains reproduction scripts and derived datasets for analyses presented in the Supplementary Information (SI).

## Directory Structure

```text
supplementary_information/
├── README.md                                          # Documentation guide
│
├── descriptive_statistics/                            # Demographic counts (Fig S1) & flow statistics (Fig S2)
│   ├── plot_figS1_cbg_counts.py                       # Reproduces Fig S1 (CBG counts across 16 MSAs)
│   ├── FigS1_cbg_demographic_counts.csv               # CBG demographic counts per MSA
│   ├── FigS1.svg                                      # Vector output
│   ├── FigureS2_city_paired_results.csv               # Paired city metrics for Fig S2
│   ├── FigureS2_descriptive_statistics.csv            # Summary statistics for Fig S2
│   ├── FigureS2_statistical_report.txt                # Statistical analysis report
│   └── FigureS2_statistical_tests.csv                 # Statistical test results
│
├── threshold_sensitivity/                             # Poverty & racial threshold sensitivity analyses
│   ├── plot_threshold_sensitivity_blockage.py         # Reproduces Fig S4 (blockage rate across 9 thresholds)
│   ├── plot_threshold_sensitivity_R.py                # Reproduces Fig S5 (realization ratio R across thresholds)
│   ├── plot_threshold_sensitivity_FA.py               # Reproduces Figs S7, S8 (flow asymmetry sensitivity)
│   ├── threshold_sensitivity_blockage_data.csv        # Blockage rates across thresholds
│   ├── threshold_sensitivity_R_data.csv               # Realization ratios across thresholds
│   ├── threshold_sensitivity_FA_data.csv              # FA values across thresholds
│   ├── threshold_sensitivity_summary.csv              # Summary table
│   ├── threshold_sensitivity_blockage.svg             # Vector output
│   ├── threshold_sensitivity_R.svg                    # Vector output
│   └── threshold_sensitivity_FA.svg                   # Vector output
│
├── rf_lomao_validation/                               # Cross-metropolitan holdout & permutation importance
│   ├── plot_rf_validation_comparison.py               # Reproduces Figs S9, S10
│   ├── plot_data_metropolitan_holdout.csv             # Held-out R2 across 16 MSAs (16 LOMAO folds)
│   ├── plot_data_permutation_importance.csv           # Permutation feature importance (mean & SD)
│   ├── metropolitan_holdout_performance.svg           # Vector output
│   └── permutation_importance_comparison.svg          # Vector output
│
└── topological_rf_importance/                         # Random Forest on topological baselines (IOM & Choice-IOM)
    ├── plot_topological_rf_importance.py              # Reproduces Figs S11 (IOM) and S12 (Choice-IOM)
    ├── iom_feature_importance_results.csv             # Feature importance under IOM
    ├── choice_iom_feature_importance_results.csv      # Feature importance under Choice-IOM (tau = 0.5)
    ├── FigS11_IOM_Feature_Importance.svg              # Vector output
    └── FigS12_Choice_IOM_Feature_Importance.svg       # Vector output
```

## Mapping to Supplementary Information

| SI Item | Content | Script | Input Data | Data Source |
| :--- | :--- | :--- | :--- | :--- |
| **Fig S1** | CBG demographic distributions (HPM & LPW) | `descriptive_statistics/plot_figS1_cbg_counts.py` | `FigS1_cbg_demographic_counts.csv` | U.S. Census ACS 2015–2019 |
| **Fig S2** | City-level paired asymmetry statistics | Provided in `descriptive_statistics/` | `FigureS2_*.csv` | Derived mobility metrics |
| **Fig S3** | Flow distributions for 16 metropolitan areas | `figure_3/Fig3D/Fig3D_16_cities/Fig3D_16_cities.py` | `figure_3/Fig3D/Fig3D_16_cities/` | Aggregated flow distributions |
| **Fig S4** | Blockage rate threshold sensitivity | `threshold_sensitivity/plot_threshold_sensitivity_blockage.py` | `threshold_sensitivity_blockage_data.csv` | Derived sensitivity table |
| **Fig S5** | Realization ratio $R$ threshold sensitivity | `threshold_sensitivity/plot_threshold_sensitivity_R.py` | `threshold_sensitivity_R_data.csv` | Derived sensitivity table |
| **Figs S7, S8** | Flow asymmetry ($FA$) threshold sensitivity | `threshold_sensitivity/plot_threshold_sensitivity_FA.py` | `threshold_sensitivity_FA_data.csv` | Derived sensitivity table |
| **Fig S9** | Cross-metropolitan LOMAO holdout $R^2$ | `rf_lomao_validation/plot_rf_validation_comparison.py` | `plot_data_metropolitan_holdout.csv` | Model validation summary |
| **Fig S10** | Permutation feature importance across folds | `rf_lomao_validation/plot_rf_validation_comparison.py` | `plot_data_permutation_importance.csv` | Model validation summary |
| **Fig S11** | Random Forest feature importance under IOM | `topological_rf_importance/plot_topological_rf_importance.py` | `iom_feature_importance_results.csv` | Model training output |
| **Fig S12** | Random Forest feature importance under Choice-IOM | `topological_rf_importance/plot_topological_rf_importance.py` | `choice_iom_feature_importance_results.csv` | Model training output |

## Reproduction Commands

Run from the repository root:

```bash
# Fig S1: CBG demographic distribution
python supplementary_information/descriptive_statistics/plot_figS1_cbg_counts.py

# Fig S3: Flow probability distributions across 16 MSAs
python figure_3/Fig3D/Fig3D_16_cities/Fig3D_16_cities.py

# Figs S4, S5, S7, S8: Threshold sensitivity analyses
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_blockage.py
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_R.py
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_FA.py

# Figs S9, S10: Cross-metropolitan LOMAO validation
python supplementary_information/rf_lomao_validation/plot_rf_validation_comparison.py

# Figs S11, S12: Topological predictor importance
python supplementary_information/topological_rf_importance/plot_topological_rf_importance.py
```

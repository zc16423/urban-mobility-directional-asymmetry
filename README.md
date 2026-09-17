# Directional Asymmetry in Urban Mobility

Replication code and data for:
> **Directional asymmetry in urban mobility reveals semi-permeable racialized segregation** (PNAS).

This repository contains scripts and derived datasets to reproduce the figures and quantitative analyses in the manuscript and Supplementary Information (SI).

## Data

1. **Census Demographic & Socioeconomic Attributes**: Census Block Group (CBG) attributes (total population, racial composition, poverty rates, and geographic coordinates) are derived from the U.S. Census Bureau American Community Survey (ACS) 2015–2019 5-Year Estimates. Curated attributes for the 16 metropolitan areas are provided in `cbg_socioeconomic_attributes/`.
2. **Mobility Data**: Aggregated origin-destination (OD) flows were constructed from 2019 SafeGraph mobile device records across 16 U.S. metropolitan areas. Raw device-level and trip-level mobility records are subject to third-party academic licensing through [Dewey Data](https://www.deweydata.io/) and cannot be redistributed directly.
3. **Derived Reproduction Data**: Aggregated OD realization tables, binned summary metrics, model comparison tables, and sensitivity data are included directly in this repository to reproduce all figures without requiring raw SafeGraph records.

## Repository Structure

```text
urban-mobility-directional-asymmetry/
├── README.md                                          # Replication guide
├── LICENSE                                            # MIT License
├── .gitignore                                         # Git ignore rules
│
├── cbg_socioeconomic_attributes/                      # CBG demographic & socioeconomic attributes (16 cities)
│   ├── Atlanta.csv
│   ├── Boston.csv
│   └── ... (16 metropolitan areas)
│
├── figure_1/                                          # Figure 1: Spatial patterns & flow asymmetry
│   ├── Fig1A/                                         # 16-MSA mobility asymmetry map
│   │   ├── Fig1A.py
│   │   ├── Fig1A.csv
│   │   ├── Fig1A_Pop_Academic.svg
│   │   ├── compute_city_mobility_asymmetry_metrics.py
│   │   ├── compute_daily_asymmetry_metrics.py
│   │   └── cb_2018_us_state_20m/
│   ├── Fig1BC/                                        # Asymmetry vs poverty and race
│   │   ├── Fig1BC.py
│   │   ├── Fig1BC.csv
│   │   ├── Fig1B.svg
│   │   └── Fig1C.svg
│   ├── Fig1D/                                         # Flow ratio distribution (Boston)
│   │   ├── Fig1D.py
│   │   ├── Fig1D.csv
│   │   ├── Fig1D.svg
│   │   └── appendix/plot_appendix_ring.py
│   └── Fig1EF/                                        # Flow maps (Boston)
│       ├── Fig1EF.py
│       ├── Fig1E.csv
│       ├── Fig1F.csv
│       ├── Fig1EF_attributes.csv
│       ├── Fig1E.svg
│       └── Fig1F.svg
│
├── figure_2/                                          # Figure 2: Observed vs Gravity baseline
│   ├── Fig2B.py
│   ├── Fig2C.py
│   ├── Fig2BC.csv
│   ├── Fig2B.svg
│   ├── Fig2C.svg
│   └── Fig2BC_city/                                   # City-specific flow share distributions
│       ├── HPM_to_LPW/
│       └── LPW_to_HPM/
│
├── figure_3/                                          # Figure 3: Realization ratio R & blockage rate
│   ├── Fig3A/                                         # Realization ratio R across 16 cities
│   │   ├── Fig3A.py
│   │   ├── Fig3A_year.csv
│   │   ├── Fig3A_day/
│   │   └── Fig3A.svg
│   ├── Fig3B/                                         # ECDF of log(R) and blockage rate inset
│   │   ├── Fig3B.py
│   │   ├── Fig3B_active_links.csv.gz
│   │   ├── Fig3B_blockage_stats.csv
│   │   └── Fig3B.svg
│   ├── Fig3C/                                         # Observed vs Gravity asymmetry
│   │   ├── Fig3C.py
│   │   ├── Fig3C_gravity_year.csv
│   │   ├── Fig3C_real_year.csv
│   │   ├── Fig3C_real_day/
│   │   └── Fig3C.svg
│   └── Fig3D/                                         # Flow distributions (4 cities & 16 cities)
│       ├── Fig3D.py
│       ├── Fig3D.svg
│       ├── gravity/
│       ├── real/
│       └── Fig3D_16_cities/
│           ├── Fig3D_16_cities.py
│           ├── Fig3D_16_city_real_vs_gravity.svg
│           ├── gravity/
│           └── real/
│
├── figure_4/                                          # Figure 4: Multimodel comparison & Random Forest predictors
│   ├── Fig4A/                                         # Gravity vs IOM vs Choice-IOM (tau = 0.5)
│   │   ├── Fig4A.py
│   │   ├── Fig4A_real_gravity.csv
│   │   ├── Fig4A_real_iom.csv
│   │   ├── Fig4A_real_choice.csv
│   │   └── Fig4A.svg
│   ├── Fig4B/                                         # Random Forest feature importance
│   │   ├── Fig4B.py
│   │   ├── Fig4B_feature_importance_results.csv
│   │   ├── Fig4B.svg
│   │   ├── build_regression_dataset.py
│   │   ├── compute_positive_realization_od_pairs.py
│   │   └── run_random_forest_feature_importance.py
│   └── Fig4CD/                                        # Binned median curves (Racial gap & Density ratio)
│       ├── Fig4CD.py
│       ├── Fig4CD_data/
│       └── images/
│           ├── Figure_4C.svg
│           └── Figure_4D.svg
│
├── supplementary_information/                         # Supplementary Information replication materials
│   ├── README.md
│   ├── descriptive_statistics/                        # Demographic counts (Fig S1) & flow statistics (Fig S2)
│   │   ├── plot_figS1_cbg_counts.py
│   │   ├── FigS1_cbg_demographic_counts.csv
│   │   ├── FigS1.svg
│   │   └── FigureS2_*.csv
│   ├── threshold_sensitivity/                         # Sensitivity across poverty/racial thresholds (Figs S4, S5, S7, S8)
│   │   ├── plot_threshold_sensitivity_blockage.py
│   │   ├── plot_threshold_sensitivity_R.py
│   │   ├── plot_threshold_sensitivity_FA.py
│   │   └── *.csv / *.svg
│   ├── rf_lomao_validation/                           # Cross-metropolitan LOMAO holdout & permutation importance
│   │   ├── plot_rf_validation_comparison.py
│   │   └── *.csv / *.svg
│   └── topological_rf_importance/                     # Random Forest on IOM & Choice-IOM baselines (Figs S11, S12)
│       ├── plot_topological_rf_importance.py
│       └── *.csv / *.svg
│
└── scripts/                                           # Spatial interaction model calibration code
    ├── predict_gravity_model_matrix.py                # Exponential gravity model (NLS minimizing RMSE)
    ├── generate_cumulative_intervening_opportunity_matrix.py
    ├── predict_cumulative_intervening_opportunity_matrix.py
    ├── generate_path_intervening_opportunity_matrix.py
    └── predict_path_intervening_opportunity_matrix.py  # Choice-IOM (tau = 0.5)
```

## Software Environment

Python 3.10+ is required. Dependencies:
```bash
pip install numpy pandas scipy matplotlib seaborn geopandas scikit-learn
```
Optional: `adjustText` for automated text positioning in Figures 1A and 3C:
```bash
pip install adjustText
```

## Figure Reproduction

Figures can be generated by running the corresponding script:

```bash
# Figure 1
python figure_1/Fig1A/Fig1A.py
python figure_1/Fig1BC/Fig1BC.py
python figure_1/Fig1D/Fig1D.py
python figure_1/Fig1EF/Fig1EF.py

# Figure 2
python figure_2/Fig2B.py
python figure_2/Fig2C.py

# Figure 3
python figure_3/Fig3A/Fig3A.py
python figure_3/Fig3B/Fig3B.py
python figure_3/Fig3C/Fig3C.py
python figure_3/Fig3D/Fig3D.py
python figure_3/Fig3D_16_cities/Fig3D_16_cities.py

# Figure 4
python figure_4/Fig4A/Fig4A.py
python figure_4/Fig4B/Fig4B.py
python figure_4/Fig4CD/Fig4CD.py

# Supplementary Information Figures
python supplementary_information/descriptive_statistics/plot_figS1_cbg_counts.py
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_blockage.py
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_R.py
python supplementary_information/threshold_sensitivity/plot_threshold_sensitivity_FA.py
python supplementary_information/rf_lomao_validation/plot_rf_validation_comparison.py
python supplementary_information/topological_rf_importance/plot_topological_rf_importance.py
```

## Spatial Interaction Models

The scripts in `scripts/` provide the calibration and prediction code for the three baseline spatial interaction models:
- **Exponential Gravity Model** (`predict_gravity_model_matrix.py`): Calibrates the distance decay parameter $\beta$ via Non-linear Least Squares (NLS / L-BFGS-B) minimizing RMSE on annual origin-destination flows.
- **Cumulative Intervening Opportunities Model (IOM)** (`generate_cumulative_intervening_opportunity_matrix.py`, `predict_cumulative_intervening_opportunity_matrix.py`): Stouffer-type cumulative opportunity matrix generation and parameter estimation.
- **Choice-IOM** (`generate_path_intervening_opportunity_matrix.py`, `predict_path_intervening_opportunity_matrix.py`): Path intervening opportunity model with detour parameter $\tau = 0.5$.

Running these calibration scripts from raw data requires full trip-level OD matrices and distance matrices.

## Restricted Data Note

Raw mobility records are licensed by SafeGraph / Dewey Data Inc. Researchers can apply for academic access directly through [Dewey Data](https://www.deweydata.io/). All derived datasets needed to generate the figures and replication results are provided in this repository.

## Citation

```bibtex
@article{directional_asymmetry_2026,
  title={Directional asymmetry in urban mobility reveals semi-permeable racialized segregation},
  author={...},
  journal={Proceedings of the National Academy of Sciences},
  year={2026}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

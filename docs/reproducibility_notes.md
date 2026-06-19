# Reproducibility Notes

This repository preparation pass renamed public-facing files where possible, synchronized code path references, and created lightweight GitHub documentation. It did not execute project scripts and did not generate outputs.

## Resolved and deferred items

- `figure_1/Fig1A/compute_daily_asymmetry_metrics.py` depends on an unavailable daily OD input structure. Its path setup was changed from an external drive path to script-relative paths only; its functional workflow was not otherwise modified.
- Resolved before the round 4 audit: the previous Figure 3 and Figure 4 directory rename issue has been manually repaired. Current paths are `figure_3`, `figure_3/Fig3D/Fig3D_16_cities`, and `figure_4`.

## Scripts that should not be run casually

- `predict_path_intervening_opportunity_matrix.py`
- `predict_cumulative_intervening_opportunity_matrix.py`
- `predict_gravity_model_matrix.py`
- `generate_path_intervening_opportunity_matrix.py`
- `generate_cumulative_intervening_opportunity_matrix.py`
- `figure_1/Fig1A/compute_daily_asymmetry_metrics.py`
- `figure_4/Fig4B/compute_positive_realization_od_pairs.py`
- `figure_4/Fig4B/build_regression_dataset.py`
- `figure_4/Fig4B/run_random_forest_feature_importance.py`

## Missing or large folders

Do not create these folders during static verification or repository packaging:

- `basic_data/real_day/`
- `basic_data/choice_iom_day/`
- `basic_data/iom_day/`

## Code Repository And External Data Archive Policy

The GitHub repository should remain lightweight and should not ordinary-Git track the full large data package. Full data are expected to be hosted externally on Zenodo, OSF, institutional storage, or another approved archive. The archive DOI/URL is currently TBD.

Large CSV, binary, generated figure, and model-output files are ignored by `.gitignore` unless they are placed intentionally in `sample_data/` or `examples/`.

Before running computational workflows, restore externally archived data to the documented relative paths.

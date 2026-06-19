# Directional Asymmetry in Urban Mobility

## Overview

This repository contains data-processing scripts, model baselines, figure-generation code, manuscript files, and selected derived data for the PNAS-associated study `[ARTICLE_TITLE]` by `[AUTHOR_NAMES]`.

The study measures directional asymmetry in urban mobility across 16 major US metropolitan areas. It focuses on flows between high-poverty minority (HPM) Census Block Groups and low-poverty white (LPW) Census Block Groups, and asks whether mobility across racialized economic boundaries is reciprocal or directionally filtered. The analysis combines SafeGraph origin-destination mobility records, ACS demographic attributes, EPA built-environment attributes, gravity-model counterfactuals, cumulative intervening opportunity models, path/choice intervening opportunity models, and random forest interpretation.

## Associated manuscript

The manuscript source is located in `manuscript/Research_report.tex`.

Manuscript title in the current source: `Directional asymmetry in urban mobility reveals semi-permeable racialized segregation`.

Publication placeholders:

- Article: `[ARTICLE_TITLE]`
- Authors: `[AUTHOR_NAMES]`
- Journal reference: `[JOURNAL_REFERENCE]`
- DOI: `[DOI]`

## Repository structure

```text
basic_data/                         Core annual OD matrices, model outputs, and opportunity matrices
city_distance_matrices/              City-level CBG distance matrices
city_population_poi/                 City-level CBG population and POI attributes
figure_1/                            Figure 1 code and source data
figure_2/                            Figure 2 code and source data
figure_3/                            Figure 3 code and source data
figure_4/                            Figure 4 code and source data
manuscript/                          LaTeX manuscript source and PNAS style files
rename_map.md                        Record of public-facing path renames
workflow.md                          Repository preparation workflow and historical notes
```

Round 4 structure check: the previous Figure 3 and Figure 4 directory rename issue has been resolved. The current public-facing figure directories are `figure_3/`, `figure_3/Fig3D/Fig3D_16_cities/`, and `figure_4/`.

## Data description

The repository is organized around several data types:

- SafeGraph-derived origin-destination mobility matrices for 2019, aggregated at the Census Block Group level.
- ACS 2015-2019 demographic attributes, including population, poverty, racial composition, age, education, and housing variables.
- EPA Smart Location Database built-environment attributes, including population density, employment density, and related spatial variables.
- City-level distance matrices used for gravity-model and intervening-opportunity baselines.
- Opportunity matrices for cumulative intervening opportunity and path/choice intervening opportunity baselines.
- Figure-specific summary tables and intermediate data used to reproduce manuscript figures.

Key fields include `origin_geoid`, `Tot_Population_ACS_15_19`, `log_LPM`, `log_HPM`, `HPM_to_LPW`, and `LPW_to_HPM`.

## Code description

Top-level scripts provide the main counterfactual model-generation workflow:

- `predict_gravity_model_matrix.py` estimates production-constrained gravity-model predictions.
- `generate_cumulative_intervening_opportunity_matrix.py` builds cumulative intervening opportunity matrices.
- `predict_cumulative_intervening_opportunity_matrix.py` predicts cumulative IOM daily matrices.
- `generate_path_intervening_opportunity_matrix.py` builds path/choice intervening opportunity matrices.
- `predict_path_intervening_opportunity_matrix.py` predicts path/choice IOM daily matrices.

Figure folders contain scripts for reproducing manuscript figure panels and associated summary data. Scripts under Figure 4B construct large link-level and regression datasets and fit random forest models for feature-importance interpretation.

## Requirements

The scripts are written in Python and use common scientific Python packages, including:

- `numpy`
- `pandas`
- `scipy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `joblib`

Some figure scripts may also require geospatial plotting dependencies depending on the panel being reproduced.


## Data Availability

This GitHub repository is intended to host code, documentation, manuscript source files, workflow metadata, and lightweight examples only. It does not include the complete large data package needed for full reproduction.

The full data archive should be obtained from an external repository:

- Archive platform: Zenodo / OSF / institutional storage
- Archive DOI or URL: TBD
- Data version: TBD

After download, restore the archive contents to the expected repository-relative paths, including:

```text
basic_data/
city_distance_matrices/
city_population_poi/
figure_1/
figure_2/
figure_3/
figure_4/
```

Data derived from SafeGraph or other third-party sources may be subject to redistribution restrictions. Users are responsible for confirming access rights and license terms before using or redistributing those data.

## Repository Contents

The GitHub repository should contain:

- Python source code and lightweight configuration files.
- `README.md`, `workflow.md`, `rename_map.md`, `.gitignore`, and documentation under `docs/`.
- Manuscript source files under `manuscript/`.
- Optional tiny sample data under `sample_data/` or `examples/`, if added intentionally.

The GitHub repository should not contain the full large CSV matrix archive.

## External Data Archive

The external archive should contain the full reproducibility data package, including large CSV files, city distance matrices, annual OD/model matrices, opportunity matrices, Fig4 intermediate datasets, and generated model-ready datasets. A future data manifest should list file paths, checksums, archive version, and restore instructions.

## Large Files Policy

Files larger than 100 MB should not be committed to ordinary Git. Files larger than 500 MB should normally be placed in Zenodo, OSF, institutional storage, or another external archive. Git LFS is not the default strategy for this repository; `docs/gitattributes_lfs_draft.txt` is retained only as an optional draft.

## Reproducibility workflow

A typical static-to-computational workflow is:

1. Inspect `README.md`, `rename_map.md`, and `workflow.md` for data availability and path conventions.
2. Confirm that required SafeGraph-derived inputs and annual matrices are available locally.
3. Run only the specific model or figure script needed for the target result.
4. Avoid running large matrix-generation or prediction scripts unless sufficient disk space and compute time are available.
5. Compare generated outputs with the figure-specific CSV summaries and manuscript descriptions.

This preparation pass performed static path synchronization and did not execute project scripts. For full reproduction, first obtain the external data archive, restore it to the expected repository-relative directories, and then run only the specific scripts required for the target result.

## Expected inputs and outputs

Expected inputs include annual OD matrices, city distance matrices, population/POI tables, opportunity matrices, and figure-specific source tables.

Expected outputs may include gravity-model predictions, cumulative IOM predictions, path/choice IOM predictions, figure images, feature-importance tables, and processed regression datasets. Several outputs are very large and should be generated intentionally rather than as part of routine repository inspection.

## Large data note

The following directories are large, missing, or intentionally not generated by default:

```text
basic_data/real_day/
basic_data/choice_iom_day/
basic_data/iom_day/
```

Do not create or populate these folders during repository preparation. They may contain daily OD matrices or daily prediction outputs that are too large for ordinary Git tracking.

The following large files or directories require a human repository-hosting decision before GitHub upload. Consider Git LFS, Zenodo, OSF, institutional storage, or GitHub Releases instead of ordinary Git tracking:

```text
figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv
figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv
figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv
figure_4/Fig4B/basic_data/Link_Level_Realization_Ratio.csv
city_distance_matrices/
```

## Usage instructions

Use scripts from the repository root unless a script is explicitly designed to run from its own figure folder. Most scripts resolve paths relative to `__file__` and should not require local drive-letter paths.

Do not casually run these scripts because they can generate very large outputs:

```text
predict_path_intervening_opportunity_matrix.py
predict_cumulative_intervening_opportunity_matrix.py
predict_gravity_model_matrix.py
generate_path_intervening_opportunity_matrix.py
generate_cumulative_intervening_opportunity_matrix.py
figure_1/Fig1A/compute_daily_asymmetry_metrics.py
figure_4/Fig4B/compute_positive_realization_od_pairs.py
figure_4/Fig4B/build_regression_dataset.py
figure_4/Fig4B/run_random_forest_feature_importance.py
```

## Verification status

Static verification was performed during repository preparation. No project scripts were executed, no matrices were generated, no prediction outputs were generated, and no large daily folders were created.

Remaining manual item: create and cite the external data archive DOI/URL, then update the Data Availability section before public release.

## Citation

Please cite the associated article when using this repository:

```text
[AUTHOR_NAMES]. [ARTICLE_TITLE]. [JOURNAL_REFERENCE]. [DOI]
```

## License

License: `[LICENSE_NAME]`

## Contact

For questions, contact `[CONTACT_EMAIL]`.

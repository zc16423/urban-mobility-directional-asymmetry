# Data Hosting Plan

## Recommended Release Model

Use a split release model. Keep code, documentation, manuscript source, rename history, lightweight metadata, and optionally tiny sample data in GitHub. Place the full reproducibility data package in an external archive with persistent identifiers and clear download instructions.

This recommendation follows from the repository size (19.426 GB), multiple files over 500 MB, and total large-data volume well above 5 GB.

## GitHub Repository Contents

- Python scripts and lightweight notebooks, if any.
- `README.md`, `workflow.md`, `rename_map.md`, `.gitignore`, and `docs/`.
- Manuscript LaTeX source and style files under `manuscript/`.
- Small metadata files and tiny figure summary tables when each file is comfortably below 100 MB.
- Optional small sample data for smoke tests, if the authors choose to create it later.

## External Data Archive Contents

- Full `basic_data/` data package, especially annual OD/model matrices and opportunity matrices.
- Full `city_distance_matrices/` directory.
- Full large figure-specific data under `figure_3/` and `figure_4/`.
- Fig4B link-level and regression datasets.
- Generated model-ready datasets needed to reproduce manuscript figures.

## Git LFS Candidates

Git LFS can be considered for selected files between 100 MB and 500 MB when they must live in the GitHub repository. It is less attractive for this repository as a whole because total data volume exceeds 19 GB and Git LFS quota/bandwidth costs may become a maintenance issue.

| Relative Path |Size |Likely Category |Recommendation |
|---|---|---|---|
| `basic_data/choice_iom_year/New York.csv` | 421.3 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/iom_year/New York.csv` | 389.1 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/cumulative_intervening_opportunity_matrices/Los Angeles_opportunity_matrix.csv` | 384.2 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/iom_year/Los Angeles.csv` | 381.8 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/path_intervening_opportunity_matrices/Los Angeles_path_opportunity_matrix.csv` | 380.3 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/cumulative_intervening_opportunity_matrices/New York_opportunity_matrix.csv` | 361.3 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/path_intervening_opportunity_matrices/New York_path_opportunity_matrix.csv` | 357.5 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/choice_iom_year/Los Angeles.csv` | 318.9 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `city_distance_matrices/Chicago.csv` | 276.5 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `figure_4/Fig4B/basic_data/distance_matrices/Chicago.csv` | 276.5 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/real_year/Chicago.csv` | 234 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `figure_3/Fig3B/gravity/Chicago.csv` | 234 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `figure_4/Fig4B/basic_data/gravity/Chicago.csv` | 234 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/iom_year/Chicago.csv` | 213.5 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/choice_iom_year/Chicago.csv` | 170.4 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `basic_data/gravity_year/Los Angeles.csv` | 158.6 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `figure_1/Fig1A/real_year/Los Angeles.csv` | 158.6 MB | figure_input | Git LFS only if quota/bandwidth are approved |
| `figure_3/Fig3B/real/Los Angeles.csv` | 158.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `figure_4/Fig4B/basic_data/real/Los Angeles.csv` | 158.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/gravity_year/New York.csv` | 149.6 MB | model_output | Git LFS only if quota/bandwidth are approved |
| `figure_1/Fig1A/real_year/New York.csv` | 149.6 MB | figure_input | Git LFS only if quota/bandwidth are approved |
| `figure_3/Fig3B/real/New York.csv` | 149.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `figure_4/Fig4B/basic_data/real/New York.csv` | 149.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/cumulative_intervening_opportunity_matrices/Chicago_opportunity_matrix.csv` | 147.8 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/path_intervening_opportunity_matrices/Chicago_path_opportunity_matrix.csv` | 145.4 MB | processed_data | Git LFS only if quota/bandwidth are approved |
| `city_distance_matrices/Phoenix.csv` | 108.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `figure_4/Fig4B/basic_data/distance_matrices/Phoenix.csv` | 108.6 MB | source_data | Git LFS only if quota/bandwidth are approved |
| `basic_data/iom_year/Phoenix.csv` | 106.5 MB | model_output | Git LFS only if quota/bandwidth are approved |

## Zenodo / OSF / Institutional Storage Candidates

Files over 500 MB and large directories should go to Zenodo, OSF, institutional storage, or another durable archive rather than ordinary Git.

| Relative Path |Size |Likely Category |Recommendation |
|---|---|---|---|
| `figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv` | 848.7 MB | intermediate_data | External archive preferred |
| `figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv` | 848.7 MB | intermediate_data | External archive preferred |
| `figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv` | 762.1 MB | intermediate_data | External archive preferred |
| `city_distance_matrices/Los Angeles.csv` | 708.8 MB | source_data | External archive preferred |
| `figure_4/Fig4B/basic_data/distance_matrices/Los Angeles.csv` | 708.8 MB | source_data | External archive preferred |
| `figure_4/Fig4B/basic_data/Link_Level_Realization_Ratio.csv` | 691.5 MB | intermediate_data | External archive preferred |
| `city_distance_matrices/New York.csv` | 672.3 MB | source_data | External archive preferred |
| `figure_4/Fig4B/basic_data/distance_matrices/New York.csv` | 672.3 MB | source_data | External archive preferred |
| `basic_data/real_year/Los Angeles.csv` | 610.7 MB | source_data | External archive preferred |
| `figure_3/Fig3B/gravity/Los Angeles.csv` | 610.7 MB | model_output | External archive preferred |
| `figure_4/Fig4B/basic_data/gravity/Los Angeles.csv` | 610.7 MB | model_output | External archive preferred |
| `basic_data/real_year/New York.csv` | 566 MB | source_data | External archive preferred |
| `figure_3/Fig3B/gravity/New York.csv` | 566 MB | model_output | External archive preferred |
| `figure_4/Fig4B/basic_data/gravity/New York.csv` | 566 MB | model_output | External archive preferred |

## Files To Keep Out Of Ordinary Git

- `basic_data/` large matrix and model-output contents.
- `city_distance_matrices/`.
- `figure_3/Fig3B/gravity/`, `figure_3/Fig3B/real/`, and large `figure_3/Fig3D/` data.
- `figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv`.
- `figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv`.
- `figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv`.
- `figure_4/Fig4B/basic_data/Link_Level_Realization_Ratio.csv`.
- Large duplicate city distance and gravity/real matrices inside figure-specific folders.

## Reproducibility Implications

A code-only GitHub repository will not be fully reproducible without the external data archive. The README should document exact archive contents, expected relative paths after download, checksums if available, and which scripts require large data.

If data are archived externally, users should download and unpack the archive so that paths match the repository layout, or follow explicit README instructions for setting data paths.

## Required Manual Decisions

- Decide whether GitHub will host code only, code plus samples, or code plus selected LFS data.
- Decide whether the full data archive will be Zenodo, OSF, institutional storage, or another repository.
- Decide whether generated/intermediate Fig4B datasets should be archived as reproducibility artifacts or regenerated from upstream data.
- Decide whether duplicate large matrices in figure folders should be retained, replaced by symlink-like instructions, or omitted from the public GitHub repository.
- Decide license and access terms for SafeGraph-derived data, which may have redistribution restrictions.

## Recommended Citation Text For Data Archive

Suggested placeholder:

```text
[AUTHOR_NAMES]. Data and code for [ARTICLE_TITLE]. [DATA_REPOSITORY_NAME]. [VERSION]. [YEAR]. [DATA_DOI].
```

In the article/code README, cite both the manuscript and the data archive DOI once available.

## Checklist Before Upload

- Choose external archive platform and data license/access policy.
- Decide whether any files will use Git LFS.
- Update `README.md` with data download and unpacking instructions.
- Update `.gitignore` to exclude ordinary-Git copies of externally archived data.
- Optionally add `.gitattributes` only after approving Git LFS.
- Run a pre-commit size check for files over 100 MB.
- Clone into a fresh directory and verify documentation paths.

## Applied Round 6 Policy

The chosen model is a GitHub code repository plus an external full data archive. Git LFS is not enabled by default. The root `.gitignore` excludes large tabular, binary, generated figure, and model-output data while preserving code, documentation, manuscript source, and optional `sample_data/` or `examples/` allowlisted content.

Archive DOI/URL remains TBD and must be added before public release.

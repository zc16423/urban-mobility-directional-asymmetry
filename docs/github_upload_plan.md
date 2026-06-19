# GitHub Upload Plan

## Current Status

The repository structure is English-only and statically verified. The remaining blocker is data hosting: the working tree contains large data assets that are not suitable for ordinary GitHub commits.

## Recommended Repository Type

Recommended: code-first public repository with external archived data. Include small metadata and documentation in ordinary Git. Avoid committing full large CSV matrices directly to ordinary Git.

## Files Suitable For Ordinary Git

- `*.py` source code.
- `README.md`, `workflow.md`, `rename_map.md`, `.gitignore`.
- `docs/*.md` planning and reproducibility documentation.
- `manuscript/*.tex`, `.bib`, `.bst`, `.sty` and small manuscript assets.
- Small CSV metadata files below 100 MB if redistribution rights permit.

## Files Requiring Git LFS Or External Hosting

All files over 100 MB require Git LFS or external hosting. Files over 500 MB are recommended for external archive by default. Current high-risk areas include:

| Relative Path |Size |Likely Category |Recommended Handling |
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
| `basic_data/choice_iom_year/New York.csv` | 421.3 MB | model_output | Git LFS or external archive |
| `basic_data/iom_year/New York.csv` | 389.1 MB | model_output | Git LFS or external archive |
| `basic_data/cumulative_intervening_opportunity_matrices/Los Angeles_opportunity_matrix.csv` | 384.2 MB | processed_data | Git LFS or external archive |
| `basic_data/iom_year/Los Angeles.csv` | 381.8 MB | model_output | Git LFS or external archive |
| `basic_data/path_intervening_opportunity_matrices/Los Angeles_path_opportunity_matrix.csv` | 380.3 MB | processed_data | Git LFS or external archive |
| `basic_data/cumulative_intervening_opportunity_matrices/New York_opportunity_matrix.csv` | 361.3 MB | processed_data | Git LFS or external archive |
| `basic_data/path_intervening_opportunity_matrices/New York_path_opportunity_matrix.csv` | 357.5 MB | processed_data | Git LFS or external archive |
| `basic_data/choice_iom_year/Los Angeles.csv` | 318.9 MB | model_output | Git LFS or external archive |
| `city_distance_matrices/Chicago.csv` | 276.5 MB | source_data | Git LFS or external archive |
| `figure_4/Fig4B/basic_data/distance_matrices/Chicago.csv` | 276.5 MB | source_data | Git LFS or external archive |
| `basic_data/real_year/Chicago.csv` | 234 MB | source_data | Git LFS or external archive |
| `figure_3/Fig3B/gravity/Chicago.csv` | 234 MB | model_output | Git LFS or external archive |
| `figure_4/Fig4B/basic_data/gravity/Chicago.csv` | 234 MB | model_output | Git LFS or external archive |
| `basic_data/iom_year/Chicago.csv` | 213.5 MB | model_output | Git LFS or external archive |
| `basic_data/choice_iom_year/Chicago.csv` | 170.4 MB | model_output | Git LFS or external archive |
| `basic_data/gravity_year/Los Angeles.csv` | 158.6 MB | model_output | Git LFS or external archive |
| `figure_1/Fig1A/real_year/Los Angeles.csv` | 158.6 MB | figure_input | Git LFS or external archive |
| `figure_3/Fig3B/real/Los Angeles.csv` | 158.6 MB | source_data | Git LFS or external archive |
| `figure_4/Fig4B/basic_data/real/Los Angeles.csv` | 158.6 MB | source_data | Git LFS or external archive |
| `basic_data/gravity_year/New York.csv` | 149.6 MB | model_output | Git LFS or external archive |
| `figure_1/Fig1A/real_year/New York.csv` | 149.6 MB | figure_input | Git LFS or external archive |
| `figure_3/Fig3B/real/New York.csv` | 149.6 MB | source_data | Git LFS or external archive |
| `figure_4/Fig4B/basic_data/real/New York.csv` | 149.6 MB | source_data | Git LFS or external archive |
| `basic_data/cumulative_intervening_opportunity_matrices/Chicago_opportunity_matrix.csv` | 147.8 MB | processed_data | Git LFS or external archive |
| `basic_data/path_intervening_opportunity_matrices/Chicago_path_opportunity_matrix.csv` | 145.4 MB | processed_data | Git LFS or external archive |
| `city_distance_matrices/Phoenix.csv` | 108.6 MB | source_data | Git LFS or external archive |
| `figure_4/Fig4B/basic_data/distance_matrices/Phoenix.csv` | 108.6 MB | source_data | Git LFS or external archive |
| `basic_data/iom_year/Phoenix.csv` | 106.5 MB | model_output | Git LFS or external archive |

## Proposed .gitignore Updates

Current `.gitignore` already excludes missing daily folders and temporary files. Before upload, consider adding ordinary-Git exclusions for externally archived data, for example:

```gitignore
# Full data archive hosted externally; keep ordinary Git lightweight.
basic_data/**/*.csv
city_distance_matrices/**/*.csv
figure_3/**/*.csv
figure_4/**/*.csv

# Keep small examples only if authors intentionally add them.
!sample_data/**
```

Do not apply these rules until the authors decide which small CSVs, if any, should remain in Git.

## Proposed .gitattributes Draft

A Git LFS draft is provided at `docs/gitattributes_lfs_draft.txt`. Do not copy it to root `.gitattributes` until Git LFS is approved.

## Upload Sequence

1. Decide the data hosting model.
2. Upload or stage the external data archive and obtain DOI/access URL if applicable.
3. Update `README.md` with data download, unpacking, and citation instructions.
4. Update `.gitignore` or root `.gitattributes` according to the chosen model.
5. Run `git status`.
6. Check whether any file over 100 MB would be committed to ordinary Git.
7. Commit only after the large-file policy is enforced.
8. Push to GitHub.
9. Clone into a fresh directory and verify README instructions and script paths.

## Verification Before Commit

- Confirm no Chinese public-facing filenames remain.
- Confirm no `__pycache__` directories.
- Confirm missing daily folders were not generated.
- Confirm no ordinary-Git tracked file exceeds 100 MB unless Git LFS is intentionally configured.
- Confirm README data-access instructions match the chosen archive.

## Verification After Clone

- Fresh clone succeeds without downloading enormous files unexpectedly.
- README renders correctly on GitHub.
- Paths in README match repository layout.
- If using external data, downloaded archive can be placed into expected paths.
- AST-only syntax check still passes without importing project modules.

## Do Not Upload Until

- Full data-hosting strategy is approved.
- Redistribution rights for SafeGraph-derived data are confirmed.
- `.gitignore` or Git LFS policy prevents accidental ordinary-Git commits of large files.
- README includes final data archive DOI/URL or clear placeholder instructions.

## Applied Ignore Policy

The root `.gitignore` now implements the code-repository plus external-data-archive strategy. It excludes large CSV and binary data under core data and figure folders, excludes generated figure outputs, and keeps source code, markdown documentation, LaTeX manuscript source, and optional small sample/example files visible.

Do not initialize, commit, or push until the external archive decision is complete and README data links are updated from TBD.

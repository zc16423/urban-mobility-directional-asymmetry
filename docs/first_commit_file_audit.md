# First Commit File Audit

## Summary

- Git repository initialized: yes.
- Existing commits: none; `git log` reports that the current branch has no commits yet.
- Remote configured: no.
- Staged files: none.
- Dry-run proposed file count: 57.
- Files over 100 MB proposed for Git: 0.
- Files over 500 MB proposed for Git: 0.
- Large-data extensions proposed for Git: 0.
- Result: no large data files are proposed by dry-run.

## Repository State

| Check | Result |
| --- | --- |
| Git repository initialized | yes |
| Existing commits | no; empty repository |
| Remote configured | no |
| Staged files | none |
| Root .gitattributes | absent |
| .gitignore | present |

## Files Proposed For First Commit

| Relative path | Size | Extension |
| --- | --- | --- |
| .gitignore | 0.002 MB | (none) |
| docs/data_hosting_plan.md | 0.009 MB | .md |
| docs/data_manifest_template.md | 0.001 MB | .md |
| docs/first_commit_file_audit.md | 0.005 MB | .md |
| docs/gitattributes_lfs_draft.txt | 0.001 MB | .txt |
| docs/github_upload_plan.md | 0.008 MB | .md |
| docs/large_file_inventory.md | 0.065 MB | .md |
| docs/pre_commit_large_file_check.md | 0.005 MB | .md |
| docs/reproducibility_notes.md | 0.002 MB | .md |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.cpg | 0.000 MB | .cpg |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.dbf | 0.008 MB | .dbf |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.prj | 0.000 MB | .prj |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.shp | 0.214 MB | .shp |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.shp.ea.iso.xml | 0.017 MB | .xml |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.shp.iso.xml | 0.031 MB | .xml |
| figure_1/Fig1A/cb_2018_us_state_20m/cb_2018_us_state_20m.shx | 0.000 MB | .shx |
| figure_1/Fig1A/compute_city_mobility_asymmetry_metrics.py | 0.003 MB | .py |
| figure_1/Fig1A/compute_daily_asymmetry_metrics.py | 0.006 MB | .py |
| figure_1/Fig1A/Fig1A.py | 0.007 MB | .py |
| figure_1/Fig1BC/Fig1BC.py | 0.005 MB | .py |
| figure_1/Fig1D/appendix/plot_appendix_ring.py | 0.006 MB | .py |
| figure_1/Fig1D/Fig1D.py | 0.005 MB | .py |
| figure_1/Fig1EF/Fig1EF.py | 0.009 MB | .py |
| figure_2/Fig2B.py | 0.006 MB | .py |
| figure_2/Fig2C.py | 0.006 MB | .py |
| figure_3/Fig3A/Fig3A.py | 0.005 MB | .py |
| figure_3/Fig3B/Fig3B.py | 0.010 MB | .py |
| figure_3/Fig3C/Fig3C.py | 0.005 MB | .py |
| figure_3/Fig3D/Fig3D_16_cities/Fig3D_16_cities.py | 0.005 MB | .py |
| figure_3/Fig3D/Fig3D.py | 0.005 MB | .py |
| figure_4/Fig4A/Fig4A.py | 0.006 MB | .py |
| figure_4/Fig4B/build_regression_dataset.py | 0.005 MB | .py |
| figure_4/Fig4B/compute_positive_realization_od_pairs.py | 0.005 MB | .py |
| figure_4/Fig4B/Fig4B.py | 0.003 MB | .py |
| figure_4/Fig4B/run_random_forest_feature_importance.py | 0.005 MB | .py |
| figure_4/Fig4CD/Fig4CD.py | 0.010 MB | .py |
| generate_cumulative_intervening_opportunity_matrix.py | 0.004 MB | .py |
| generate_path_intervening_opportunity_matrix.py | 0.005 MB | .py |
| manuscript/Fig/Fig1.png | 1.451 MB | .png |
| manuscript/Fig/Fig2.png | 0.395 MB | .png |
| manuscript/Fig/Fig3.png | 0.342 MB | .png |
| manuscript/Fig/Fig4.png | 0.214 MB | .png |
| manuscript/jabbrv-ltwa-all.ldf | 0.047 MB | .ldf |
| manuscript/jabbrv-ltwa-en.ldf | 0.256 MB | .ldf |
| manuscript/jabbrv.sty | 0.015 MB | .sty |
| manuscript/PNAS_Logo.pdf | 0.055 MB | .pdf |
| manuscript/pnas-new.bst | 0.019 MB | .bst |
| manuscript/pnas-new.cls | 0.023 MB | .cls |
| manuscript/pnas-sample.bib | 0.019 MB | .bib |
| manuscript/pnasresearcharticle.sty | 0.002 MB | .sty |
| manuscript/Research_report.tex | 0.036 MB | .tex |
| predict_cumulative_intervening_opportunity_matrix.py | 0.007 MB | .py |
| predict_gravity_model_matrix.py | 0.006 MB | .py |
| predict_path_intervening_opportunity_matrix.py | 0.007 MB | .py |
| README.md | 0.009 MB | .md |
| rename_map.md | 0.005 MB | .md |
| workflow.md | 0.013 MB | .md |

## Ignored Large Data Paths

| Relative path | Status | Matching ignore rule |
| --- | --- | --- |
| basic_data/real_year/Los Angeles.csv | ignored | .gitignore:32:basic_data/**/*.csv	basic_data/real_year/Los Angeles.csv |
| city_distance_matrices/Los Angeles.csv | ignored | .gitignore:35:city_distance_matrices/*.csv	city_distance_matrices/Los Angeles.csv |
| city_population_poi/Los Angeles.csv | ignored | .gitignore:37:city_population_poi/*.csv	city_population_poi/Los Angeles.csv |
| figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv | ignored | .gitignore:44:figure_4/**/*.csv	figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv |
| figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv | ignored | .gitignore:44:figure_4/**/*.csv	figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv |
| figure_1/Fig1A/real_year/Los Angeles.csv | ignored | .gitignore:38:figure_1/**/*.csv	figure_1/Fig1A/real_year/Los Angeles.csv |
| figure_3/Fig3B/gravity/Los Angeles.csv | ignored | .gitignore:42:figure_3/**/*.csv	figure_3/Fig3B/gravity/Los Angeles.csv |
| figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv | ignored | .gitignore:44:figure_4/**/*.csv	figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv |

## Potentially Risky Files

No large-data extensions or files over 100 MB are proposed for the first commit.

Small manuscript figure assets and the small public US states shapefile are proposed for inclusion. They are below 2 MB each and are not large-data blockers, but they should still receive manual review before the real commit.

## Files Over 100 MB That Would Be Added

No files over 100 MB are proposed for the first commit.

## Files Over 500 MB That Would Be Added

No files over 500 MB are proposed for the first commit.

## Required Fixes Before Real Commit

- No large-file blocker was detected by dry-run.
- External archive DOI/URL and data version are still `TBD`; this is not a Git technical blocker, but it is a public-release metadata item.
- Because Git reports this Windows path as a dubious-ownership repository unless a safe-directory override is supplied, use `git -c safe.directory=I:/0git上传 ...` for checks or add the path to Git safe.directory only after manual trust review.
- Review the proposed small manuscript images, PDF logo, LaTeX support files, and public shapefile assets before the real first commit.

## Recommended First Commit Message

```text
Initial public release structure and documentation
```

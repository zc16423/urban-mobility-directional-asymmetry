# Project Objective

Prepare the repository at `I:\0git上传` for GitHub release as the data and code companion repository for a PNAS research article.

The repository must use English folder names, English file names, English code input/output paths, and include a publication-ready `README.md` that matches the article, data, and code structure.


## Round 4 Status

Round 4 audit confirmed that the previous Figure 3 and Figure 4 directory rename issue has been manually repaired. Current paths are `figure_3`, `figure_3/Fig3D/Fig3D_16_cities`, and `figure_4`. Historical old-path references in this workflow are retained only as rename history, not as current paths.

## Background

This repository contains data, scripts, figure-generation code, matrix-generation code, and prediction code for a PNAS research article.

The full manuscript is located at:

```text
manuscript\Research_report.tex
```

The repository has already completed schema synchronization and static verification. The current task is repository packaging, naming standardization, README generation, and GitHub readiness.

Important prior synchronization notes:

- `GIDBG` has been replaced by `origin_geoid`.
- Old `population` input column has been replaced by `Tot_Population_ACS_15_19`.
- Outdated numeric city-code assumptions were removed where applicable.
- External paths were updated from `F:\...` to local project-relative paths under `I:\0git上传`.
- Opportunity matrix filename patterns are:
  - `{city}_path_opportunity_matrix.csv`
  - `{city}_opportunity_matrix.csv`
- Fig2 semantics:
  - `Fig2B.py` uses `log_LPM` for `HPM_to_LPW`.
  - `Fig2C.py` uses `log_HPM` for `LPW_to_HPM`.
- Prediction output semantics:
  - path intervention opportunity prediction outputs to `basic_data\choice_iom_day`
  - cumulative intervention opportunity prediction outputs to `basic_data\iom_day`
  - `choice_iom_year` is the element-wise annual sum of `choice_iom_day`
  - `iom_year` is the element-wise annual sum of `iom_day`

## Goals

- Rename all Chinese folder names, CSV files, and Python files into clear English names.
- Update all Python scripts so input paths, output paths, and generated filenames use the new English names.
- Preserve scientific meaning and existing data relationships.
- Create a GitHub-ready repository layout suitable for a PNAS data/code release.
- Write a complete `README.md` adapted to the manuscript, code, and data.
- Avoid generating large outputs or running heavy scripts.
- Verify the repository statically before handoff.

## Inputs

Use the following local repository root:

```text
I:\0git上传
```

Primary manuscript:

```text
manuscript\Research_report.tex
```

Current items requiring English renaming:

```text
city_distance_matrices
city_population_poi
figure_1
figure_2
Fig3绘图
Fig4绘图
manuscript
basic_data
predict_cumulative_intervening_opportunity_matrix.py
generate_cumulative_intervening_opportunity_matrix.py
generate_path_intervening_opportunity_matrix.py
predict_path_intervening_opportunity_matrix.py
predict_gravity_model_matrix.py
```

Deferred file that must not be synchronized beyond necessary path-name updates unless required for repository consistency:

```text
figure_1\Fig1A\Fig1A计算每天的不对称基尼以及变异系数.py
```

Reason:

- It depends on unavailable daily OD matrix input structure.
- Round 2 replaced the external `F:\...` paths in this deferred script with script-relative paths; its unavailable daily OD input structure remains unresolved.
- It should not be functionally modified until the correct daily input folder structure and sample headers are available.

Missing or large local folders that must not be generated:

```text
basic_data\real_day
basic_data\choice_iom_day
basic_data\iom_day
```

## Required Tasks

### Phase 1 — Repository Inventory

- Scan the full repository under `I:\0git上传`.
- Produce an inventory of:
  - folders with Chinese names,
  - `.py` files with Chinese names,
  - `.csv` files with Chinese names,
  - code references to old Chinese paths,
  - code references to old Chinese filenames,
  - code references to unavailable external paths such as `F:\`.
- Do not execute project scripts.
- Do not import project Python modules.
- Do not generate matrices, figures, or prediction outputs.

### Phase 2 — Define English Naming Map

Create a deterministic rename map before modifying files.

Use clear, publication-ready English names. Suggested mappings:

```text
16城市距离矩阵 -> city_distance_matrices
16城市人数及poi数量信息 -> city_population_poi
Fig1绘图 -> figure_1
Fig2绘图 -> figure_2
Fig3绘图 -> figure_3
Fig4绘图 -> figure_4
PNAS_directional_asymmetry -> manuscript
基本数据 -> basic_data

累积介入机会预测矩阵.py -> predict_cumulative_intervening_opportunity_matrix.py
累计介入机会矩阵生成.py -> generate_cumulative_intervening_opportunity_matrix.py
路径介入机会矩阵生成.py -> generate_path_intervening_opportunity_matrix.py
路径介入机会预测矩阵.py -> predict_path_intervening_opportunity_matrix.py
重力模型预测矩阵.py -> predict_gravity_model_matrix.py
```

For nested figure scripts and CSV files:

- Translate Chinese names into concise English names.
- Preserve figure panel identifiers such as `Fig1A`, `Fig2B`, etc.
- Prefer lowercase snake_case for script and data filenames unless existing figure-panel naming is clearer.
- Avoid spaces in filenames.
- Avoid special characters except `_` and `-`.
- Preserve file extensions.

Before applying renames, write the rename map to:

```text
rename_map.md
```

The map must include:

- old relative path,
- new relative path,
- reason for rename,
- whether code references were updated.

### Phase 3 — Rename Files and Folders

- Apply the approved English rename map.
- Rename folders first from deepest paths upward where needed to avoid path conflicts.
- Rename files after folder renaming.
- Preserve file contents unless content changes are required for path consistency.
- Do not rename large missing folders that are not present locally.
- Do not create placeholder folders for unavailable large data unless needed for documentation only.

### Phase 4 — Update Code References

Update all relevant `.py`, `.md`, `.tex`, and configuration files so they reference the new English names.

Required updates:

- Input paths.
- Output paths.
- CSV filenames.
- Python script references.
- Figure output references.
- Matrix output references.
- Data folder references.
- Any hard-coded repository paths.

Rules:

- Prefer relative paths based on script location or repository root.
- Avoid absolute paths such as `I:\0git上传` inside reusable scripts unless already necessary.
- Do not introduce new external drive paths.
- Do not change scientific calculations.
- Do not change schemas except for path/name consistency.
- Do not execute scripts that generate large outputs.

### Phase 5 — README.md Generation

Create a GitHub-ready `README.md` at:

```text
README.md
```

The README must be written in professional academic English.

The README must include:

```markdown
# Repository title

## Overview

## Associated manuscript

## Repository structure

## Data description

## Code description

## Requirements

## Reproducibility workflow

## Expected inputs and outputs

## Large data note

## Usage instructions

## Verification status

## Citation

## License

## Contact
```

README requirements:

- Adapt content to the manuscript `manuscript\Research_report.tex`.
- Describe the repository as supporting data and code for a PNAS research article.
- Explain the purpose of major folders:
  - `basic_data`
  - `city_distance_matrices`
  - `city_population_poi`
  - `figure_1`
  - `figure_2`
  - `figure_3`
  - `figure_4`
  - `manuscript`
- Explain matrix-generation scripts.
- Explain prediction scripts.
- Explain figure-generation scripts.
- Clearly state that large daily OD and prediction folders are not included if absent:
  - `basic_data\real_day`
  - `basic_data\choice_iom_day`
  - `basic_data\iom_day`
- Include reproducibility warnings for scripts that can generate large outputs.
- Include a verification status section stating that static validation was performed and no heavy outputs were generated.
- Use placeholders where human input is required:
  - `[ARTICLE_TITLE]`
  - `[AUTHOR_NAMES]`
  - `[JOURNAL_REFERENCE]`
  - `[DOI]`
  - `[CONTACT_EMAIL]`
  - `[LICENSE_NAME]`

### Phase 6 — Optional Documentation Files

If useful, create the following lightweight documentation files:

```text
docs\data_dictionary.md
docs\reproducibility_notes.md
docs\file_inventory.md
```

These files should not duplicate the README unnecessarily.

`data_dictionary.md` should describe known key fields, including:

```text
origin_geoid
Tot_Population_ACS_15_19
log_LPM
log_HPM
HPM_to_LPW
LPW_to_HPM
```

`reproducibility_notes.md` should document:

- scripts that are safe for static inspection,
- scripts that may generate large outputs,
- unavailable large folders,
- deferred synchronization for Fig1A daily OD calculation.

`file_inventory.md` should summarize final repository structure after renaming.

### Phase 7 — Static Verification

Run static verification only.

Required checks:

- Confirm no Chinese folder names remain.
- Confirm no Chinese `.py` filenames remain.
- Confirm no Chinese `.csv` filenames remain unless scientifically necessary and documented.
- Confirm no code references old Chinese paths.
- Confirm no code references old Chinese script names.
- Confirm no stale `F:\` paths remain except in explicitly deferred documentation or comments.
- Confirm all `.py` files pass AST syntax checks.
- Confirm `README.md` exists and references the final English repository layout.
- Confirm `rename_map.md` exists.
- Confirm no heavy outputs were generated.
- Confirm no `__pycache__` folders were created.

Allowed commands:

```powershell
Get-ChildItem -Recurse
Select-String
python -m py_compile
```

Do not run:

```text
predict_path_intervening_opportunity_matrix.py
predict_cumulative_intervening_opportunity_matrix.py
predict_gravity_model_matrix.py
generate_path_intervening_opportunity_matrix.py
generate_cumulative_intervening_opportunity_matrix.py
Fig1A daily OD calculation script
```

### Phase 8 — GitHub Readiness Check

Prepare the repository for GitHub upload.

Check for:

- English-only public-facing names.
- Clear README.
- No unnecessary temporary files.
- No `__pycache__`.
- No hidden large generated outputs.
- No local-only absolute paths in reusable scripts.
- No sensitive information.
- No manuscript build artifacts unless intentionally retained.
- No large daily OD folders unless intentionally tracked.

If no `.gitignore` exists, create or update:

```text
.gitignore
```

Recommended exclusions:

```gitignore
__pycache__/
*.pyc
.DS_Store
Thumbs.db
.ipynb_checkpoints/
*.log

basic_data/real_day/
basic_data/choice_iom_day/
basic_data/iom_day/

*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
```

Do not exclude source `.py`, `.csv`, `.tex`, `.md`, or required figure source files unless they are large generated outputs.

## Deliverables

Create or update the following:

```text
README.md
rename_map.md
.gitignore
```

Optional, if helpful:

```text
docs\data_dictionary.md
docs\reproducibility_notes.md
docs\file_inventory.md
```

Also deliver:

- Fully renamed English folder structure.
- Fully renamed English Python filenames.
- Fully renamed English CSV filenames where applicable.
- Updated code references matching the new names.
- Static verification summary.

## Verification Checklist

Before completion, verify:

- [ ] All target folders have English names.
- [ ] All target Python files have English names.
- [ ] All target CSV files have English names.
- [ ] All code references use English paths and filenames.
- [ ] `README.md` exists at repository root.
- [ ] `README.md` describes the manuscript, data, code, workflow, and limitations.
- [ ] `rename_map.md` records all old-to-new path changes.
- [ ] `.gitignore` excludes heavy generated folders and temporary files.
- [ ] No large missing folders were generated.
- [ ] No prediction scripts were executed.
- [ ] No matrix-generation scripts were executed.
- [ ] No figure-generation scripts requiring unavailable daily OD data were executed.
- [ ] All Python files pass AST-only syntax checks.
- [ ] No `__pycache__` folders remain.
- [ ] No unwanted `F:\` paths remain outside explicitly deferred documentation.
- [ ] Repository is ready for manual GitHub upload.

## Constraints

- Do not change scientific calculations.
- Do not modify data values.
- Do not regenerate large outputs.
- Do not execute heavy project scripts.
- Do not import project modules during validation.
- Do not modify `.tex` manuscript content except repository path references if necessary.
- Do not delete research data unless it is clearly temporary or generated and already documented.
- Preserve existing directory relationships where possible.
- Use English academic naming suitable for a public PNAS companion repository.
- Maintain reproducibility and traceability through `rename_map.md`.

## Output Format

At the end of the task, report only:

```markdown
# GitHub Preparation Summary

## Completed Changes

## Rename Map Location

## README Location

## Verification Results

## Deferred Items

## GitHub Upload Notes
```

The final report must be concise and must not include long file contents.

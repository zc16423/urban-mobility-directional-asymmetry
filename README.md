# Directional asymmetry in urban mobility reveals semi-permeable racialized segregation

## Overview

This repository contains the code, documentation, figure-generation scripts, and selected derived data associated with the study:

**Directional asymmetry in urban mobility reveals semi-permeable racialized segregation**

Using mobility data from 16 major US metropolitan areas, this study quantifies directional asymmetry in travel between high-poverty minority (HPM) and low-poverty white (LPW) Census Block Groups (CBGs). The analysis evaluates multiple mobility baselines, including gravity models, cumulative intervening-opportunity models, and path/choice intervening-opportunity models, and examines the social and built-environment factors associated with asymmetric mobility patterns.

---

## Repository Structure

```text
basic_data/                   Core model outputs and derived matrices
city_distance_matrices/       City-level CBG distance matrices
city_population_poi/          Population and POI attributes

figure_1/                     Asymmetry metrics and descriptive analyses
figure_2/                     Gravity-model comparison
figure_3/                     Intervening-opportunity model analyses
figure_4/                     Mechanism analyses and random forest models

```

---

## Main Analysis Scripts

### Counterfactual Mobility Models

```text
predict_gravity_model_matrix.py

generate_cumulative_intervening_opportunity_matrix.py
predict_cumulative_intervening_opportunity_matrix.py

generate_path_intervening_opportunity_matrix.py
predict_path_intervening_opportunity_matrix.py
```

### Figure Generation

Each figure directory contains scripts and processed data required to reproduce the corresponding manuscript figures.

---

## Data Sources

The study integrates data from multiple sources:

* SafeGraph origin-destination mobility records
* American Community Survey (ACS) 2015–2019 demographic attributes
* EPA Smart Location Database built-environment indicators

Derived datasets include:

* CBG-level origin-destination matrices
* Distance matrices
* Opportunity matrices
* Figure-specific summary tables
* Model prediction outputs

---

## Software Requirements

The analyses were conducted in Python using:

```text
numpy
pandas
scipy
matplotlib
seaborn
scikit-learn
joblib
```

Additional geospatial libraries may be required for selected figure scripts.

---

## Reproducibility Workflow

1. Obtain the required data archive (see Data Availability).
2. Restore the archived files to the repository directory structure.
3. Run the desired model-generation or figure-generation scripts.
4. Compare generated outputs with the published manuscript figures and summary tables.

Because several intermediate datasets are large, users are encouraged to reproduce only the analyses relevant to their needs.

---

## Data Availability

Due to file-size limitations and third-party licensing restrictions, the complete reproducibility dataset is not hosted directly in this GitHub repository.

The full data archive is available at:

DOI: [TO BE INSERTED]

The archive contains:

* Origin-destination matrices
* Distance matrices
* Opportunity matrices
* Figure-specific intermediate datasets
* Model-ready analysis datasets

SafeGraph-derived data remain subject to the original provider's licensing and redistribution policies.

---

## Citation

If you use this repository, please cite:

Zhang c., et al.

*Directional asymmetry in urban mobility reveals semi-permeable racialized segregation.*

---

## License

Code in this repository is released under the MIT License.

Users are responsible for complying with the licensing terms associated with all third-party datasets used in this study.

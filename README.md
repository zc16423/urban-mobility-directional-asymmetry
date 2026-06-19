# Directional asymmetry in urban mobility reveals semi-permeable racialized segregation

## Overview

This repository contains the code, documentation, figure-generation scripts, and selected derived data associated with this study.

Using mobility data from 16 major US metropolitan areas, the study quantifies directional asymmetry in travel between high-poverty minority (HPM) and low-poverty white (LPW) Census Block Groups (CBGs). The analysis evaluates multiple mobility baselines, including gravity models, cumulative intervening-opportunity models, and path/choice intervening-opportunity models, and examines the social and built-environment factors associated with asymmetric mobility patterns.

---

## Repository Structure

```text
README.md

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
* American Community Survey (ACS) 2015–2019 5-year estimates
* EPA Smart Location Database (SLD)

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

1. Prepare the required input datasets.
2. Run the desired model-generation or figure-generation scripts.
3. Compare generated outputs with the manuscript figures and summary tables.

Because several intermediate datasets are large, users are encouraged to reproduce only the analyses relevant to their needs.

---

## Data Availability

This repository contains code, documentation, and selected derived datasets used in the analysis.

Some source datasets are subject to third-party licensing restrictions and therefore cannot be redistributed through this repository. Users seeking access to the original mobility data should consult the corresponding data providers.

---

## Citation

Citation information will be updated upon publication.

---

## License

See the LICENSE file for licensing information.

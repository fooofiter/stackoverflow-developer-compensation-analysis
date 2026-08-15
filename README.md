# What Predicts Developer Compensation?

This Udacity Data Scientist Nanodegree project analyzes the 2025 Stack Overflow
Developer Survey to understand compensation differences and test how well
public survey attributes can predict annual pay.

## Business questions

1. How does annual compensation vary across experience levels, countries, and
   developer roles?
2. Which technologies are conditionally associated with higher or lower
   compensation after accounting for career and workplace context?
3. How accurately can compensation be predicted, and which features contribute
   most to predictive performance?
4. What does the selected model predict for three hypothetical career profiles?

## Main findings

- Median compensation rises from approximately USD 30,764 for developers with
  0–2 years of professional experience to USD 117,082 for those with 31 or
  more years.
- Among the 15 highest-support countries, median compensation ranges from USD
  19,761 in India to USD 151,000 in the United States. These unadjusted global
  comparisons do not account for purchasing power or cost of living.
- Country and experience variables contribute more predictive information than
  any single technology.
- Histogram Gradient Boosting outperforms Ridge and Extra Trees. Its held-out
  log MAE is 0.422, equivalent to a typical multiplicative error of about
  1.53×, with log R² of 0.564.
- The model is suitable for population-level pattern discovery, not individual
  salary decisions or causal claims.

## Data

The project uses the official [2025 Stack Overflow Developer Survey data](https://github.com/StackExchange/Survey/tree/main/packages/archive/2025).
The raw response file contains 49,191 rows and 172 columns. The primary analysis
retains 19,025 professional, working developers who report annual compensation
from USD 1,000 through USD 1,000,000.

The 134 MB response file exceeds GitHub's normal file limit and is therefore
not committed to this repository. Download and verify the official files with:

```bash
python scripts/download_data.py
```

This creates:

```text
data/raw/results.csv
data/raw/schema.csv
```

## Repository structure

```text
.
├── blog/
│   └── developer_compensation_blog_post.md
├── data/
│   └── README.md
├── notebooks/
│   └── stackoverflow_developer_compensation.ipynb
├── reports/
│   ├── figures/
│   └── *.csv
├── scripts/
│   ├── build_final_notebook.py
│   └── download_data.py
├── LICENSE
├── README.md
└── requirements.txt
```

The main deliverable is
[`notebooks/stackoverflow_developer_compensation.ipynb`](notebooks/stackoverflow_developer_compensation.ipynb).
Intermediate development notebooks and decision-gate records are retained
locally but excluded from the public repository.

## Installation and execution

Python 3.10 is recommended.

```bash
python -m venv .venv
```

Activate the environment, then install the tested dependencies:

```bash
pip install -r requirements.txt
python scripts/download_data.py
jupyter lab
```

Open the main notebook and run all cells. A complete run performs the bounded
five-fold hyperparameter searches and takes approximately 14 minutes on the
development machine.

To rebuild and execute the notebook programmatically:

```bash
python scripts/build_final_notebook.py
```

## Method summary

- Target: `log1p(ConvertedCompYearly)`
- Split: country-stratified 80/20 train/test split, `random_state=42`
- Missing values: training-only median or explicit-category imputation
- Rare categories: grouped inside training folds
- Technology fields: training-only multi-select vocabulary
- Models: median baseline, Ridge, Extra Trees, Histogram Gradient Boosting
- Selection metric: five-fold cross-validated log MAE
- Interpretation: held-out permutation importance and Ridge coefficients
- Sensitivity check: USD 2,500–500,000 compensation range

## Libraries

- NumPy and pandas for data preparation
- Matplotlib and seaborn for visualization
- scikit-learn for preprocessing, modeling, evaluation, and interpretation
- JupyterLab, nbformat, and nbclient for the executable notebook workflow

## Licensing and acknowledgements

Project code is available under the [MIT License](LICENSE).

The survey data is owned and distributed by Stack Overflow and Stack Exchange.
According to the official survey repository, the database is licensed under
the Open Database License (ODbL) and its individual contents under the Database
Contents License (DbCL). The raw data is not redistributed here.

Thanks to Stack Overflow survey respondents and the Stack Exchange team for
making the anonymized dataset publicly available.

<div align="center">
  <picture>
    <img src="https://raw.githubusercontent.com/cachevector/tablint/refs/heads/main/docs/assets/tablint-wobg.svg" width="80">
  </picture>

  <h1>Tablint</h1>
  <p>
    <b> Dataset Profiler & Debugger for Machine Learning </b>
  </p>

  <p align="center">
    <!-- Distribution -->
    <img src="https://img.shields.io/pypi/v/tablint?color=blue&label=PyPI" />
    <!-- License -->
    <img src="https://img.shields.io/badge/License-MIT-green" />
    <img src="https://img.shields.io/badge/CLI-Supported-orange" />
    <!-- CI -->
    <a href="https://github.com/cachevector/tablint/actions/workflows/ci.yml"><img src="https://github.com/cachevector/tablint/actions/workflows/ci.yml/badge.svg" /></a>
  </p>
  <p>
    <!-- Features -->
    <img src="https://img.shields.io/badge/Feature-Dataset%20Quality%20Assurance-critical" />
    <img src="https://img.shields.io/badge/Feature-Preprocessing%20%2B%20Profiling-blueviolet" />
    <img src="https://img.shields.io/badge/Feature-Report%20Generation-3f4f75" />
    <img src="https://img.shields.io/badge/Feature-Quick%20Fixes-success" />
  </p>
</div>

> [!NOTE]
> Tablint 0.1.0b1 is the first public beta. `critical` means "do not train this table as-is."

## Overview

**Tablint** is a Python library for intelligent dataset profiling and debugging that acts as a comprehensive pre-training quality assurance tool for machine learning projects.
Think of it as **"Pandas Profiling + PyLint for datasets"**, designed specifically for machine learning workflows.

It catches critical dataset issues before they derail your ML pipeline, explains the problems, and suggests context-aware fixes.  
If you want, Tablint can even apply those fixes for you automatically.


---

## Features

Key features include:

- **Intelligent Profiling**: Detect missing values, skewed distributions, outliers, and data type inconsistencies.
- **ML-Specific Checks**: Identify data leakage, dataset drift, class imbalance, and high-cardinality features.
- **Automated Preparation**: Get suggestions for encoding, imputation, scaling, and transformations.
- **Rich Reporting**: Generate statistical summaries and exportable reports (HTML/PDF/Markdown/JSON) with embedded visualizations.
- **Reviewed preparation code**: Write a pandas cleaning script and a scikit-learn pipeline. Fit the pipeline on the training split. The pandas script computes statistics from the frame you pass in.
- **Modern Themes**: Choose between "Minimal" (professional) and "Neubrutalism" (bold) report styles.

---

## Installation

### Using pip
```bash
pip install tablint
```

### Using uv (recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install tablint
uv pip install tablint

# Or for development from source
git clone https://github.com/cachevector/tablint.git
cd tablint
uv sync
```

After installation, the `tablint` command will be available directly in your terminal.

---

## Usage

Tablint can be used both as a **command-line tool** and as a **Python library**.

### CLI Usage

#### 1. Quick Scan
Get a quick summary of critical issues in your terminal.
```bash
tablint scan dataset.csv
```

**Options:**
- `--critical-only`: Show only critical issues
- `--quiet`: Minimal output (counts only)
- `--json`: Output in JSON format
- `--target COLUMN`: Specify target column for ML-specific checks
- `--checks CHECKS`: Run specific checks (comma-separated)
- `--comparison FILE`: Compare with another dataset for drift detection
- `--preset {gate,profile}`: `gate` is the default and is the training-blocker set. `profile` runs every check.
- `--fail-on {critical,warning}`: Exit 2 when that severity is present. Exit 0 means the bar was not hit. Exit 1 is a usage or runtime error.
- `--sample-size N`: Analyze at most N rows. Sampling stays off unless this is set.
- `--no-sample`: Disable sampling even when `--sample-size` is set.
- `--config FILE`: Load thresholds from a YAML/TOML/JSON config file

**Example:**
```bash
# Block a training job when the table is not trainable
tablint scan train.csv --target Survived --preset gate --fail-on critical

# Quick scan with JSON output
tablint scan dataset.csv --json --quiet
```

#### 2. Detailed Analysis
Get comprehensive details about all detected issues.
```bash
tablint details dataset.csv
```

**Options:** Same as `scan` command (including `--config`)

**Example:**
```bash
tablint details train.csv --target Survived
```

#### 3. Generate Reports
Generate comprehensive reports in multiple formats with visualizations.
```bash
tablint report dataset.csv --format html --theme minimal
```

**Options:**
- `--output PATH`, `-o PATH`: Custom output file path
- `--format {md,json,html,pdf}`: Report format (default: md)
- `--theme {minimal,neubrutalism}`: HTML report theme (default: minimal)
- `--with-code`: Generate Python scripts for fixes and pipelines
- `--full` / `--no-full`: Include/exclude full summaries (default: True)
- `--visualizations` / `--no-visualizations`: Include/exclude plots (default: True)
- `--target COLUMN`: Specify target column
- `--checks CHECKS`: Run specific checks
- `--comparison FILE`: Compare with another dataset for drift detection
- `--preset {gate,profile}`: `profile` is the default for reports. `gate` runs only training blockers.
- `--sample-size N`: Analyze at most N rows. Sampling stays off unless this is set.
- `--no-sample`: Disable sampling even when `--sample-size` is set.
- `--config FILE`: Load thresholds from a YAML/TOML/JSON config file

**Examples:**
```bash
# Generate HTML report with minimal theme
tablint report dataset.csv --format html --theme minimal --full

# Generate PDF report without visualizations (faster)
tablint report dataset.csv --format pdf --no-visualizations

# Generate report with automatic fix scripts
tablint report dataset.csv --with-code

# Generate report with custom output path
tablint report dataset.csv --format html --output my_reports/analysis.html

# This creates:
# - dataset_tablint_report.md (or .html/.pdf/.json)
# - dataset_tablint_report_fixes.py (pandas script)
# - dataset_tablint_report_pipeline.py (sklearn pipeline)

# Compare two datasets for drift detection
tablint report train.csv --comparison test.csv --format html
```

#### 4. List Available Checks
Discover all data quality checks that Tablint can perform.
```bash
tablint checks
```

#### 5. Version
Check Tablint version.
```bash
tablint version
```

#### Available Checks
- `outliers` - Detect outliers using z-score
- `duplicates` - Find duplicate rows
- `high_missing_values` - Columns with high missing data
- `empty_columns` - Completely empty columns
- `dataset_missingness` - Overall missing data patterns
- `missing_patterns` - Correlated missing value patterns
- `high_cardinality` - Categorical columns with too many unique values
- `single_value_columns` - Constant columns with no variance
- `mixed_data_types` - Columns with mixed data types
- `class_imbalance` - Imbalanced target variable (requires --target)
- `feature_correlation` - Highly correlated numeric features
- `categorical_correlation` - Highly associated categorical features
- `mixed_correlation` - Numeric-categorical associations
- `data_leakage` - Columns identical to target
- `target_leakage_patterns` - Features that may leak target information
- `dataset_drift` - Distribution drift between datasets (requires --comparison)
- `uniform_distribution` - Uniformly distributed numeric columns
- `unique_values` - Columns where >95% values are unique
- `high_zero_counts` - Columns with excessive zero values
- `skewness` - Highly skewed numeric distributions
- `infinite_values` - Columns containing infinite values
- `constant_length` - String columns with constant character length
- `extreme_text_lengths` - Text columns with extreme value lengths
- `datetime_skew` - Datetime columns concentrated in one period
- `datetime_future_dates` - Datetime columns with values in the future
- `datetime_gaps` - Anomalous gaps in datetime sequences
- `datetime_monotonicity` - Non-monotonic datetime columns
- `normality` - Non-normal numeric distributions (Shapiro-Wilk / D'Agostino-Pearson)
- `variance_homogeneity` - Unequal variances across target groups (Levene's test, requires --target)
- `low_mutual_information` - Features with near-zero mutual information with the target (requires --target)
- `empty_dataset` - Empty or all-missing datasets

---

### Python Library Usage

#### Basic Analysis
```python
import pandas as pd
from tablint import DatasetAnalyzer

# Load your dataset
df = pd.read_csv("dataset.csv")

# Create analyzer
analyzer = DatasetAnalyzer(df)

# Run analysis
summary = analyzer.analyze()

# Access results
print(f"Critical issues: {summary['critical_count']}")
print(f"Warnings: {summary['warning_count']}")

# Iterate through issues
for issue in summary['issues']:
    print(f"{issue['severity']}: {issue['description']}")
```

#### Analysis with Target Column
```python
# Specify target for ML-specific checks
analyzer = DatasetAnalyzer(
    df,
    target_col='target_column'
)
summary = analyzer.analyze()
```

#### Run Specific Checks
```python
# Only run specific checks
analyzer = DatasetAnalyzer(
    df,
    selected_checks=['outliers', 'high_missing_values', 'class_imbalance']
)
summary = analyzer.analyze()
```

#### Include Visualizations
```python
# Generate analysis with plots
analyzer = DatasetAnalyzer(df, include_plots=True)
summary = analyzer.analyze()

# Plots are stored in summary['summaries']['plots']
```

#### Drift Detection
```python
# Compare two datasets
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

analyzer = DatasetAnalyzer(
    train_df,
    comparison_df=test_df,
    selected_checks=['dataset_drift']
)
summary = analyzer.analyze()
```

#### Generate Reports Programmatically
```python
from tablint.reports import generate_report

# Analyze dataset
analyzer = DatasetAnalyzer(df, include_plots=True)
summary = analyzer.analyze()

# Generate HTML report
generate_report(
    summary,
    format='html',
    full=True,
    output_file='report.html',
    theme='minimal'
)

# Generate PDF report
generate_report(
    summary,
    format='pdf',
    full=True,
    output_file='report.pdf'
)

# Generate JSON report
generate_report(
    summary,
    format='json',
    full=True,
    output_file='report.json'
)

# Generate Markdown report
generate_report(
    summary,
    format='md',
    full=True,
    output_file='report.md'
)
```

#### Generate Fix Scripts
```python
from tablint.checks.core import Issue
from tablint.preparers.codegen import CodeGenerator
from tablint.preparers.pipeline_builder import PipelineBuilder
from tablint.preparers.suggestions import SuggestionProvider

# After running analysis
analyzer = DatasetAnalyzer(df, target_col='target')
summary = analyzer.analyze()

# Convert issues to proper format
issues = [Issue(**i) for i in summary['issues']]
column_types = summary.get('column_types', {})

# Get suggestions
provider = SuggestionProvider(
    issues=issues,
    column_types=column_types,
    target_col='target'
)
suggestions = provider.get_suggestions()

# Generate pandas fix script
codegen = CodeGenerator(suggestions)
fixes_code = codegen.generate_pandas_script()
with open('fixes.py', 'w') as f:
    f.write(fixes_code)

# Generate sklearn pipeline
builder = PipelineBuilder(suggestions)
pipeline_code = builder.generate_pipeline_code()
with open('pipeline.py', 'w') as f:
    f.write(pipeline_code)
```

#### Load Config from File
```python
from tablint.utils.config_loader import load_config
from tablint import DatasetAnalyzer

# Load thresholds from YAML, TOML, or JSON
config = load_config("tablint.yaml")  # or .toml / .json

analyzer = DatasetAnalyzer(df, config=config)
summary = analyzer.analyze()
```

Example `tablint.yaml`:
```yaml
missing_values:
  warning: 0.3
  critical: 0.6
outliers:
  z_score: 3.5
statistical_tests:
  normality_p_value: 0.01
```

Only the keys you specify are overridden; all others fall back to defaults.

#### Custom Sampling
```python
from tablint.utils.sampling import SamplingConfig

# Configure sampling for large datasets
sampling_config = SamplingConfig(max_rows=10000)

analyzer = DatasetAnalyzer(
    df,
    sampling_config=sampling_config,
    auto_sample=True
)
summary = analyzer.analyze()

# Check if sampling occurred
if 'sampling_info' in summary:
    info = summary['sampling_info']
    print(f"Sampled: {info['sample_fraction']*100:.1f}%")
```

---

## Production gate

`DatasetAnalyzer` defaults to the `gate` preset. `tablint report` defaults to `profile`.

`critical` is reserved for defects that should stop a training job: an empty table, an all-null column, missingness at or above the critical threshold, infinite values, duplicate rows above the critical ratio, a column identical or nearly identical to the target, and drift whose effect size is large. Skew, non-normality, ordinary correlation with the target, and zero-inflation of a binary target are warnings, and most of them run only in the `profile` preset.

Stable keys in `analyze()` and in `scan --json` / `details --json`:

- `schema_version` (`"0.2"`), `critical_count`, `warning_count`, `total_issues`
- `issues[]`: `category`, `severity`, `column`, `description`, `impact_score`, `quick_fix`, `statistic`, `effect_size`
- `sampling_info`

`summaries` and plots are best-effort and can change without a major version.

```bash
tablint scan train.csv --target Survived --preset gate --fail-on critical --json
```

Exit 2 when `--fail-on` matches. A job that only checks the exit code should pass `--fail-on critical`.

### Limitations

- Input is CSV, or Parquet when `tablint[parquet]` is installed. HTML, PDF, and plots need `tablint[reports]`.
- Leakage means near-deterministic association with the target, not a proof that a column was built from the label.
- Sampling is off unless you pass `--sample-size` or `auto_sample=True`. Checks then describe the analyzed frame, which is the full table by default.
- Generated pandas code learns fill values from the frame you pass. Pass the training split, or fit the generated sklearn pipeline on that split.

---

## License

This project is licensed under the [**MIT License**](./LICENSE).

---

## Contributing

We welcome contributions from the community to make Tablint better!

Before you get started, please:

- Review our [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines and setup instructions
- Write clean, well-documented code
- Follow best practices for the stack or component you’re working on
- Open a pull request (PR) with a clear description of your changes and motivation

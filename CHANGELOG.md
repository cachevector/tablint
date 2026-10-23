# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0b1] - 2026-10-23

Project renamed from `hashprep` to `tablint`. This beta ships the training-gate behaviour previously developed as hashprep 0.2.0.

### Changed
- Distribution name, import package, and CLI are `tablint`.
- `HashPrepConfig` is now `TablintConfig`.
- Report filenames use the `_tablint_report` suffix.

## [0.2.0] - 2026-10-20

### Breaking
- `critical` means a training blocker. Non-normality is always a warning. Drift is critical only when the shift is large, not merely when the p-value is small.
- `DatasetAnalyzer` and `tablint scan` / `details` default to the `gate` preset. `tablint report` defaults to `profile`. Pass `preset="profile"` or `--preset profile` for the previous full catalogue.
- Sampling is off unless `--sample-size` or `auto_sample=True` is set.
- `scan --json` now uses `schema_version`, `critical_count`, `warning_count`, `total_issues`, `issues`, and `sampling_info`. `details --json` prints the same object.
- F-statistic leakage thresholds are ignored. Leakage uses correlation, bias-corrected Cramér's V, or correlation ratio.
- Plots, HTML, and PDF require `pip install "tablint[reports]"`. Parquet requires `pip install "tablint[parquet]"`.

### Added
- Column roles (`target`, `identifier`, `boolean`, `categorical`, `numeric`, `datetime`, `text`) shared by every check.
- `--preset`, `--fail-on`, and Parquet input.
- `statistic` and `effect_size` on each issue.
- Generated code escapes column names. Sklearn steps with the same transformation are grouped. Outlier clipping is a real pre-pipeline function.

## [0.1.0] - 2026-05-22

### Added
- First official stable release.
- Comprehensive dataset profiling and health checks.
- Support for multiple report formats: Markdown, JSON, HTML, and PDF.
- Two HTML report themes: `minimal` and `neubrutalism`.
- Automatic suggestion provider for data quality issues.
- Code generation for pandas fix scripts.
- Sklearn preprocessing pipeline generation.
- CLI commands: `scan`, `details`, `report`, `checks`, and `version`.
- Robust error handling for invalid files, empty datasets, and malformed configurations.
- Configuration support via YAML, TOML, and JSON.
- Intelligent sampling for large datasets.
- Dataset drift detection.
- Mutual information and statistical checks.

### Changed
- Refactored report generators for robust lazy loading.
- Improved CLI output with better error messages and color-coded statuses.
- Updated documentation and website for stable release.

### Fixed
- Fixed crash when generating reports for single-row datasets.
- Fixed dependency issues in report generation when optional libraries are missing.
- Fixed non-deterministic order in generated fix scripts.

## [0.1.0b3] - 2026-04-15
- Initial beta release with core features.

import numpy as np
import pandas as pd
from scipy.stats import chisquare, ks_2samp

from ..config import DEFAULT_CONFIG
from ..utils.logging import get_logger
from ..utils.type_inference import infer_roles, infer_types
from .core import Issue

_log = get_logger("checks.drift")

_DRIFT = DEFAULT_CONFIG.drift


def _drift_severity(
    p_val: float, effect: float, threshold: float, drift_cfg, effect_warning: float, effect_critical: float
):
    """Report drift only when the test is significant and the shift is large enough."""
    if p_val >= threshold or effect < effect_warning:
        return None
    if p_val < drift_cfg.critical_p_value and effect >= effect_critical:
        return "critical"
    return "warning"


def check_drift(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    threshold: float = _DRIFT.p_value,
    config=None,
    hashprep_config=None,
) -> list[Issue]:
    """
    Check for distribution shift between two datasets.
    Uses Kolmogorov-Smirnov test for numeric and datetime columns and Chi-square for categorical.
    """
    if not isinstance(df_train, pd.DataFrame) or not isinstance(df_test, pd.DataFrame):
        raise TypeError("Both df_train and df_test must be pandas DataFrames")

    drift_cfg = config if config is not None else (hashprep_config.drift if hashprep_config is not None else _DRIFT)
    full_config = hashprep_config if hashprep_config is not None else DEFAULT_CONFIG
    roles = infer_roles(df_train, infer_types(df_train, full_config), config=full_config)
    issues = []

    issues.extend(_check_numeric_drift(df_train, df_test, threshold, drift_cfg, roles))
    issues.extend(_check_categorical_drift(df_train, df_test, threshold, drift_cfg, roles))

    return issues


def _numeric_drift_values(series: pd.Series, role: str) -> pd.Series:
    if role == "datetime":
        parsed = pd.to_datetime(series, errors="coerce").dropna()
        if parsed.empty:
            return parsed
        return parsed.astype("int64")
    return series.dropna()


def _check_numeric_drift(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    threshold: float,
    drift_cfg,
    roles: dict[str, str],
) -> list[Issue]:
    """Check numeric and datetime columns for distribution drift using KS-test."""
    issues = []
    num_cols = [col for col, role in roles.items() if role in ("numeric", "datetime")]

    for col in num_cols:
        if col not in df_test.columns:
            continue

        train_vals = _numeric_drift_values(df_train[col], roles[col])
        test_vals = _numeric_drift_values(df_test[col], roles[col])

        if len(train_vals) == 0 or len(test_vals) == 0:
            continue

        stat, p_val = ks_2samp(train_vals, test_vals)
        severity = _drift_severity(
            p_val, float(stat), threshold, drift_cfg, drift_cfg.ks_warning, drift_cfg.ks_critical
        )
        if severity:
            kind = "datetime" if roles[col] == "datetime" else "numeric"
            issues.append(
                Issue(
                    category="dataset_drift",
                    severity=severity,
                    column=col,
                    description=(
                        f"Drift detected in {kind} column '{col}' (KS statistic: {float(stat):.3f}, p-value: {p_val:.4f})"
                    ),
                    impact_score="high" if severity == "critical" else "medium",
                    statistic=float(p_val),
                    effect_size=float(stat),
                    quick_fix="Options:\n- Re-train model with recent data.\n- Investigate data collection differences.\n- Use drift-robust features.",
                )
            )

    return issues


def _check_categorical_drift(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    threshold: float,
    drift_cfg,
    roles: dict[str, str],
) -> list[Issue]:
    """Check categorical columns for distribution drift using Chi-square test."""
    issues = []
    cat_cols = [col for col, role in roles.items() if role in ("categorical", "boolean", "text", "target")]

    for col in cat_cols:
        if col not in df_test.columns:
            continue

        train_counts = df_train[col].value_counts()
        test_counts = df_test[col].value_counts()

        new_categories = set(test_counts.index) - set(train_counts.index)
        if new_categories:
            sample_new = list(new_categories)[: drift_cfg.max_new_category_samples]
            issues.append(
                Issue(
                    category="dataset_drift",
                    severity="warning",
                    column=col,
                    description=f"New categories in test set for '{col}': {sample_new}{'...' if len(new_categories) > drift_cfg.max_new_category_samples else ''}",
                    impact_score="medium",
                    quick_fix="Handle unseen categories in preprocessing pipeline (e.g., OrdinalEncoder with unknown_value).",
                )
            )

        all_cats = list(set(train_counts.index) | set(test_counts.index))
        if len(all_cats) > drift_cfg.max_categories_for_chi2:
            continue

        train_total = train_counts.sum()
        test_total = test_counts.sum()

        if train_total == 0 or test_total == 0:
            continue

        observed = []
        expected = []

        for cat in all_cats:
            observed.append(test_counts.get(cat, 0))
            train_freq = train_counts.get(cat, 0) / train_total
            expected.append(train_freq * test_total)

        observed_arr = np.array(observed, dtype=float)
        expected_arr = np.array(expected, dtype=float)

        expected_arr = np.where(expected_arr < 1e-10, 1e-10, expected_arr)

        try:
            _chi2_stat, p_val = chisquare(observed_arr, f_exp=expected_arr)
            train_prob = expected_arr / expected_arr.sum()
            test_prob = observed_arr / observed_arr.sum()
            distance = float(0.5 * np.abs(test_prob - train_prob).sum())
            severity = _drift_severity(
                p_val,
                distance,
                threshold,
                drift_cfg,
                drift_cfg.distance_warning,
                drift_cfg.distance_critical,
            )

            if severity:
                issues.append(
                    Issue(
                        category="dataset_drift",
                        severity=severity,
                        column=col,
                        description=(
                            f"Drift detected in categorical column '{col}' "
                            f"(total variation: {distance:.3f}, Chi-square p-value: {p_val:.4f})"
                        ),
                        impact_score="high" if severity == "critical" else "medium",
                        statistic=float(p_val),
                        effect_size=distance,
                        quick_fix="Options:\n- Re-train model with recent data.\n- Investigate category distribution changes.\n- Consider rebalancing categories.",
                    )
                )
        except (ValueError, RuntimeWarning) as e:
            _log.debug("Chi-square drift test failed for '%s': %s", col, e)

    return issues

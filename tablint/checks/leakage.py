import numpy as np
import pandas as pd

from ..utils.logging import get_logger
from .core import Issue
from .correlations import _cramers_v_corrected
from .roles import column_roles, columns_with_roles

_log = get_logger("checks.leakage")

_LEAKAGE_CRITICAL_FIX = (
    "Options: \n- Drop column: Prevents target leakage (Pros: Ensures model integrity; Cons: Loses feature info)."
    "\n- Verify feature: Check if correlation is valid or data-derived (Pros: Validates data; Cons: Time-consuming)."
)
_LEAKAGE_WARNING_FIX = (
    "Options: \n- Drop column: Reduces leakage risk (Pros: Safer model; Cons: May lose predictive info)."
    "\n- Retain and test: Use robust models (e.g., trees) and evaluate (Pros: Keeps potential signal; Cons: Risk of overfitting)."
    "\n- Engineer feature: Transform to reduce correlation (Pros: Retains info; Cons: Adds complexity)."
)


def _check_data_leakage(analyzer):
    issues = []
    if analyzer.target_col and analyzer.target_col in analyzer.df.columns:
        target = analyzer.df[analyzer.target_col]
        for col in analyzer.df.columns:
            if col == analyzer.target_col:
                continue
            if analyzer.df[col].equals(target):
                issues.append(
                    Issue(
                        category="data_leakage",
                        severity="critical",
                        column=col,
                        description=f"Column '{col}' is identical to target '{analyzer.target_col}'",
                        impact_score="high",
                        quick_fix="Options: \n- Drop column: Prevents data leakage (Pros: Ensures model integrity; Cons: Loses potential feature info).\n- Verify data collection: Ensure column isn't target-derived (Pros: Validates data; Cons: Time-consuming).",
                    )
                )
    return issues


def _association_severity(value: float, warning: float, critical: float) -> str | None:
    if not np.isfinite(value):
        return None
    if value >= critical:
        return "critical"
    if value >= warning:
        return "warning"
    return None


def _correlation_ratio(labels: pd.Series, values: pd.Series) -> float:
    """Return eta, in [0, 1], for a numeric feature against a categorical target."""
    frame = pd.DataFrame({"label": labels, "value": pd.to_numeric(values, errors="coerce")}).dropna()
    if len(frame) < 3:
        return 0.0
    overall = float(frame["value"].mean())
    ss_total = float(((frame["value"] - overall) ** 2).sum())
    if ss_total == 0:
        return 0.0
    ss_between = 0.0
    for _, group in frame.groupby("label", observed=True):
        ss_between += len(group) * (float(group["value"].mean()) - overall) ** 2
    return float(np.sqrt(ss_between / ss_total))


def _append_leakage(issues: list[Issue], column: str, severity: str, description: str, effect: float) -> None:
    issues.append(
        Issue(
            category="target_leakage",
            severity=severity,
            column=column,
            description=description,
            impact_score="high" if severity == "critical" else "medium",
            statistic=effect,
            effect_size=effect,
            quick_fix=_LEAKAGE_CRITICAL_FIX if severity == "critical" else _LEAKAGE_WARNING_FIX,
        )
    )


def _check_target_leakage_patterns(analyzer):
    """Flag near-deterministic association with the target.

    Numeric pairs use absolute Pearson correlation. Categorical pairs use
    bias-corrected Cramér's V. Mixed pairs use the correlation ratio (eta).
    Ordinary predictive signal stays below the warning thresholds.
    """
    _leak = analyzer.config.leakage
    issues = []
    if not analyzer.target_col or analyzer.target_col not in analyzer.df.columns:
        return issues

    target = analyzer.df[analyzer.target_col]
    roles = column_roles(analyzer)
    target_is_numeric = roles.get(analyzer.target_col) == "target" and (
        pd.api.types.is_numeric_dtype(target)
        and target.nunique(dropna=True) > analyzer.config.type_inference.num_low_cat_threshold
    )

    for col in columns_with_roles(analyzer, "numeric"):
        if target_is_numeric:
            paired = pd.DataFrame({col: analyzer.df[col], "target": target}).dropna()
            if len(paired) < 3 or paired[col].std(ddof=0) == 0 or paired["target"].std(ddof=0) == 0:
                continue
            effect = float(paired[col].corr(paired["target"]))
            effect = abs(effect)
            warning, critical = _leak.numeric_warning, _leak.numeric_critical
            label = "correlation"
        else:
            effect = _correlation_ratio(target, analyzer.df[col])
            warning, critical = _leak.numeric_warning, _leak.numeric_critical
            label = "correlation ratio"
        severity = _association_severity(effect, warning, critical)
        if severity:
            _append_leakage(
                issues,
                col,
                severity,
                f"Column '{col}' is nearly determined by the target ({label}: {effect:.2f})",
                effect,
            )

    for col in columns_with_roles(analyzer, "categorical", "boolean"):
        if target_is_numeric:
            effect = _correlation_ratio(analyzer.df[col], target)
            warning, critical = _leak.numeric_warning, _leak.numeric_critical
            label = "correlation ratio"
        else:
            try:
                table = pd.crosstab(target, analyzer.df[col])
                effect = float(_cramers_v_corrected(table))
            except (ValueError, np.linalg.LinAlgError, ZeroDivisionError) as e:
                _log.debug("Cramer's V leakage test failed for '%s': %s", col, e)
                continue
            warning, critical = _leak.categorical_warning, _leak.categorical_critical
            label = "Cramer's V"
        severity = _association_severity(effect, warning, critical)
        if severity:
            _append_leakage(
                issues,
                col,
                severity,
                f"Column '{col}' is nearly determined by the target ({label}: {effect:.2f})",
                effect,
            )

    return issues

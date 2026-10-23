import warnings

import numpy as np
import pandas as pd

from ..config import DEFAULT_CONFIG, TablintConfig

_TYPE_TO_ROLE = {
    "Numeric": "numeric",
    "Categorical": "categorical",
    "Text": "text",
    "DateTime": "datetime",
    "Boolean": "boolean",
    "Unsupported": "unsupported",
}


def _type_config(config: TablintConfig | None):
    cfg = config or DEFAULT_CONFIG
    return cfg, cfg.type_inference, cfg.datetime


def _looks_like_datetime(series: pd.Series, parse_threshold: float) -> bool:
    """Return True if an object/string column parses as datetime above the threshold."""
    sample = series.dropna().head(200)
    if len(sample) == 0:
        return False
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed = pd.to_datetime(sample, errors="coerce")
    parse_ratio = parsed.notna().mean()
    return float(parse_ratio) >= parse_threshold


def _has_infinity(series: pd.Series) -> bool:
    if not pd.api.types.is_numeric_dtype(series):
        return False
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return bool(np.isinf(values).any())


def _is_boolean_text(series: pd.Series, mappings: dict) -> bool:
    if series.empty:
        return False
    sample = series.dropna().astype(str).str.lower()
    if sample.empty:
        return False
    return bool(sample.isin(list(mappings)).all())


def infer_types(df: pd.DataFrame, config: TablintConfig | None = None) -> dict[str, str]:
    """
    Infer semantic types per ydata logic.
    Returns: {col: 'Numeric' | 'Categorical' | 'Text' | 'DateTime' | 'Boolean' | 'Unsupported'}
    """
    _, type_cfg, dt_cfg = _type_config(config)
    types = {}
    for col in df.columns:
        series = df[col].dropna()
        if series.empty:
            types[col] = "Unsupported"
            continue

        if pd.api.types.is_datetime64_any_dtype(series):
            types[col] = "DateTime"

        elif pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
            # Infinities are a numeric defect even when the column has few distinct values.
            if _has_infinity(series):
                types[col] = "Numeric"
            elif 1 <= series.nunique() <= type_cfg.num_low_cat_threshold:
                types[col] = "Categorical"
            else:
                types[col] = "Numeric"

        elif pd.api.types.is_bool_dtype(series):
            types[col] = "Categorical"

        elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
            n_unique = series.nunique()
            unique_pct = n_unique / len(series)
            if _is_boolean_text(series, type_cfg.bool_mappings):
                types[col] = "Categorical"
            elif _looks_like_datetime(series, dt_cfg.parse_threshold):
                types[col] = "DateTime"
            elif 1 <= n_unique <= type_cfg.cat_cardinality_threshold and unique_pct < type_cfg.cat_percentage_threshold:
                types[col] = "Categorical"
            else:
                types[col] = "Text"

        elif pd.api.types.is_categorical_dtype(series):
            types[col] = "Categorical"

        else:
            types[col] = "Unsupported"

    return types


def infer_roles(
    df: pd.DataFrame,
    column_types: dict[str, str],
    target_col: str | None = None,
    config: TablintConfig | None = None,
) -> dict[str, str]:
    """Classify each column for checks.

    Roles: target, identifier, boolean, categorical, numeric, datetime, text, unsupported.
    The target wins over every other role. Identifiers are columns whose non-null
    unique ratio reaches the configured threshold. Low-cardinality integers stay categorical.
    """
    cfg, type_cfg, _ = _type_config(config)
    unique_ratio_threshold = cfg.distribution.unique_value_ratio
    roles: dict[str, str] = {}

    for col in df.columns:
        if target_col is not None and col == target_col:
            roles[col] = "target"
            continue

        if _has_infinity(df[col]):
            roles[col] = "numeric"
            continue

        non_null = df[col].dropna()
        unique_ratio = (non_null.nunique() / len(non_null)) if len(non_null) >= 2 else 0.0
        # Integer ids and free-text ids repeat only by accident. A float with a
        # distinct value on every row is still a measurement, so it stays numeric.
        label_like = (
            pd.api.types.is_integer_dtype(non_null)
            or pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_string_dtype(df[col])
            or isinstance(df[col].dtype, pd.CategoricalDtype)
        )
        if unique_ratio >= unique_ratio_threshold and label_like:
            roles[col] = "identifier"
            continue

        if pd.api.types.is_bool_dtype(df[col]) or _is_boolean_text(non_null, type_cfg.bool_mappings):
            roles[col] = "boolean"
            continue

        roles[col] = _TYPE_TO_ROLE.get(column_types.get(col, "Unsupported"), "unsupported")

    return roles


# Helper: Check if series is constant/empty (skip corr)
def is_usable_for_corr(series: pd.Series) -> bool:
    return series.nunique() > 1 and len(series.dropna()) > 1

from ..models import FixSuggestion
from .base import FixStrategy


class OutlierStrategy(FixStrategy):
    """Strategy for handling outliers through clipping or removal."""

    SKLEARN_IMPORTS = [
        "from sklearn.preprocessing import RobustScaler",
    ]

    def generate_pandas_code(self, suggestion: FixSuggestion) -> str:
        cols = suggestion.columns
        clip_method = suggestion.parameters.get("clip_method", "iqr")

        if clip_method == "iqr":
            return self._generate_iqr_code(cols)

        if clip_method == "percentile":
            lower_pct = suggestion.parameters.get("lower_pct", 0.01)
            upper_pct = suggestion.parameters.get("upper_pct", 0.99)
            lines = []
            for index, col in enumerate(cols):
                ref = self._ref(col)
                lines.append(f"_low_{index}, _high_{index} = {ref}.quantile([{lower_pct}, {upper_pct}])")
                lines.append(f"{ref} = {ref}.clip(lower=_low_{index}, upper=_high_{index})")
            return "\n".join(lines)

        if clip_method == "zscore":
            z_threshold = suggestion.parameters.get("z_threshold", 3.0)
            lines = []
            for index, col in enumerate(cols):
                ref = self._ref(col)
                lines.append(f"_mean_{index} = {ref}.mean()")
                lines.append(f"_std_{index} = {ref}.std()")
                lines.append(f"_lower_{index} = _mean_{index} - {z_threshold} * _std_{index}")
                lines.append(f"_upper_{index} = _mean_{index} + {z_threshold} * _std_{index}")
                lines.append(f"{ref} = {ref}.clip(lower=_lower_{index}, upper=_upper_{index})")
            return "\n".join(lines)

        return self._generate_iqr_code(cols)

    def _generate_iqr_code(self, cols: list[str]) -> str:
        lines = []
        for index, col in enumerate(cols):
            ref = self._ref(col)
            lines.append(f"_q1_{index}, _q3_{index} = {ref}.quantile([0.25, 0.75])")
            lines.append(f"_iqr_{index} = _q3_{index} - _q1_{index}")
            lines.append(
                f"{ref} = {ref}.clip(lower=_q1_{index} - 1.5 * _iqr_{index}, upper=_q3_{index} + 1.5 * _iqr_{index})"
            )
        return "\n".join(lines)

    def get_sklearn_transformer(self, suggestion: FixSuggestion) -> tuple[str | None, list[str]]:
        return None, suggestion.columns

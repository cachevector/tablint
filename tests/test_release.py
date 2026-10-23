"""Release coverage for the public library, CLI, and generated-code contract.

These tests lock the behavior a 0.2 caller can depend on. They sit beside the
narrower unit tests and fail when a check, preset, report, or script drifts.
"""

import json

import numpy as np
import pandas as pd
import pytest
from click.testing import CliRunner

import tablint
from tablint import DatasetAnalyzer, load_config
from tablint.checks.core import Issue
from tablint.checks.drift import check_drift
from tablint.config import config_from_dict
from tablint.interfaces.cli.main import cli
from tablint.preparers.codegen import CodeGenerator
from tablint.preparers.models import FixSuggestion, FixType, ImputeMethod
from tablint.preparers.pipeline_builder import PipelineBuilder
from tablint.preparers.suggestions import SuggestionProvider
from tablint.reports import generate_report
from tablint.utils.type_inference import infer_roles, infer_types

ISSUE_KEYS = {
    "category",
    "severity",
    "column",
    "description",
    "impact_score",
    "quick_fix",
    "statistic",
    "effect_size",
}


def _invoke(args):
    return CliRunner().invoke(cli, args)


def _roles(frame, target=None):
    types = infer_types(frame)
    return infer_roles(frame, types, target_col=target)


class TestColumnRoles:
    def test_roles_distinguish_ids_codes_and_measurements(self):
        frame = pd.DataFrame(
            {
                "passenger_id": range(60),
                "pclass": [1, 2, 3] * 20,
                "age": np.linspace(1.0, 60.0, 60),
                "flag": ["yes", "no"] * 30,
                "name": [f"person-{i}" for i in range(60)],
                "note": ["short", "also short"] * 30,
            }
        )
        roles = _roles(frame, target="pclass")

        assert roles["pclass"] == "target"
        assert roles["passenger_id"] == "identifier"
        assert roles["name"] == "identifier"
        assert roles["age"] == "numeric"
        assert roles["flag"] == "boolean"
        assert roles["note"] == "categorical"

    def test_infinity_stays_numeric_even_when_values_are_unique(self):
        values = np.arange(25, dtype=float)
        values[-1] = np.inf
        frame = pd.DataFrame({"broken": values})
        assert _roles(frame)["broken"] == "numeric"

    def test_float_measurement_is_not_an_identifier(self):
        rng = np.random.default_rng(4)
        frame = pd.DataFrame({"reading": rng.normal(size=40)})
        assert _roles(frame)["reading"] == "numeric"


class TestAnalyzerContract:
    def test_rejects_bad_inputs(self):
        frame = pd.DataFrame({"y": [0, 1], "x": [1.0, 2.0]})
        with pytest.raises(TypeError):
            DatasetAnalyzer([1, 2, 3])
        with pytest.raises(ValueError, match="duplicate column"):
            DatasetAnalyzer(pd.DataFrame([[1, 2]], columns=["a", "a"]))
        with pytest.raises(ValueError, match="not found"):
            DatasetAnalyzer(frame, target_col="missing")
        with pytest.raises(TypeError, match="comparison_df"):
            DatasetAnalyzer(frame, comparison_df=[1, 2])
        with pytest.raises(ValueError, match="preset"):
            DatasetAnalyzer(frame, preset="audit")

    def test_gate_and_profile_select_different_checks(self):
        rng = np.random.default_rng(5)
        frame = pd.DataFrame(
            {
                "y": [0, 1] * 100,
                "skewed": rng.exponential(size=200),
                "id": range(200),
            }
        )
        gate = DatasetAnalyzer(frame, target_col="y", preset="gate").analyze()
        profile = DatasetAnalyzer(frame, target_col="y", preset="profile").analyze()

        assert all(issue["category"] != "normality" for issue in gate["issues"])
        assert any(issue["category"] == "normality" and issue["severity"] == "warning" for issue in profile["issues"])
        assert any(issue["category"] == "unique_values" and issue["column"] == "id" for issue in gate["issues"])
        assert all(issue["category"] != "high_cardinality" or issue["column"] != "id" for issue in profile["issues"])

    def test_every_issue_has_the_stable_fields(self):
        frame = pd.DataFrame({"y": [0, 1] * 20, "empty": [np.nan] * 40, "x": np.linspace(0, 1, 40)})
        summary = DatasetAnalyzer(frame, target_col="y").analyze()

        assert summary["schema_version"] == "0.2"
        assert set(summary) >= {
            "schema_version",
            "critical_count",
            "warning_count",
            "total_issues",
            "issues",
            "sampling_info",
        }
        assert summary["issues"]
        assert set(summary["issues"][0]) >= ISSUE_KEYS
        assert "memory_exceeded" in summary["sampling_info"]
        assert summary["sampling_info"]["was_sampled"] is False
        assert summary["summaries"]["dataset_info"]["rows"] == 40

    def test_explicit_sample_is_recorded_and_limits_rows(self):
        from tablint.utils.sampling import SamplingConfig

        frame = pd.DataFrame({"x": range(300)})
        summary = DatasetAnalyzer(
            frame,
            sampling_config=SamplingConfig(max_rows=50),
            auto_sample=True,
            selected_checks=["empty_dataset"],
        ).analyze()
        assert summary["sampling_info"]["was_sampled"] is True
        assert summary["summaries"]["dataset_info"]["rows"] == 50


class TestSeverity:
    def test_blockers_are_critical_and_ordinary_signal_is_not(self):
        rng = np.random.default_rng(6)
        rows = 200
        signal = rng.normal(size=rows)
        target = signal + rng.normal(scale=2.0, size=rows)
        leaked = target + rng.normal(scale=0.001, size=rows)
        repeated = pd.concat([pd.DataFrame({"y": [0], "x": [1.0]})] * 40, ignore_index=True)
        frame = pd.DataFrame(
            {
                "y": target,
                "signal": signal,
                "leaked": leaked,
                "label": ["a"] * 190 + ["b"] * 10,
            }
        )

        summary = DatasetAnalyzer(frame, target_col="y", preset="profile").analyze()
        leakage = [issue for issue in summary["issues"] if issue["column"] == "leaked"]
        assert any(issue["category"] == "target_leakage" and issue["severity"] == "critical" for issue in leakage)
        assert all(issue["column"] != "signal" or issue["category"] != "target_leakage" for issue in summary["issues"])

        imbalance = DatasetAnalyzer(frame, target_col="label", selected_checks=["class_imbalance"]).analyze()
        assert imbalance["issues"][0]["severity"] == "warning"
        assert imbalance["critical_count"] == 0

        duplicates = DatasetAnalyzer(repeated, selected_checks=["duplicates"]).analyze()
        assert duplicates["issues"][0]["severity"] == "critical"

    def test_small_shift_is_not_critical_drift_and_integer_codes_use_categories(self):
        rng = np.random.default_rng(7)
        train = pd.DataFrame({"amount": rng.normal(0, 1, 1500), "code": [1, 2, 3] * 500})
        nudged = pd.DataFrame({"amount": rng.normal(0.02, 1, 1500), "code": [1, 2, 3] * 500})
        shifted = pd.DataFrame({"amount": rng.normal(8, 1, 1500), "code": [1] * 1200 + [2] * 200 + [3] * 100})

        quiet = check_drift(train, nudged)
        assert all(issue.column != "amount" or issue.severity != "critical" for issue in quiet)

        loud = check_drift(train, shifted)
        amount = next(issue for issue in loud if issue.column == "amount")
        code = next(issue for issue in loud if issue.column == "code")
        assert amount.severity == "critical"
        assert amount.effect_size >= 0.25
        assert "categorical" in code.description
        assert code.effect_size is not None

    def test_constant_target_is_critical(self):
        frame = pd.DataFrame({"y": [1] * 30, "x": range(30)})
        summary = DatasetAnalyzer(frame, target_col="y", selected_checks=["single_value_columns"]).analyze()
        assert summary["issues"][0]["severity"] == "critical"
        assert summary["issues"][0]["column"] == "y"


class TestPreparation:
    def test_suggestions_drop_critical_missing_data_and_impute_partial_numbers(self):
        provider = SuggestionProvider(
            issues=[
                Issue("missing_values", "critical", "cabin", "80.0% missing values in 'cabin'", "high", "drop"),
                Issue("missing_values", "warning", "age", "20.0% missing values in 'age'", "medium", "impute"),
            ],
            column_types={"cabin": "Text", "age": "Numeric"},
        )
        by_column = {suggestion.columns[0]: suggestion for suggestion in provider.get_suggestions()}
        assert by_column["cabin"].fix_type == FixType.DROP_COLUMN
        assert by_column["age"].fix_type == FixType.IMPUTE
        assert by_column["age"].method == ImputeMethod.MEDIAN.value

    def test_empty_mode_does_not_crash_generated_code(self):
        column = "city"
        suggestion = FixSuggestion(
            fix_type=FixType.IMPUTE,
            columns=[column],
            method=ImputeMethod.MODE.value,
            reason="Missing category",
        )
        namespace: dict = {}
        exec(CodeGenerator([suggestion]).generate_pandas_script(), namespace)
        result = namespace["apply_fixes"](pd.DataFrame({column: [np.nan, np.nan]}))
        assert result[column].isna().all()

    def test_same_imputers_share_one_sklearn_step(self):
        suggestions = [
            FixSuggestion(FixType.IMPUTE, ["age"], method=ImputeMethod.MEDIAN.value, reason="age"),
            FixSuggestion(FixType.IMPUTE, ["fare"], method=ImputeMethod.MEDIAN.value, reason="fare"),
        ]
        code = PipelineBuilder(suggestions).generate_pipeline_code()
        assert code.count("SimpleImputer(") == 1
        assert "age" in code and "fare" in code

        namespace: dict = {}
        exec(code, namespace)
        frame = pd.DataFrame({"age": [1.0, np.nan, 3.0], "fare": [4.0, 8.0, np.nan]})
        transformed = namespace["build_preprocessing_pipeline"]().fit_transform(frame)
        assert transformed.shape == (3, 2)
        assert not np.isnan(transformed).any()

    def test_clip_step_is_runnable(self):
        suggestion = FixSuggestion(
            fix_type=FixType.CLIP_OUTLIERS,
            columns=["fare"],
            reason="Clip",
        )
        code = PipelineBuilder([suggestion]).generate_pipeline_code()
        assert "_clip_outliers" in code
        assert "None" not in code.split("def get_pre_pipeline_steps", 1)[1]

        namespace: dict = {}
        exec(code, namespace)
        frame = pd.DataFrame({"fare": [1.0, 2.0, 3.0, 4.0, 10_000.0]})
        clipped = namespace["get_pre_pipeline_steps"]()[0][1](frame)
        assert clipped["fare"].max() < 10_000


class TestReportsAndConfig:
    def test_html_report_escapes_dataset_text(self):
        column = '"><script>alert(1)</script>'
        value = "<img src=x onerror=alert(1)>"
        frame = pd.DataFrame({column: [value, "ok"] * 8})
        summary = DatasetAnalyzer(frame, include_plots=False, preset="profile").analyze()

        for theme in ("minimal", "neubrutalism"):
            html = generate_report(summary, format="html", full=True, theme=theme)
            assert "<script>alert(1)</script>" not in html
            assert "<img src=x onerror=alert(1)>" not in html
            assert "&lt;script&gt;" in html
            assert "<table" in html

    def test_markdown_and_json_reports_round_trip_without_plots(self, tmp_path):
        frame = pd.DataFrame({"y": [0, 1] * 15, "empty": [np.nan] * 30})
        summary = DatasetAnalyzer(frame, target_col="y", include_plots=False).analyze()

        markdown_path = tmp_path / "report.md"
        json_path = tmp_path / "report.json"
        generate_report(summary, format="md", full=False, output_file=str(markdown_path))
        generate_report(summary, format="json", full=True, output_file=str(json_path))

        markdown = markdown_path.read_text()
        assert "empty" in markdown
        payload = json.loads(json_path.read_text())
        assert payload["metadata"]["version"] == tablint.__version__
        assert payload["alerts"]["issues"]
        assert payload["alerts"]["issues"][0]["severity"] in {"critical", "warning"}

    def test_unknown_report_format_is_rejected(self, tmp_path):
        frame = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
        summary = DatasetAnalyzer(frame, selected_checks=[]).analyze()
        with pytest.raises(ValueError, match="Unsupported format"):
            generate_report(summary, format="xml", output_file=str(tmp_path / "report.xml"))

    def test_drift_thresholds_load_and_unknown_keys_fail(self, tmp_path):
        loaded = config_from_dict({"drift": {"ks_critical": 0.4, "distance_warning": 0.2}})
        assert loaded.drift.ks_critical == 0.4
        assert loaded.drift.distance_warning == 0.2
        assert loaded.missing_values.critical == config_from_dict({}).missing_values.critical

        with pytest.raises(ValueError, match="Unknown configuration key"):
            config_from_dict({"drift": {"not_a_threshold": 1}})

        path = tmp_path / "tablint.json"
        path.write_text(json.dumps({"drift": {"ks_warning": 0.2}}))
        assert load_config(path).drift.ks_warning == 0.2


class TestCommandLine:
    def test_parquet_scan_uses_the_same_json_contract(self, tmp_path):
        path = tmp_path / "batch.parquet"
        pd.DataFrame({"y": [0, 1] * 20, "x": np.linspace(0, 1, 40)}).to_parquet(path)
        result = _invoke(["scan", str(path), "--target", "y", "--json", "--preset", "gate"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["schema_version"] == "0.2"
        assert payload["critical_count"] == 0

    def test_fail_on_warning_exits_when_only_warnings_exist(self, tmp_path):
        path = tmp_path / "ids.csv"
        pd.DataFrame({"y": [0, 1] * 15, "row_id": range(30)}).to_csv(path, index=False)

        warned = _invoke(["scan", str(path), "--target", "y", "--preset", "gate", "--fail-on", "warning"])
        clean = _invoke(["scan", str(path), "--target", "y", "--preset", "gate", "--fail-on", "critical"])
        assert warned.exit_code == 2
        assert clean.exit_code == 0

    def test_checks_command_lists_the_gate_set(self):
        result = _invoke(["checks"])
        assert result.exit_code == 0
        for name in DatasetAnalyzer.GATE_CHECKS:
            assert name in result.output

    def test_details_json_matches_scan_json(self, tmp_path):
        path = tmp_path / "tiny.csv"
        pd.DataFrame({"y": [0, 1, 0, 1], "x": [1.0, 2.0, 3.0, 4.0]}).to_csv(path, index=False)
        scan = _invoke(["scan", str(path), "--json", "--preset", "gate"])
        details = _invoke(["details", str(path), "--json", "--preset", "gate"])
        assert scan.exit_code == details.exit_code == 0
        assert json.loads(scan.output) == json.loads(details.output)

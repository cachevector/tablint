"""Acceptance tests for the 0.2 production gate contract."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from click.testing import CliRunner

from hashprep import DatasetAnalyzer
from hashprep.interfaces.cli.main import _json_payload, cli

TITANIC = Path(__file__).parent.parent / "datasets" / "train.csv"


def _invoke(args):
    return CliRunner().invoke(cli, args)


def _critical(summary):
    return [issue for issue in summary["issues"] if issue["severity"] == "critical"]


class TestGateContract:
    def test_titanic_gate_critical_is_cabin_only(self):
        df = pd.read_csv(TITANIC)
        summary = DatasetAnalyzer(df, target_col="Survived", preset="gate").analyze()

        critical = _critical(summary)
        assert {issue["column"] for issue in critical} == {"Cabin"}
        assert {issue["category"] for issue in critical} == {"missing_values"}
        assert summary["schema_version"] == "0.2"
        assert summary["sampling_info"]["was_sampled"] is False

        warned = {(issue["category"], issue["column"]) for issue in summary["issues"]}
        assert ("unique_values", "Name") in warned
        assert ("unique_values", "PassengerId") in warned
        assert all(issue["category"] != "normality" for issue in summary["issues"])
        assert all(
            issue["column"] != "Survived" or issue["category"] == "class_imbalance" for issue in summary["issues"]
        )

    def test_titanic_profile_does_not_fail_on_expected_signal(self):
        df = pd.read_csv(TITANIC)
        summary = DatasetAnalyzer(df, target_col="Survived", preset="profile").analyze()

        normality = [issue for issue in summary["issues"] if issue["category"] == "normality"]
        assert normality
        assert all(issue["severity"] == "warning" for issue in normality)
        assert all(issue["column"] not in {"Survived", "Pclass", "SibSp", "Parch"} for issue in normality)
        assert not any(
            issue["category"] in {"feature_correlation", "categorical_correlation", "mixed_correlation"}
            and "Sex" in issue["description"]
            and "Survived" in issue["description"]
            for issue in summary["issues"]
        )
        assert not any(
            issue["category"] == "high_zero_counts" and issue["column"] == "Survived" for issue in summary["issues"]
        )
        assert not any(
            issue["category"] == "constant_length" and issue["column"] == "Embarked" for issue in summary["issues"]
        )

    def test_clean_frame_has_no_critical_issues(self):
        rng = np.random.default_rng(0)
        frame = pd.DataFrame(
            {
                "y": np.array([0, 1] * 250),
                "x1": rng.normal(size=500),
                "x2": rng.normal(size=500),
                "group": rng.choice(["a", "b", "c", "d"], size=500),
            }
        )
        summary = DatasetAnalyzer(frame, target_col="y", preset="gate").analyze()
        assert summary["critical_count"] == 0

    def test_broken_frame_flags_each_blocker(self):
        rng = np.random.default_rng(1)
        rows = 200
        target = rng.integers(0, 2, rows)
        sparse = np.concatenate([np.full(160, np.nan), rng.normal(size=40)])
        values = np.concatenate([rng.normal(size=rows - 5), np.full(5, np.inf)])
        frame = pd.DataFrame(
            {
                "y": target,
                "leak": target,
                "inf_col": values,
                "empty": np.full(rows, np.nan),
                "sparse": sparse,
                "ok": rng.normal(size=rows),
            }
        )
        summary = DatasetAnalyzer(frame, target_col="y", preset="gate").analyze()
        found = {(issue["category"], issue["column"]) for issue in _critical(summary)}
        assert ("data_leakage", "leak") in found
        assert ("infinite_values", "inf_col") in found
        assert ("empty_column", "empty") in found
        assert ("missing_values", "sparse") in found

    def test_sampling_is_opt_in(self):
        frame = pd.DataFrame({"x": range(1_000)})
        summary = DatasetAnalyzer(frame).analyze()
        assert summary["sampling_info"]["was_sampled"] is False
        assert summary["summaries"]["dataset_info"]["rows"] == 1_000

    def test_json_payload_matches_scan_and_details(self, tmp_path):
        frame = pd.DataFrame({"y": [0, 1, 0, 1], "x": [1.0, 2.0, 3.0, 4.0]})
        path = tmp_path / "tiny.csv"
        frame.to_csv(path, index=False)
        summary = DatasetAnalyzer(frame, target_col="y", preset="gate").analyze()
        payload = _json_payload(summary)

        scan = _invoke(["scan", str(path), "--target", "y", "--json", "--preset", "gate"])
        details = _invoke(["details", str(path), "--target", "y", "--json", "--preset", "gate"])
        assert scan.exit_code == 0
        assert details.exit_code == 0
        scan_data = json.loads(scan.output)
        details_data = json.loads(details.output)
        assert scan_data["schema_version"] == payload["schema_version"] == "0.2"
        assert (
            set(scan_data)
            == set(details_data)
            == {
                "schema_version",
                "critical_count",
                "warning_count",
                "total_issues",
                "issues",
                "sampling_info",
            }
        )

    def test_fail_on_critical_exit_code(self, tmp_path):
        clean = tmp_path / "clean.csv"
        pd.DataFrame({"y": [0, 1] * 20, "x": np.linspace(0, 1, 40)}).to_csv(clean, index=False)
        ok = _invoke(["scan", str(clean), "--target", "y", "--preset", "gate", "--fail-on", "critical"])
        assert ok.exit_code == 0

        broken = tmp_path / "broken.csv"
        pd.DataFrame({"y": [0, 1] * 20, "leak": [0, 1] * 20, "x": np.linspace(0, 1, 40)}).to_csv(broken, index=False)
        failed = _invoke(["scan", str(broken), "--target", "y", "--preset", "gate", "--fail-on", "critical"])
        assert failed.exit_code == 2

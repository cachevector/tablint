import json
import os
import sys
from contextlib import contextmanager

import click
import fuzzybunny
import numpy as np
import pandas as pd

import hashprep
from hashprep import DatasetAnalyzer
from hashprep.checks.core import Issue
from hashprep.preparers.codegen import CodeGenerator
from hashprep.preparers.pipeline_builder import PipelineBuilder
from hashprep.preparers.suggestions import SuggestionProvider
from hashprep.reports import generate_report
from hashprep.utils.config_loader import load_config
from hashprep.utils.sampling import SamplingConfig


def json_numpy_handler(obj):
    """Custom JSON encoder to handle numpy types."""
    if hasattr(obj, "tolist"):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _read_table(path: str) -> pd.DataFrame:
    """Read a CSV or Parquet table. Parquet needs the parquet extra."""
    if str(path).lower().endswith(".parquet"):
        try:
            return pd.read_parquet(path)
        except ImportError as e:
            raise ImportError("Reading Parquet requires the parquet extra: pip install 'hashprep[parquet]'") from e
    return pd.read_csv(path)


def _parse_checks(checks: str | None) -> list[str] | None:
    if not checks:
        return None
    selected = [item.strip() for item in checks.split(",") if item.strip()]
    valid_checks = DatasetAnalyzer.ALL_CHECKS
    invalid_checks = [item for item in selected if item not in valid_checks]
    if invalid_checks:
        click.echo(f"Warning: Invalid checks ignored: {', '.join(invalid_checks)}")
        for invalid in invalid_checks:
            suggestions = suggest_check_names(invalid, valid_checks)
            if suggestions:
                click.echo(f"  Did you mean: {', '.join(suggestions)}?")
    return [item for item in selected if item in valid_checks]


def _run_analysis(
    file_path,
    target,
    checks,
    comparison,
    sample_size,
    no_sample,
    config_path,
    preset,
    include_plots=False,
):
    df = _read_table(file_path)
    comparison_df = _read_table(comparison) if comparison else None
    auto_sample = sample_size is not None and not no_sample
    sampling_config = SamplingConfig(max_rows=sample_size) if auto_sample else None
    config = load_config(config_path) if config_path else None
    analyzer = DatasetAnalyzer(
        df,
        target_col=target,
        selected_checks=_parse_checks(checks),
        include_plots=include_plots,
        comparison_df=comparison_df,
        sampling_config=sampling_config,
        auto_sample=auto_sample,
        config=config,
        preset=preset,
    )
    return analyzer.analyze()


def _json_payload(summary: dict) -> dict:
    return {
        "schema_version": summary["schema_version"],
        "critical_count": summary["critical_count"],
        "warning_count": summary["warning_count"],
        "total_issues": summary["total_issues"],
        "issues": summary["issues"],
        "sampling_info": summary.get("sampling_info"),
    }


def _exit_if_failed(summary: dict, fail_on: str | None) -> None:
    if fail_on == "critical" and summary["critical_count"] > 0:
        sys.exit(2)
    if fail_on == "warning" and (summary["critical_count"] > 0 or summary["warning_count"] > 0):
        sys.exit(2)


def suggest_check_names(invalid_check, valid_checks, cutoff=0.4):
    """Suggest similar check names for an invalid check using fuzzybunny."""
    # Use fuzzybunny to find the top 3 most similar check names
    results = fuzzybunny.rank(invalid_check, valid_checks, scorer="levenshtein", threshold=cutoff, top_n=3)
    # Extract just the matched strings from the results
    suggestions = [match[0] for match in results]
    return suggestions


@contextmanager
def error_handler():
    try:
        yield
    except FileNotFoundError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)
    except pd.errors.EmptyDataError:
        click.secho("Error: The CSV file is empty or has no columns to parse.", fg="red", err=True)
        sys.exit(1)
    except pd.errors.ParserError as e:
        click.secho(f"Error: Failed to parse CSV: {e}", fg="red", err=True)
        sys.exit(1)
    except ValueError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)
    except TypeError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)
    except ImportError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)
    except ZeroDivisionError:
        click.secho(
            "Error: Division by zero occurred during analysis. This often happens with empty or single-row datasets.",
            fg="red",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red", err=True)
        if os.environ.get("HASHPREP_DEBUG"):
            raise
        sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo(f"HashPrep Version: {hashprep.__version__}")


@cli.command()
def checks():
    """List all available data quality checks."""
    click.echo("Available Checks:")
    for check in sorted(DatasetAnalyzer.ALL_CHECKS):
        click.echo(f"- {check}")
    click.echo("\nUse these with the --checks option in 'scan', 'details', or 'report'.")


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--critical-only", is_flag=True, help="Show only critical issues")
@click.option("--quiet", is_flag=True, help="Show minimal output")
@click.option("--json", "json_out", is_flag=True, help="Output in JSON format")
@click.option("--target", default=None, help="Target column for relevant checks")
@click.option(
    "--checks",
    default=None,
    help="Comma-separated checks to run. Defaults to the gate preset.",
)
@click.option("--preset", type=click.Choice(["gate", "profile"]), default="gate", show_default=True)
@click.option(
    "--fail-on", type=click.Choice(["critical", "warning"]), default=None, help="Exit 2 when this severity is present"
)
@click.option(
    "--comparison",
    type=click.Path(exists=True),
    default=None,
    help="Comparison dataset for drift detection",
)
@click.option(
    "--sample-size",
    type=int,
    default=None,
    help="Analyze at most N rows. Sampling stays off unless this is set.",
)
@click.option("--no-sample", is_flag=True, help="Disable sampling even when --sample-size is set")
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to config file (.yaml, .toml, .json)",
)
def scan(
    file_path,
    critical_only,
    quiet,
    json_out,
    target,
    checks,
    preset,
    fail_on,
    comparison,
    sample_size,
    no_sample,
    config_path,
):
    with error_handler():
        summary = _run_analysis(file_path, target, checks, comparison, sample_size, no_sample, config_path, preset)

        issues = summary["issues"]
        critical = [i for i in issues if i["severity"] == "critical"]
        warnings = [i for i in issues if i["severity"] == "warning"]

        if json_out:
            click.echo(json.dumps(_json_payload(summary), default=json_numpy_handler))
            _exit_if_failed(summary, fail_on)
            return

        if quiet:
            click.echo(f"CRITICAL ISSUES: {len(critical)}, WARNINGS: {len(warnings)}")
            _exit_if_failed(summary, fail_on)
            return

        click.echo(f"Dataset Health Check: {file_path}")
        click.echo(
            f"Size: {summary['summaries']['dataset_info']['rows']} rows x {summary['summaries']['dataset_info']['columns']} columns"
        )

        if "sampling_info" in summary and summary["sampling_info"].get("was_sampled"):
            info = summary["sampling_info"]
            click.echo(f"Sampled: {info['sample_fraction'] * 100:.1f}% of {info['original_rows']} rows")

        if critical_only:
            click.echo("Critical Issues:")
            for i, issue in enumerate(critical, 1):
                click.echo(f"{i}. {issue['description']}")
            _exit_if_failed(summary, fail_on)
            return

        click.echo("Critical Issues:")
        for issue in critical:
            click.echo(f"- {issue['description']}")
        click.echo("Warnings:")
        for issue in warnings:
            click.echo(f"- {issue['description']}")
        click.echo("Next steps: Run 'hashprep details' or 'hashprep report' for more info.")
        _exit_if_failed(summary, fail_on)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--json", "json_out", is_flag=True, help="Output the stable JSON issue list")
@click.option("--target", default=None, help="Target column for relevant checks")
@click.option(
    "--checks",
    default=None,
    help="Comma-separated checks to run. Defaults to the gate preset.",
)
@click.option("--preset", type=click.Choice(["gate", "profile"]), default="gate", show_default=True)
@click.option(
    "--fail-on", type=click.Choice(["critical", "warning"]), default=None, help="Exit 2 when this severity is present"
)
@click.option(
    "--comparison",
    type=click.Path(exists=True),
    default=None,
    help="Comparison dataset for drift detection",
)
@click.option(
    "--sample-size",
    type=int,
    default=None,
    help="Analyze at most N rows. Sampling stays off unless this is set.",
)
@click.option("--no-sample", is_flag=True, help="Disable sampling even when --sample-size is set")
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to config file (.yaml, .toml, .json)",
)
def details(file_path, json_out, target, checks, preset, fail_on, comparison, sample_size, no_sample, config_path):
    with error_handler():
        summary = _run_analysis(file_path, target, checks, comparison, sample_size, no_sample, config_path, preset)

        if json_out:
            click.echo(json.dumps(_json_payload(summary), default=json_numpy_handler))
            _exit_if_failed(summary, fail_on)
            return

        issues = summary["issues"]
        critical = [i for i in issues if i["severity"] == "critical"]
        warnings = [i for i in issues if i["severity"] == "warning"]

        click.echo(f"Detailed Analysis: {file_path}")

        if "sampling_info" in summary and summary["sampling_info"].get("was_sampled"):
            info = summary["sampling_info"]
            click.echo(
                f"Note: Analysis performed on {info['sample_fraction'] * 100:.1f}% sample ({int(info['original_rows'] * info['sample_fraction'])} of {info['original_rows']} rows)"
            )

        click.echo("\nCritical Issues:")
        for i, issue in enumerate(critical, 1):
            click.echo(f"{i}. {issue['category'].upper()} - '{issue['column']}'")
            click.echo(f"   Description: {issue['description']}")
            click.echo(f"   Impact: {issue['impact_score'].capitalize()}")
            click.echo(f"   Quick fix: {issue['quick_fix']}")

        click.echo("\nWarnings:")
        for i, issue in enumerate(warnings, 1):
            click.echo(f"{i}. {issue['category'].upper()}")
            click.echo(f"   Description: {issue['description']}")
            click.echo(f"   Impact: {issue['impact_score'].capitalize()}")
            click.echo(f"   Quick fix: {issue['quick_fix']}")

        click.echo("\nDataset Summary:")
        info = summary["summaries"]["dataset_info"]
        click.echo(f"- Rows: {info['rows']}")
        click.echo(f"- Columns: {info['columns']}")
        click.echo(f"- Memory: ~{info['memory_mb']} MB")
        click.echo(f"- Missing: {info['missing_cells']} ({info['missing_percentage']} %)")
        click.echo("- Variable Types:")
        for col, typ in summary["summaries"]["variable_types"].items():
            click.echo(f"  {col}: {typ}")
        click.echo("- Missing Values (by column):")
        for col, pct in sorted(
            summary["summaries"]["missing_values"]["percentage"].items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            if pct > 0:
                click.echo(f"  {col}: {pct}%")
        repro = summary["summaries"]["reproduction_info"]
        click.echo(f"- Dataset Hash: {repro['dataset_hash']}")
        if "analysis_started" in repro and repro["analysis_started"]:
            click.echo(f"- Analysis Started: {repro['analysis_started'][:19]}")
        if "duration_seconds" in repro:
            click.echo(f"- Duration: {repro['duration_seconds']} seconds")
        _exit_if_failed(summary, fail_on)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path for the report")
@click.option("--with-code", is_flag=True, help="Generate fixes.py and pipeline.py scripts")
@click.option("--full/--no-full", default=True, help="Include full summaries in report (default: True)")
@click.option("--format", default="md", help="Report format: md, json, html, pdf")
@click.option("--theme", default="minimal", help="HTML report theme: minimal, neubrutalism")
@click.option("--target", default=None, help="Target column for relevant checks")
@click.option(
    "--checks",
    default=None,
    help="Comma-separated checks to run. Defaults to the profile preset.",
)
@click.option("--preset", type=click.Choice(["gate", "profile"]), default="profile", show_default=True)
@click.option(
    "--visualizations/--no-visualizations",
    default=True,
    help="Include plots in report (default: True)",
)
@click.option(
    "--comparison",
    type=click.Path(exists=True),
    default=None,
    help="Comparison dataset for drift detection",
)
@click.option(
    "--sample-size",
    type=int,
    default=None,
    help="Analyze at most N rows. Sampling stays off unless this is set.",
)
@click.option("--no-sample", is_flag=True, help="Disable sampling even when --sample-size is set")
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to config file (.yaml, .toml, .json)",
)
def report(
    file_path,
    output,
    with_code,
    full,
    format,
    theme,
    target,
    checks,
    preset,
    visualizations,
    comparison,
    sample_size,
    no_sample,
    config_path,
):
    with error_handler():
        summary = _run_analysis(
            file_path,
            target,
            checks,
            comparison,
            sample_size,
            no_sample,
            config_path,
            preset,
            include_plots=visualizations,
        )

        base_name = os.path.splitext(os.path.basename(file_path))[0] + "_hashprep_report"
        if output:
            report_file = output
        else:
            report_file = f"{base_name}.{format}"

        generate_report(
            summary,
            format=format,
            full=full,
            output_file=report_file,
            theme=theme,
        )
        click.echo(f"Report saved to: {report_file}")
        click.echo(f"Summary: {summary['critical_count']} critical, {summary['warning_count']} warnings")

        if "sampling_info" in summary and summary["sampling_info"].get("was_sampled"):
            info = summary["sampling_info"]
            click.echo(f"Note: Analysis performed on {info['sample_fraction'] * 100:.1f}% sample")

        if with_code:
            issues = [Issue(**i) for i in summary["issues"]]
            column_types = summary.get("column_types", {})

            provider = SuggestionProvider(
                issues=issues,
                column_types=column_types,
                target_col=target,
            )
            suggestions = provider.get_suggestions()

            codegen = CodeGenerator(suggestions)
            fixes_file = f"{base_name}_fixes.py"
            fixes_code = codegen.generate_pandas_script()
            with open(fixes_file, "w") as f:
                f.write(fixes_code)
            click.echo(f"Pandas fixes script saved to: {fixes_file}")

            builder = PipelineBuilder(suggestions)
            pipeline_file = f"{base_name}_pipeline.py"
            pipeline_code = builder.generate_pipeline_code()
            with open(pipeline_file, "w") as f:
                f.write(pipeline_code)
            click.echo(f"sklearn pipeline script saved to: {pipeline_file}")


if __name__ == "__main__":
    cli()

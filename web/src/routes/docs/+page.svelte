<script lang="ts">
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';

  let content: HTMLElement;
  let activeId = $state('overview');

  onMount(() => {
    const sections = Array.from(content.querySelectorAll<HTMLElement>(':scope > section[id]'));
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible.length) activeId = visible[0].target.id;
      },
      { rootMargin: '-80px 0px -65% 0px' }
    );
    sections.forEach((section) => observer.observe(section));

    // Copy buttons on every code block.
    const buttons: HTMLButtonElement[] = [];
    content.querySelectorAll('pre').forEach((pre) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-btn';
      button.textContent = 'Copy';
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(pre.querySelector('code')?.innerText ?? '');
          button.textContent = 'Copied';
          setTimeout(() => (button.textContent = 'Copy'), 1500);
        } catch {}
      });
      pre.appendChild(button);
      buttons.push(button);
    });

    return () => {
      observer.disconnect();
      buttons.forEach((b) => b.remove());
    };
  });
</script>

<Navbar />

<main class="docs">
  <section class="docs-hero">
    <div class="container">
      <p class="cv-eyebrow docs-kicker"><span class="square"></span>Documentation <span class="cv-chip">v0.1.0b1</span></p>
      <h1>Learn Tablint in minutes, not hours.</h1>
      <p class="docs-lede">
        A focused guide to installing, running, and integrating Tablint into your ML workflows.
      </p>
    </div>
  </section>

  <section class="docs-body">
    <div class="container docs-layout">
      <aside class="docs-nav" aria-label="Documentation sections">
        <div class="docs-nav-group">
          <div class="docs-nav-label">Getting started</div>
          <a href="#overview" class:active={activeId === 'overview'}>Overview</a>
          <a href="#installation" class:active={activeId === 'installation'}>Installation</a>
          <a href="#quickstart-cli" class:active={activeId === 'quickstart-cli'}>Quickstart (CLI)</a>
          <a href="#quickstart-python" class:active={activeId === 'quickstart-python'}>Quickstart (Python)</a>
        </div>
        <div class="docs-nav-group">
          <div class="docs-nav-label">Deep dive</div>
          <a href="#reports" class:active={activeId === 'reports'}>Reports</a>
          <a href="#cli-reference" class:active={activeId === 'cli-reference'}>CLI reference</a>
          <a href="#python-api" class:active={activeId === 'python-api'}>Python API</a>
          <a href="#checks" class:active={activeId === 'checks'}>Available checks</a>
          <a href="#configuration" class:active={activeId === 'configuration'}>Configuration</a>
          <a href="#contributing" class:active={activeId === 'contributing'}>Contributing</a>
        </div>
      </aside>

      <article class="docs-content" bind:this={content}>
        <section id="overview">
          <h2>Overview</h2>
          <p>
            Tablint is a dataset profiler and debugger for machine learning. Think of it as
            <strong>&ldquo;Pandas Profiling + a linter for datasets&rdquo;</strong> that runs before you train.
          </p>
          <p>
            It scans your data, surfaces critical issues, explains why they matter for modeling, and suggests (or
            generates) concrete fixes. You can use it as a single CLI command or as a Python library inside your
            pipelines.
          </p>
        </section>

        <section id="installation">
          <h2>Installation</h2>
          <div class="docs-card">
            <h3>Using pip</h3>
            <pre data-lang="bash"><code><span class="hl-command">pip</span> <span class="hl-arg">install</span> <span class="hl-value">tablint</span></code></pre>
          </div>

          <div class="docs-card">
            <h3>Using uv (recommended)</h3>
            <pre data-lang="bash"><code><span class="hl-comment"># Install uv (if needed)</span>
<span class="hl-command">curl</span> <span class="hl-flag">-LsSf</span> <span class="hl-value">https://astral.sh/uv/install.sh</span> <span class="hl-operator">|</span> <span class="hl-command">sh</span>

<span class="hl-comment"># Install Tablint</span>
<span class="hl-command">uv</span> <span class="hl-command">pip</span> <span class="hl-arg">install</span> <span class="hl-value">tablint</span>

<span class="hl-comment"># Or from source</span>
<span class="hl-command">git</span> <span class="hl-arg">clone</span> <span class="hl-value">https://github.com/cachevector/tablint.git</span>
<span class="hl-command">cd</span> <span class="hl-value">tablint</span>
<span class="hl-command">uv</span> <span class="hl-arg">sync</span></code></pre>
          </div>

          <p class="docs-note">
            After installation, the <code>tablint</code> command is available directly in your terminal.
          </p>
        </section>

        <section id="quickstart-cli">
          <h2>Quickstart &mdash; CLI</h2>
          <div class="docs-card">
            <h3>1. Run a quick scan</h3>
            <p>Get a concise summary of dataset issues in your terminal.</p>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">scan</span> <span class="hl-value">dataset.csv</span></code></pre>
          </div>

          <div class="docs-grid-2">
            <div class="docs-card">
              <h3>Common options</h3>
              <ul>
                <li><code>--target COLUMN</code> &mdash; target column for ML-specific checks</li>
                <li><code>--checks outliers,high_missing_values</code> &mdash; run only selected checks</li>
                <li><code>--json</code> &mdash; JSON output for automation</li>
                <li><code>--sample-size N</code> &mdash; restrict analysis to N rows</li>
              </ul>
            </div>
            <div class="docs-card">
              <h3>Example</h3>
              <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">scan</span> <span class="hl-value">train.csv</span> <span class="hl-operator">\</span>
  <span class="hl-flag">--target</span> <span class="hl-value">Survived</span> <span class="hl-operator">\</span>
  <span class="hl-flag">--checks</span> <span class="hl-value">outliers,high_missing_values,class_imbalance</span></code></pre>
            </div>
          </div>

          <div class="docs-card">
            <h3>2. Detailed analysis</h3>
            <p>Drill into every issue Tablint found.</p>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">details</span> <span class="hl-value">train.csv</span> <span class="hl-flag">--target</span> <span class="hl-value">Survived</span></code></pre>
          </div>
        </section>

        <section id="quickstart-python">
          <h2>Quickstart &mdash; Python</h2>

          <div class="docs-card">
            <h3>Basic analysis</h3>
            <pre data-lang="python"><code><span class="hl-keyword">import</span> pandas <span class="hl-keyword">as</span> pd
<span class="hl-keyword">from</span> tablint <span class="hl-keyword">import</span> DatasetAnalyzer

df = pd.read_csv(<span class="hl-string">"dataset.csv"</span>)

analyzer = DatasetAnalyzer(df)
summary = analyzer.analyze()

print(<span class="hl-string">"Critical issues:"</span>, summary[<span class="hl-string">"critical_count"</span>])
print(<span class="hl-string">"Warnings:"</span>, summary[<span class="hl-string">"warning_count"</span>])</code></pre>
          </div>

          <div class="docs-grid-2">
            <div class="docs-card">
              <h3>With a target column</h3>
              <pre data-lang="python"><code>analyzer = DatasetAnalyzer(
    df,
    target_col=<span class="hl-string">"target"</span>,
)
summary = analyzer.analyze()</code></pre>
            </div>

            <div class="docs-card">
              <h3>Run specific checks</h3>
              <pre data-lang="python"><code>analyzer = DatasetAnalyzer(
    df,
    selected_checks=[<span class="hl-string">"outliers"</span>, <span class="hl-string">"high_missing_values"</span>, <span class="hl-string">"class_imbalance"</span>],
)
summary = analyzer.analyze()</code></pre>
            </div>
          </div>
        </section>

        <section id="reports">
          <h2>Reports</h2>

          <div class="docs-card">
            <h3>Generate a report from the CLI</h3>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">report</span> <span class="hl-value">dataset.csv</span> <span class="hl-flag">--format</span> <span class="hl-value">html</span> <span class="hl-flag">--theme</span> <span class="hl-value">minimal</span></code></pre>
            <p>
              Reports can be exported as <code>md</code>, <code>json</code>, <code>html</code>, or
              <code>pdf</code>, using the <code>--format</code> flag. Use <code>--with-code</code> to generate
              companion Python scripts with cleaning logic and pipelines.
            </p>
          </div>

          <div class="docs-card">
            <h3>Generate reports from Python</h3>
            <pre data-lang="python"><code><span class="hl-keyword">from</span> tablint <span class="hl-keyword">import</span> DatasetAnalyzer
<span class="hl-keyword">from</span> tablint.reports <span class="hl-keyword">import</span> generate_report

analyzer = DatasetAnalyzer(df, include_plots=<span class="hl-builtin">True</span>)
summary = analyzer.analyze()

generate_report(
    summary,
    format=<span class="hl-string">"html"</span>,
    full=<span class="hl-builtin">True</span>,
    output_file=<span class="hl-string">"dataset_tablint_report.html"</span>,
    theme=<span class="hl-string">"minimal"</span>,
)</code></pre>
          </div>
        </section>

        <section id="cli-reference">
          <h2>CLI reference</h2>

          <div class="docs-card">
            <h3><code>tablint scan</code></h3>
            <p>
              Run a quick scan and print a compact summary of issues to the terminal. Ideal for a fast health check
              during development.
            </p>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">scan</span> <span class="hl-value">dataset.csv</span> <span class="hl-flag">--target</span> <span class="hl-value">Survived</span></code></pre>
            <ul>
              <li><code>--target COLUMN</code> &mdash; target column for ML checks (class imbalance, leakage, etc.)</li>
              <li><code>--checks LIST</code> &mdash; comma-separated list of checks to run</li>
              <li><code>--comparison FILE</code> &mdash; compare with another dataset for drift detection</li>
              <li><code>--critical-only</code> &mdash; hide warnings and show only critical issues</li>
              <li><code>--json</code> &mdash; emit JSON instead of human-readable text</li>
              <li><code>--quiet</code> &mdash; minimal output, useful in CI</li>
              <li><code>--sample-size N</code> / <code>--no-sample</code> &mdash; control automatic sampling</li>
              <li><code>--config FILE</code> &mdash; load thresholds from a YAML, TOML, or JSON file</li>
            </ul>
          </div>

          <div class="docs-card">
            <h3><code>tablint details</code></h3>
            <p>
              Produce a verbose, line-by-line description of each issue in the dataset, with statistics and
              recommendations.
            </p>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">details</span> <span class="hl-value">dataset.csv</span> <span class="hl-flag">--target</span> <span class="hl-value">Survived</span></code></pre>
            <p>
              Accepts the same options as <code>scan</code> (including <code>--comparison</code> and <code>--config</code>) and is best used when you are actively debugging a dataset
              or deciding which columns to drop or transform.
            </p>
          </div>

          <div class="docs-card">
            <h3><code>tablint report</code></h3>
            <p>
              Generate a full report in HTML, PDF, Markdown, or JSON. Reports contain summaries, plots, and (optionally)
              auto-generated Python code.
            </p>
            <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">report</span> <span class="hl-value">dataset.csv</span> <span class="hl-flag">--format</span> <span class="hl-value">html</span> <span class="hl-flag">--theme</span> <span class="hl-value">minimal</span> <span class="hl-flag">--with-code</span></code></pre>
            <ul>
              <li><code>--format &#123;md,json,html,pdf&#125;</code> &mdash; output format (Markdown is the default)</li>
              <li><code>--theme &#123;minimal,neubrutalism&#125;</code> &mdash; HTML theme</li>
              <li><code>--with-code</code> &mdash; write companion <code>_fixes.py</code> and <code>_pipeline.py</code> files</li>
              <li><code>--comparison FILE</code> &mdash; compare two datasets for drift (train vs test, etc.)</li>
              <li><code>--sample-size N</code> / <code>--no-sample</code> &mdash; control automatic sampling</li>
              <li><code>--config FILE</code> &mdash; load thresholds from a YAML, TOML, or JSON file</li>
            </ul>
          </div>

          <div class="docs-card">
            <h3>Exit codes</h3>
            <p>
              Tablint is CI-friendly: non-zero exit codes indicate that critical issues were detected or an internal
              error occurred. You can wire this into pre-commit hooks or data-quality checks in your pipeline.
            </p>
          </div>
        </section>

        <section id="python-api">
          <h2>Python API</h2>

          <div class="docs-card">
            <h3><code>DatasetAnalyzer</code></h3>
            <p>
              The core entry point for programmatic usage. It accepts a pandas <code>DataFrame</code> and optional
              configuration for targets, sampling, comparison datasets, and which checks to run.
            </p>
            <pre data-lang="python"><code><span class="hl-keyword">from</span> tablint <span class="hl-keyword">import</span> DatasetAnalyzer

analyzer = DatasetAnalyzer(
    df,
    target_col=<span class="hl-string">"target"</span>,
    selected_checks=[<span class="hl-string">"outliers"</span>, <span class="hl-string">"high_missing_values"</span>],
    include_plots=<span class="hl-builtin">True</span>,
)
summary = analyzer.analyze()</code></pre>
            <p>The returned <code>summary</code> is a JSON-serializable dictionary with keys such as:</p>
            <ul>
              <li><code>critical_count</code> / <code>warning_count</code></li>
              <li><code>issues</code> &mdash; list of individual issues with severity, column, check name, and message</li>
              <li><code>summaries</code> &mdash; per-column statistics and optional plots</li>
              <li><code>sampling_info</code> &mdash; information about any sampling that was applied</li>
            </ul>
          </div>

          <div class="docs-card">
            <h3>Sampling large datasets</h3>
            <p>
              For very large tables, you can control how many rows Tablint inspects using a sampling configuration.
              This keeps runtimes predictable in production.
            </p>
            <pre data-lang="python"><code><span class="hl-keyword">from</span> tablint.utils.sampling <span class="hl-keyword">import</span> SamplingConfig

sampling = SamplingConfig(max_rows=<span class="hl-value">10000</span>)

analyzer = DatasetAnalyzer(
    df,
    sampling_config=sampling,
    auto_sample=<span class="hl-builtin">True</span>,
)
summary = analyzer.analyze()</code></pre>
            <p>
              When sampling is applied, <code>summary["sampling_info"]</code> contains details such as fractions and
              original row counts.
            </p>
          </div>

          <div class="docs-card">
            <h3>Generating fix scripts and pipelines</h3>
            <p>
              Beyond reports, Tablint can emit executable Python code that encodes suggested fixes and ML pipelines.
            </p>
            <pre data-lang="python"><code><span class="hl-keyword">from</span> tablint.checks.core <span class="hl-keyword">import</span> Issue
<span class="hl-keyword">from</span> tablint.preparers.codegen <span class="hl-keyword">import</span> CodeGenerator
<span class="hl-keyword">from</span> tablint.preparers.pipeline_builder <span class="hl-keyword">import</span> PipelineBuilder
<span class="hl-keyword">from</span> tablint.preparers.suggestions <span class="hl-keyword">import</span> SuggestionProvider

issues = [Issue(<span class="hl-arg">**i</span>) <span class="hl-keyword">for</span> i <span class="hl-keyword">in</span> summary[<span class="hl-string">"issues"</span>]]
column_types = summary.get(<span class="hl-string">"column_types"</span>, <span class="hl-builtin">dict</span>())

provider = SuggestionProvider(
    issues=issues,
    column_types=column_types,
    target_col=<span class="hl-string">"target"</span>,
)
suggestions = provider.get_suggestions()

codegen = CodeGenerator(suggestions)
fixes_code = codegen.generate_pandas_script()

builder = PipelineBuilder(suggestions)
pipeline_code = builder.generate_pipeline_code()</code></pre>
            <p>
              You can write these strings to disk (for example, <code>fixes.py</code> and <code>pipeline.py</code>) or
              load them dynamically in your tooling.
            </p>
          </div>

          <div class="docs-card">
            <h3>Drift detection</h3>
            <p>
              To compare training and serving data, construct a <code>DatasetAnalyzer</code> with both a primary and
              comparison dataset and enable the <code>dataset_drift</code> check.
            </p>
            <pre data-lang="python"><code>analyzer = DatasetAnalyzer(
    train_df,
    comparison_df=test_df,
    selected_checks=[<span class="hl-string">"dataset_drift"</span>],
)
summary = analyzer.analyze()</code></pre>
          </div>

        </section>

        <section id="checks">
          <h2>Available checks</h2>

          <div class="docs-card docs-checks">
            <div>
              <h3>Data quality</h3>
              <ul>
                <li><code>dataset_missingness</code> &mdash; overall missing data patterns</li>
                <li><code>high_missing_values</code> &mdash; columns with heavy missingness</li>
                <li><code>missing_patterns</code> &mdash; correlated missing value patterns</li>
                <li><code>duplicates</code> &mdash; duplicate rows</li>
                <li><code>empty_columns</code> &mdash; completely empty columns</li>
                <li><code>empty_dataset</code> &mdash; empty or all-missing datasets</li>
                <li><code>single_value_columns</code> &mdash; near-constant features</li>
                <li><code>mixed_data_types</code> &mdash; columns with mixed data types</li>
              </ul>
            </div>
            <div>
              <h3>Distribution &amp; statistics</h3>
              <ul>
                <li><code>outliers</code> &mdash; z-score outlier detection</li>
                <li><code>skewness</code> &mdash; highly skewed numeric distributions</li>
                <li><code>high_cardinality</code> &mdash; too many unique categorical values</li>
                <li><code>uniform_distribution</code> &mdash; uniformly distributed numeric columns</li>
                <li><code>unique_values</code> &mdash; columns where &gt;95% values are unique</li>
                <li><code>high_zero_counts</code> &mdash; features dominated by zeros</li>
                <li><code>infinite_values</code> &mdash; columns containing infinite values</li>
                <li><code>constant_length</code> &mdash; string columns with constant character length</li>
                <li><code>extreme_text_lengths</code> &mdash; text columns with extreme value lengths</li>
                <li><code>normality</code> &mdash; non-normal distributions (Shapiro-Wilk / D&rsquo;Agostino-Pearson)</li>
                <li><code>variance_homogeneity</code> &mdash; unequal variances across target groups (Levene&rsquo;s test)</li>
              </ul>
            </div>
            <div>
              <h3>ML-specific</h3>
              <ul>
                <li><code>class_imbalance</code> &mdash; target imbalance (requires <code>--target</code>)</li>
                <li><code>feature_correlation</code> &mdash; highly correlated numeric features</li>
                <li><code>categorical_correlation</code> &mdash; highly associated categorical features</li>
                <li><code>mixed_correlation</code> &mdash; numeric-categorical associations</li>
                <li><code>data_leakage</code> &mdash; columns identical to target</li>
                <li><code>target_leakage_patterns</code> &mdash; features leaking target information</li>
                <li><code>low_mutual_information</code> &mdash; near-zero MI with target (requires <code>--target</code>)</li>
                <li><code>dataset_drift</code> &mdash; drift between train / test datasets (requires <code>--comparison</code>)</li>
                <li><code>datetime_skew</code> &mdash; datetime columns concentrated in one period</li>
                <li><code>datetime_future_dates</code> &mdash; datetime values in the future</li>
                <li><code>datetime_gaps</code> &mdash; anomalous gaps in datetime sequences</li>
                <li><code>datetime_monotonicity</code> &mdash; non-monotonic datetime columns</li>
              </ul>
            </div>
          </div>
        </section>

        <section id="configuration">
          <h2>Configuration</h2>
          <p>
            Every detection threshold in Tablint has a sensible default. You can override any of them at runtime by
            providing a config file &mdash; no code changes required.
          </p>

          <div class="docs-card">
            <h3>Supported formats</h3>
            <p>Config files can be written in YAML (<code>.yaml</code> / <code>.yml</code>), TOML (<code>.toml</code>),
            or JSON (<code>.json</code>). Only the keys you specify are changed; everything else falls back to
            defaults.</p>
            <pre data-lang="yaml"><code><span class="hl-comment"># tablint.yaml</span>
missing_values:
  warning: 0.3
  critical: 0.6
outliers:
  z_score: 3.5
statistical_tests:
  normality_p_value: 0.01
mutual_info:
  low_mi_warning: 0.05</code></pre>
          </div>

          <div class="docs-grid-2">
            <div class="docs-card">
              <h3>Via CLI</h3>
              <pre data-lang="bash"><code><span class="hl-command">tablint</span> <span class="hl-arg">scan</span> <span class="hl-value">dataset.csv</span> <span class="hl-operator">\</span>
  <span class="hl-flag">--config</span> <span class="hl-value">tablint.yaml</span>

<span class="hl-command">tablint</span> <span class="hl-arg">report</span> <span class="hl-value">dataset.csv</span> <span class="hl-operator">\</span>
  <span class="hl-flag">--format</span> <span class="hl-value">html</span> <span class="hl-operator">\</span>
  <span class="hl-flag">--config</span> <span class="hl-value">tablint.toml</span></code></pre>
            </div>
            <div class="docs-card">
              <h3>Via Python</h3>
              <pre data-lang="python"><code><span class="hl-keyword">from</span> tablint.utils.config_loader <span class="hl-keyword">import</span> load_config
<span class="hl-keyword">from</span> tablint <span class="hl-keyword">import</span> DatasetAnalyzer

config = load_config(<span class="hl-string">"tablint.yaml"</span>)
analyzer = DatasetAnalyzer(df, config=config)
summary = analyzer.analyze()</code></pre>
            </div>
          </div>
        </section>

        <section id="contributing">
          <h2>Contributing</h2>
          <p>
            Tablint is open source and welcomes contributions. If you want to fix a bug, add a check, or improve the
            reports:
          </p>
          <ul>
            <li>Read the <a href="https://github.com/cachevector/tablint/blob/main/CONTRIBUTING.md">contribution guide</a></li>
            <li>Open an issue describing the change you&rsquo;d like to make</li>
            <li>Create a pull request with clear motivation and tests where appropriate</li>
          </ul>
        </section>
      </article>
    </div>
  </section>
</main>

<Footer />

<style>
  .docs {
    padding-top: var(--nav-height);
    overflow-x: clip;
    max-width: 100vw;
  }

  .docs-hero {
    padding: 64px 0 48px;
    border-bottom: 1px solid var(--border-secondary);
  }

  .docs-hero h1 {
    max-width: 18ch;
    margin-bottom: 16px;
  }

  .docs-lede {
    max-width: 560px;
    font-size: 1.0625rem;
  }

  .docs-kicker {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }

  .square {
    width: 8px;
    height: 8px;
    background: var(--accent);
  }

  .docs-kicker .cv-chip {
    text-transform: none;
  }

  .docs-body {
    padding: 48px 0 96px;
  }

  .docs-layout {
    display: grid;
    grid-template-columns: minmax(0, 220px) minmax(0, 1fr);
    gap: 64px;
    align-items: flex-start;
    width: 100%;
    box-sizing: border-box;
  }

  .docs-nav {
    position: sticky;
    top: calc(var(--nav-height) + 32px);
    align-self: flex-start;
    display: flex;
    flex-direction: column;
    gap: 28px;
    font-size: 0.875rem;
  }

  .docs-nav-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .docs-nav-group {
    border-left: 1px solid var(--border-secondary);
  }

  .docs-nav-label {
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-tertiary);
    padding-left: 14px;
    margin-bottom: 6px;
  }

  .docs-nav a {
    padding: 4px 0 4px 14px;
    margin-left: -1px;
    border-left: 1.5px solid transparent;
    color: var(--text-secondary);
    transition: color var(--transition-fast), border-color var(--transition-fast);
  }

  .docs-nav a:hover {
    color: var(--text-primary);
  }

  .docs-nav a.active {
    color: var(--text-primary);
    border-left-color: var(--accent);
  }

  .docs-content {
    display: flex;
    flex-direction: column;
    gap: 72px;
    font-size: 0.9375rem;
    max-width: 100%;
    min-width: 0;
  }

  .docs-content section + section {
    margin-top: 0;
  }

  .docs-content h2 {
    font-size: 1.5rem;
    margin-bottom: 24px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-primary);
  }

  .docs-content h3 {
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 12px;
  }

  .docs-content :global(a) {
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 3px;
    text-decoration-thickness: 1px;
  }

  .docs-content ul {
    list-style: square;
  }

  .docs-content li::marker {
    color: var(--text-tertiary);
  }

  .docs-content :not(pre) > code {
    font-size: 0.85em;
    padding: 1px 5px;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    color: var(--text-primary);
  }

  .docs-content h3 > code {
    font-size: 0.9em;
  }

  .docs-content p {
    margin-bottom: 16px;
  }

  /* Ensure paragraphs after headings have proper spacing */
  .docs-content h3 + p {
    margin-top: 0;
  }

  /* Ensure lists after paragraphs have spacing */
  .docs-content p + ul {
    margin-top: 12px;
  }

  .docs-content ul {
    margin: 0;
    padding-left: 18px;
  }

  .docs-content li + li {
    margin-top: 4px;
  }

  .docs-card {
    border: 1px solid var(--border-secondary);
    padding: 24px 28px;
    background: var(--bg-elevated);
  }

  .docs-card h3 {
    margin-top: 0;
  }

  .docs-card h3 + p {
    margin-top: 8px;
  }

  .docs-card p:first-child {
    margin-top: 0;
  }

  .docs-card ul:first-child {
    margin-top: 0;
  }

  .docs-card + .docs-card {
    margin-top: 24px;
  }

  .docs-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, minmax(280px, 1fr));
    gap: 24px;
    margin-top: 24px;
    margin-bottom: 24px;
  }

  .docs-grid-2 .docs-card {
    margin-top: 0;
    min-width: 0;
  }

  /* Code blocks in grid should wrap and be readable */
  .docs-grid-2 pre {
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: break-word;
    font-size: 0.75rem;
    line-height: 1.6;
    max-width: 100%;
  }

  .docs-grid-2 code {
    white-space: pre-wrap;
    word-break: break-word;
    display: block;
  }

  /* Ensure code blocks don't overflow */
  .docs-grid-2 .docs-card {
    overflow: hidden;
  }

  .docs-note {
    margin-top: 20px;
    padding-left: 14px;
    border-left: 2px solid var(--accent);
    font-size: 0.875rem;
    color: var(--text-tertiary);
  }

  .docs-checks {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
  }

  pre {
    margin: 0;
    margin-top: 12px;
    margin-bottom: 20px;
    padding: 30px 20px 16px;
    border: 1px solid var(--code-border);
    background: var(--bg-code);
    color: var(--code-text);
    font-size: 0.8125rem;
    line-height: 1.65;
    overflow-x: auto;
    overflow-y: hidden;
    position: relative;
    white-space: pre;
  }

  /* Allow wrapping for long commands when needed */
  pre code {
    white-space: pre;
    display: block;
  }

  /* Spacing after code blocks - works everywhere */
  pre + p,
  .docs-card pre + p {
    margin-top: 20px;
    margin-bottom: 16px;
  }

  pre + ul,
  .docs-card pre + ul {
    margin-top: 20px;
  }

  /* Ensure code blocks have bottom margin */
  .docs-card pre {
    margin-bottom: 20px;
  }

  code {
    font-family: var(--font-mono);
  }

  pre::before {
    position: absolute;
    top: 8px;
    left: 20px;
    font-family: var(--font-mono);
    font-size: 0.625rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-tertiary);
  }

  pre[data-lang="bash"]::before {
    content: 'bash';
  }

  pre[data-lang="python"]::before {
    content: 'python';
  }

  pre[data-lang="yaml"]::before {
    content: 'yaml';
  }

  pre :global(.copy-btn) {
    position: absolute;
    top: 4px;
    right: 6px;
    padding: 4px 8px;
    font-family: var(--font-mono);
    font-size: 0.625rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    opacity: 0;
    transition: opacity var(--transition-fast), color var(--transition-fast);
  }

  pre:hover :global(.copy-btn),
  pre :global(.copy-btn:focus-visible) {
    opacity: 1;
  }

  pre :global(.copy-btn:hover) {
    color: var(--text-primary);
  }

  @media (hover: none) {
    pre :global(.copy-btn) {
      opacity: 1;
    }
  }

  @media (max-width: 960px) {
    .docs-layout {
      grid-template-columns: minmax(0, 1fr);
      gap: 32px;
    }

    .docs-nav {
      position: static;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-secondary);
      flex-direction: row;
      flex-wrap: wrap;
      gap: 24px;
    }

    .docs-nav-group {
      min-width: 160px;
    }

    .docs-checks {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 640px) {
    .docs-hero {
      padding-top: 48px;
      padding-bottom: 32px;
    }

    .docs-grid-2 {
      grid-template-columns: minmax(0, 1fr);
    }

    .docs-checks {
      grid-template-columns: minmax(0, 1fr);
    }

    .docs-card {
      padding: 20px 16px;
    }

    pre {
      padding: 28px 14px 12px;
      font-size: 0.72rem;
    }

    pre::before {
      left: 14px;
    }
  }
</style>


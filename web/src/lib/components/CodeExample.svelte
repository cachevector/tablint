<script lang="ts">
  let activeTab = $state<'cli' | 'python'>('cli');
</script>

<section class="section">
  <div class="container">
    <div class="code-layout">
      <div class="code-info">
        <p class="cv-eyebrow eyebrow">03 / Usage</p>
        <h2>Use it your way</h2>
        <p class="code-subtitle">
          Quick terminal scan or deep Python integration — Tablint fits into any ML workflow.
        </p>

        <div class="check-list">
          <div class="check-item">
            <span class="tick" aria-hidden="true">+</span>
            <span>13 built-in dataset checks</span>
          </div>
          <div class="check-item">
            <span class="tick" aria-hidden="true">+</span>
            <span>HTML, PDF, Markdown, JSON reports</span>
          </div>
          <div class="check-item">
            <span class="tick" aria-hidden="true">+</span>
            <span>Auto-generated fix scripts</span>
          </div>
          <div class="check-item">
            <span class="tick" aria-hidden="true">+</span>
            <span>Drift detection between datasets</span>
          </div>
        </div>
      </div>

      <div class="code-panel">
        <div class="code-tabs">
          <button
            type="button"
            class="code-tab"
            class:active={activeTab === 'cli'}
            onclick={() => activeTab = 'cli'}
          >
            CLI
          </button>
          <button
            type="button"
            class="code-tab"
            class:active={activeTab === 'python'}
            onclick={() => activeTab = 'python'}
          >
            Python
          </button>
        </div>

        <div class="code-body">
          {#if activeTab === 'cli'}
            <pre><code><span class="c-comment"># Quick scan for critical issues</span>
<span class="c-prompt">$</span> tablint scan train.csv --target Survived

<span class="c-comment"># Detailed analysis of all issues</span>
<span class="c-prompt">$</span> tablint details train.csv --target Survived

<span class="c-comment"># Generate HTML report with fix scripts</span>
<span class="c-prompt">$</span> tablint report train.csv \
    --format html \
    --theme minimal \
    --with-code

<span class="c-comment"># Compare datasets for drift</span>
<span class="c-prompt">$</span> tablint report train.csv \
    --comparison test.csv \
    --format html</code></pre>
          {:else}
            <pre><code><span class="c-keyword">import</span> pandas <span class="c-keyword">as</span> pd
<span class="c-keyword">from</span> tablint <span class="c-keyword">import</span> DatasetAnalyzer
<span class="c-keyword">from</span> tablint.reports <span class="c-keyword">import</span> generate_report

<span class="c-comment"># Load and analyze</span>
df = pd.read_csv(<span class="c-string">"train.csv"</span>)
analyzer = DatasetAnalyzer(
    df,
    target_col=<span class="c-string">"Survived"</span>,
    include_plots=<span class="c-keyword">True</span>
)
summary = analyzer.analyze()

<span class="c-comment"># Check results</span>
<span class="c-builtin">print</span>(<span class="c-string">f"Critical: {'{'}</span>summary[<span class="c-string">'critical_count'</span>]<span class="c-string">{'}'}"</span>)

<span class="c-comment"># Generate report</span>
generate_report(
    summary,
    format=<span class="c-string">"html"</span>,
    theme=<span class="c-string">"minimal"</span>,
    output_file=<span class="c-string">"report.html"</span>
)</code></pre>
          {/if}
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .code-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 40px;
    align-items: start;
  }

  .eyebrow {
    margin-bottom: 20px;
  }

  .code-info h2 {
    margin-bottom: 12px;
  }

  .code-subtitle {
    max-width: 420px;
    margin-bottom: 28px;
  }

  .check-list {
    display: flex;
    flex-direction: column;
    border-top: 1px solid var(--border-secondary);
  }

  .check-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-secondary);
    font-size: 0.9375rem;
    color: var(--text-secondary);
  }

  .tick {
    font-family: var(--font-mono);
    color: var(--accent);
  }

  .code-panel {
    border: 1px solid var(--border-primary);
    background: var(--bg-elevated);
    min-width: 0;
  }

  .code-tabs {
    display: flex;
    border-bottom: 1px solid var(--border-secondary);
  }

  .code-tab {
    padding: 10px 18px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    border-right: 1px solid var(--border-secondary);
    margin-bottom: -1px;
    border-bottom: 1.5px solid transparent;
    transition: color var(--transition-fast);
  }

  .code-tab:hover {
    color: var(--text-primary);
  }

  .code-tab.active {
    color: var(--text-primary);
    border-bottom-color: var(--accent);
  }

  .code-body {
    padding: 20px;
    overflow-x: auto;
  }

  .code-body pre {
    margin: 0;
    font-size: 0.8rem;
    line-height: 1.7;
  }

  .code-body code {
    color: var(--text-secondary);
  }

  .c-comment { color: var(--hl-comment); }
  .c-prompt { color: var(--text-tertiary); user-select: none; }
  .c-keyword { color: var(--hl-keyword); }
  .c-string { color: var(--hl-string); }
  .c-builtin { color: var(--hl-builtin); }

  @media (min-width: 1000px) {
    .code-layout {
      grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
      gap: 64px;
    }
  }

  @media (max-width: 480px) {
    .code-body {
      padding: 14px;
    }

    .code-body pre {
      font-size: 0.7rem;
    }
  }
</style>

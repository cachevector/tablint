<script lang="ts">
  let copied = $state(false);

  async function copyInstall() {
    try {
      await navigator.clipboard.writeText('pip install tablint');
      copied = true;
      setTimeout(() => (copied = false), 1600);
    } catch {}
  }
</script>

<section class="hero">
  <div class="container hero-inner">
    <div class="copy">
      <p class="cv-eyebrow eyebrow">
        <span class="square"></span>Dataset profiler &amp; debugger
        <span class="cv-chip cv-chip-accent version">v0.1.0b1</span>
      </p>

      <h1>Lint your datasets before they reach training.</h1>

      <p class="subtitle">
        Catch critical dataset issues before they derail your ML pipeline.
        Profile, debug, and fix — all in one command.
      </p>

      <div class="actions">
        <a href="/docs#installation" class="cv-btn">Get started <span aria-hidden="true">&rarr;</span></a>
        <button type="button" class="cv-btn cv-btn-ghost" onclick={copyInstall} aria-live="polite">
          <span class="prompt" aria-hidden="true">$</span>
          {copied ? 'copied to clipboard' : 'pip install tablint'}
        </button>
      </div>
    </div>

    <div class="terminal-wrap">
      <span class="print-shadow cv-halftone" aria-hidden="true"></span>
      <div class="terminal">
        <div class="terminal-chrome">
          <span>~/project</span>
          <span>tablint</span>
        </div>
        <div class="terminal-body">
          <pre><code><span class="term-prompt">$</span> <span class="term-cmd">pip install tablint</span>
<span class="term-output">Successfully installed tablint-0.1.0b1</span>

<span class="term-prompt">$</span> <span class="term-cmd">tablint scan train.csv --target Survived</span>

<span class="term-output">  Tablint Dataset Analysis</span>
<span class="term-output">  ────────────────────────────────────</span>
<span class="term-accent">  3 critical</span><span class="term-output"> issues found</span>
<span class="term-warn">  5 warnings</span><span class="term-output"> detected</span>
<span class="term-output">  ────────────────────────────────────</span>
<span class="term-accent">  ✗ high_missing_values</span><span class="term-output">  Cabin: 77.1% missing</span>
<span class="term-accent">  ✗ class_imbalance</span><span class="term-output">      Survived: ratio 1.58</span>
<span class="term-accent">  ✗ outliers</span><span class="term-output">             Fare: 116 outliers</span>
<span class="term-warn">  ⚠ high_cardinality</span><span class="term-output">    Ticket: 681 unique</span>
<span class="term-warn">  ⚠ feature_correlation</span><span class="term-output"> SibSp ↔ Parch: 0.41</span></code></pre>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    padding: calc(var(--nav-height) + 56px) 0 72px;
  }

  .hero-inner {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 56px;
    align-items: center;
  }

  .eyebrow {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
  }

  .square {
    width: 8px;
    height: 8px;
    background: var(--accent);
  }

  .version {
    margin-left: 4px;
    text-transform: none;
  }

  h1 {
    font-size: clamp(2.5rem, 5.5vw, 4rem);
    letter-spacing: -0.045em;
    line-height: 1.02;
    max-width: 13ch;
    margin-bottom: 24px;
  }

  .subtitle {
    font-size: clamp(1rem, 1.6vw, 1.125rem);
    max-width: 480px;
    margin-bottom: 36px;
  }

  .actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .actions button {
    min-width: 200px;
  }

  .prompt {
    color: var(--text-tertiary);
  }

  /* Terminal */
  .terminal-wrap {
    position: relative;
    min-width: 0;
    margin-right: 12px;
    margin-bottom: 12px;
  }

  .print-shadow {
    position: absolute;
    inset: 12px -12px -12px 12px;
    --cv-ht-color: var(--accent);
    --cv-ht-gap: 5px;
    --cv-ht-size: 1.1px;
  }

  .terminal {
    position: relative;
    border: 1px solid var(--border-primary);
    background: var(--bg-elevated);
  }

  .terminal-chrome {
    display: flex;
    justify-content: space-between;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border-secondary);
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--text-tertiary);
  }

  .terminal-body {
    padding: 20px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .terminal-body pre {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.65;
  }

  .term-prompt {
    color: var(--text-tertiary);
    user-select: none;
  }

  .term-cmd {
    color: var(--text-primary);
    font-weight: 500;
  }

  .term-output {
    color: var(--text-secondary);
  }

  .term-accent {
    color: var(--accent);
  }

  .term-warn {
    color: var(--term-warn);
  }

  @media (min-width: 1000px) {
    .hero {
      padding: calc(var(--nav-height) + 88px) 0 96px;
    }

    .hero-inner {
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 64px;
    }
  }

  @media (max-width: 480px) {
    .terminal-body {
      padding: 14px;
    }

    .terminal-body pre {
      font-size: 0.66rem;
    }
  }
</style>

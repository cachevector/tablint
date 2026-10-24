<script lang="ts">
  import SectionHeader from './SectionHeader.svelte';

  const steps = [
    {
      step: '01',
      title: 'Scan',
      command: 'tablint scan dataset.csv',
      description: 'Run a quick scan to get a summary of critical issues in your terminal. Add --target to enable ML-specific checks.',
    },
    {
      step: '02',
      title: 'Analyze',
      command: 'tablint details dataset.csv --target Survived',
      description: 'Get comprehensive details about all detected issues including outliers, missing values, class imbalance, and data leakage.',
    },
    {
      step: '03',
      title: 'Report & Fix',
      command: 'tablint report dataset.csv --format html --with-code',
      description: 'Generate rich HTML/PDF reports with visualizations and auto-generated Python fix scripts and sklearn pipelines.',
    },
  ];
</script>

<section id="how-it-works" class="section">
  <div class="container">
    <SectionHeader
      index="02 / Workflow"
      title="Three commands. Zero guesswork."
      intro="No need to change your workflow — bring your own tools, frameworks, and datasets."
    />

    <div class="steps-grid">
      {#each steps as step}
        <div class="step-card">
          <span class="step-number">{step.step}</span>
          <h3 class="step-title">{step.title}</h3>
          <p class="step-description">{step.description}</p>
          <div class="step-command">
            <code>{step.command}</code>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .steps-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .step-card {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-top: 16px;
    border-top: 1px solid var(--border-primary);
    min-width: 0;
  }

  .step-number {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--accent);
  }

  .step-title {
    font-size: 1.125rem;
  }

  .step-command {
    padding: 10px 12px;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    overflow-x: auto;
  }

  .step-command code {
    font-size: 0.78rem;
    color: var(--code-text);
    white-space: pre;
  }

  .step-command code::before {
    content: '$ ';
    color: var(--text-tertiary);
  }

  .step-description {
    font-size: 0.9375rem;
    line-height: 1.55;
  }

  @media (min-width: 900px) {
    .steps-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 24px;
    }
  }
</style>

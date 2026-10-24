<script lang="ts">
  import SectionHeader from './SectionHeader.svelte';

  const features = [
    {
      title: 'Intelligent Profiling',
      description: 'Detect missing values, skewed distributions, outliers, and data type inconsistencies across your entire dataset.',
      icon: 'scan'
    },
    {
      title: 'ML-Specific Checks',
      description: 'Identify data leakage, dataset drift, class imbalance, and high-cardinality features before training.',
      icon: 'shield'
    },
    {
      title: 'Automated Preparation',
      description: 'Get context-aware suggestions for encoding, imputation, scaling, and transformations — with auto-apply options.',
      icon: 'wand'
    },
    {
      title: 'Rich Reporting',
      description: 'Generate statistical summaries and exportable reports in HTML, PDF, Markdown, or JSON with embedded visualizations.',
      icon: 'report'
    },
    {
      title: 'Production Pipelines',
      description: 'Output reproducible cleaning code and sklearn pipelines that integrate seamlessly into ML workflows.',
      icon: 'code'
    },
    {
      title: 'CLI & Library',
      description: 'Use as a command-line tool for quick scans or as a Python library for deep integration into your codebase.',
      icon: 'terminal'
    }
  ];
</script>

<section id="features" class="section">
  <div class="container">
    <SectionHeader
      index="01 / Features"
      title="Profile, debug, and fix your datasets in seconds"
      intro="Tablint catches critical issues before they derail your ML pipeline, explains the problems, and suggests context-aware fixes."
    />

    <div class="features-grid">
      {#each features as feature}
        <div class="feature-card">
          <div class="feature-icon">
            {#if feature.icon === 'scan'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
              </svg>
            {:else if feature.icon === 'shield'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            {:else if feature.icon === 'wand'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="m15 4-1 1 4 4 1-1a2.83 2.83 0 0 0-4-4z"/><path d="m13 6-8.5 8.5a2.12 2.12 0 1 0 3 3L16 9"/><path d="m8 16 1.5-1.5"/>
              </svg>
            {:else if feature.icon === 'report'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>
              </svg>
            {:else if feature.icon === 'code'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
              </svg>
            {:else if feature.icon === 'terminal'}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
              </svg>
            {/if}
          </div>
          <h3 class="feature-title">{feature.title}</h3>
          <p class="feature-description">{feature.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .features-grid {
    display: grid;
    grid-template-columns: 1fr;
    border-top: 1px solid var(--border-secondary);
    border-left: 1px solid var(--border-secondary);
  }

  .feature-card {
    padding: 28px 24px;
    border-right: 1px solid var(--border-secondary);
    border-bottom: 1px solid var(--border-secondary);
    background: var(--bg-elevated);
  }

  .feature-icon {
    display: flex;
    color: var(--accent);
    margin-bottom: 20px;
  }

  .feature-title {
    font-size: 1.0625rem;
    margin-bottom: 8px;
  }

  .feature-description {
    font-size: 0.9375rem;
    line-height: 1.55;
  }

  @media (min-width: 641px) {
    .features-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 1025px) {
    .features-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
</style>

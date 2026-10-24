<script lang="ts">
  import SectionHeader from './SectionHeader.svelte';

  const checks = [
    { name: 'Outliers', desc: 'IQR-based outlier detection', icon: 'alert-triangle' },
    { name: 'Missing Values', desc: 'Columns with >50% missing data', icon: 'x-circle' },
    { name: 'Duplicates', desc: 'Find duplicate rows', icon: 'copy' },
    { name: 'Class Imbalance', desc: 'Imbalanced target variable', icon: 'bar-chart' },
    { name: 'Data Leakage', desc: 'Features leaking target info', icon: 'unlock' },
    { name: 'Dataset Drift', desc: 'Distribution drift between sets', icon: 'trending-up' },
    { name: 'High Cardinality', desc: 'Too many unique categories', icon: 'hash' },
    { name: 'Correlation', desc: 'Highly correlated features', icon: 'link' },
    { name: 'Single Value', desc: 'Constant columns (no variance)', icon: 'minus' },
    { name: 'Many Zeros', desc: 'Excessive zero values', icon: 'circle' },
    { name: 'Unique Values', desc: '>95% unique value columns', icon: 'fingerprint' },
    { name: 'Uniform Distribution', desc: 'Uniformly distributed columns', icon: 'equal' },
    { name: 'Missingness Patterns', desc: 'Overall missing data analysis', icon: 'grid' },
  ];
</script>

<section class="section">
  <div class="container">
    <SectionHeader
      index="04 / Checks"
      title="13 built-in checks. Every issue caught."
      intro="From basic data quality to ML-specific concerns, Tablint runs a comprehensive audit on your dataset."
      link={{ href: '/docs#checks', label: 'Full check reference' }}
    />

    <div class="checks-grid">
      {#each checks as check}
        <div class="check-card">
          <div class="check-icon">
            {#if check.icon === 'alert-triangle'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            {:else if check.icon === 'x-circle'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            {:else if check.icon === 'copy'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
              </svg>
            {:else if check.icon === 'bar-chart'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            {:else if check.icon === 'unlock'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>
              </svg>
            {:else if check.icon === 'trending-up'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>
              </svg>
            {:else if check.icon === 'hash'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="8" y2="21"/><line x1="16" y1="3" x2="14" y2="21"/>
              </svg>
            {:else if check.icon === 'link'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
              </svg>
            {:else if check.icon === 'minus'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            {:else if check.icon === 'circle'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            {:else if check.icon === 'fingerprint'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 12C2 6.5 6.5 2 12 2a10 10 0 0 1 8 4"/><path d="M5 19.5C5.5 18 6 15 6 12c0-3.5 2.5-6 6-6 3 0 5.5 2 6 5"/><path d="M12 12v10"/>
              </svg>
            {:else if check.icon === 'equal'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
                <line x1="5" y1="9" x2="19" y2="9"/><line x1="5" y1="15" x2="19" y2="15"/>
              </svg>
            {:else if check.icon === 'grid'}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
              </svg>
            {/if}
          </div>
          <div class="check-text">
            <span class="check-name">{check.name}</span>
            <span class="check-desc">{check.desc}</span>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .checks-grid {
    display: grid;
    grid-template-columns: 1fr;
    border-top: 1px solid var(--border-secondary);
    border-left: 1px solid var(--border-secondary);
  }

  .check-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
    border-right: 1px solid var(--border-secondary);
    border-bottom: 1px solid var(--border-secondary);
    background: var(--bg-elevated);
    transition: background-color var(--transition-fast);
  }

  .check-card:hover {
    background: var(--accent-light);
  }

  .check-icon {
    flex-shrink: 0;
    display: flex;
    padding-top: 2px;
    color: var(--accent);
  }

  .check-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }

  .check-name {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .check-desc {
    font-size: 0.8125rem;
    color: var(--text-tertiary);
    line-height: 1.4;
  }

  @media (min-width: 541px) {
    .checks-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 900px) {
    .checks-grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }
</style>

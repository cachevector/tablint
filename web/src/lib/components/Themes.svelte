<script lang="ts">
  import SectionHeader from './SectionHeader.svelte';
</script>

<section class="section">
  <div class="container">
    <SectionHeader
      index="05 / Reports"
      title="Beautiful reports. Your choice of style."
      intro="Generate professional HTML reports with two built-in themes. Every report includes interactive visualizations and detailed diagnostics."
    />

    <div class="themes-grid">
      <div class="theme-card">
        <div class="theme-preview minimal-preview">
          <div class="preview-nav">
            <div class="preview-dot"></div>
            <div class="preview-line short"></div>
          </div>
          <div class="preview-content">
            <div class="preview-line wide"></div>
            <div class="preview-line medium"></div>
            <div class="preview-bars">
              <div class="preview-bar" style="height: 60%"></div>
              <div class="preview-bar" style="height: 85%"></div>
              <div class="preview-bar" style="height: 45%"></div>
              <div class="preview-bar" style="height: 70%"></div>
              <div class="preview-bar" style="height: 30%"></div>
            </div>
            <div class="preview-line wide"></div>
            <div class="preview-line short"></div>
          </div>
        </div>
        <h3 class="theme-name">Minimal</h3>
        <p class="theme-desc">Clean, professional look with soft colors and restrained typography. Ideal for stakeholder reports.</p>
      </div>

      <div class="theme-card">
        <div class="theme-preview neubrutalism-preview">
          <div class="preview-nav neu">
            <div class="preview-dot neu-dot"></div>
            <div class="preview-line short neu-line"></div>
          </div>
          <div class="preview-content">
            <div class="preview-line wide neu-line"></div>
            <div class="preview-line medium neu-line"></div>
            <div class="preview-bars">
              <div class="preview-bar neu-bar" style="height: 60%"></div>
              <div class="preview-bar neu-bar" style="height: 85%"></div>
              <div class="preview-bar neu-bar" style="height: 45%"></div>
              <div class="preview-bar neu-bar" style="height: 70%"></div>
              <div class="preview-bar neu-bar" style="height: 30%"></div>
            </div>
            <div class="preview-line wide neu-line"></div>
            <div class="preview-line short neu-line"></div>
          </div>
        </div>
        <h3 class="theme-name">Neubrutalism</h3>
        <p class="theme-desc">Bold borders, vivid accents, and high contrast. Stands out in presentations and dashboards.</p>
      </div>
    </div>
  </div>
</section>

<style>
  .themes-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }

  .theme-card {
    padding: 16px 16px 24px;
    border: 1px solid var(--border-secondary);
    background: var(--bg-elevated);
  }

  .theme-preview {
    border-radius: 0;
    overflow: hidden;
    margin-bottom: 20px;
    aspect-ratio: 16 / 10;
    border: 1px solid var(--border-secondary);
  }

  .minimal-preview {
    background: #fafafa;
  }

  :global([data-theme="dark"]) .minimal-preview {
    background: #2a2a2e;
  }

  .neubrutalism-preview {
    background: #fffef5;
    border: 2px solid #1d1d1d;
  }

  :global([data-theme="dark"]) .neubrutalism-preview {
    background: #2a2924;
    border-color: #555;
  }

  .preview-nav {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-secondary);
  }

  .preview-nav.neu {
    border-bottom: 2px solid #1d1d1d;
  }

  :global([data-theme="dark"]) .preview-nav.neu {
    border-bottom-color: #555;
  }

  .preview-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
  }

  .neu-dot {
    border-radius: 2px;
  }

  .preview-content {
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .preview-line {
    height: 6px;
    border-radius: 3px;
    background: var(--border-secondary);
  }

  .neu-line {
    border-radius: 0;
    background: #1d1d1d;
    opacity: 0.15;
  }

  :global([data-theme="dark"]) .neu-line {
    background: #aaa;
    opacity: 0.2;
  }

  .preview-line.wide { width: 80%; }
  .preview-line.medium { width: 55%; }
  .preview-line.short { width: 35%; }

  .preview-bars {
    display: flex;
    align-items: flex-end;
    gap: 6px;
    height: 60px;
    padding-top: 8px;
  }

  .preview-bar {
    flex: 1;
    background: var(--accent);
    border-radius: 2px 2px 0 0;
    opacity: 0.6;
  }

  .neu-bar {
    border-radius: 0;
    opacity: 0.8;
    border: 1.5px solid var(--text-primary);
    background: var(--accent);
  }

  .theme-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 6px;
  }

  .theme-desc {
    font-size: 0.9375rem;
    max-width: 420px;
    line-height: 1.55;
  }

  @media (max-width: 640px) {
    .themes-grid {
      grid-template-columns: 1fr;
      gap: 32px;
    }
  }
</style>

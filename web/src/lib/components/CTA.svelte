<script lang="ts">
</script>

<section class="section">
  <div class="container">
    <div class="cta-card">
      <span class="corner cv-halftone" aria-hidden="true"></span>
      <div class="cta-content">
        <p class="cv-eyebrow">Get started</p>
        <h2>Stop debugging datasets manually.</h2>
        <p class="cta-subtitle">
          Install Tablint and get your first dataset audit in under a minute.
        </p>
      </div>
      <div class="cta-side">
        <code class="cta-install"><span aria-hidden="true">$&nbsp;</span>pip install tablint</code>
        <div class="cta-actions">
          <a href="/docs#installation" class="cv-btn">Read the docs <span aria-hidden="true">&rarr;</span></a>
          <a href="https://github.com/cachevector/tablint" target="_blank" rel="noopener noreferrer" class="cv-btn cv-btn-ghost">GitHub &#8599;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .cta-card {
    position: relative;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 32px;
    padding: 40px 24px;
    border: 1px solid var(--border-primary);
    background: var(--bg-elevated);
    overflow: hidden;
  }

  .corner {
    position: absolute;
    top: 0;
    right: 0;
    width: 260px;
    height: 260px;
    --cv-ht-color: var(--accent);
    --cv-ht-gap: 6px;
    --cv-ht-size: 1.2px;
    -webkit-mask-image: radial-gradient(circle at top right, #000, transparent 70%);
    mask-image: radial-gradient(circle at top right, #000, transparent 70%);
    pointer-events: none;
  }

  .cta-content,
  .cta-side {
    position: relative;
  }

  .cta-content h2 {
    margin: 16px 0 12px;
  }

  .cta-subtitle {
    max-width: 420px;
  }

  .cta-side {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 16px;
  }

  .cta-install {
    padding: 12px 16px;
    font-size: 0.875rem;
    color: var(--code-text);
    background: var(--code-bg);
    border: 1px solid var(--code-border);
  }

  .cta-install span {
    color: var(--text-tertiary);
  }

  .cta-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  @media (min-width: 900px) {
    .cta-card {
      grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
      gap: 48px;
      padding: 56px 48px;
    }
  }
</style>

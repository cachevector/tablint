<script lang="ts">
  const currentYear = new Date().getFullYear();
</script>

<!-- Same structure as the cachevector.org footer, with Tablint's own columns. -->
<footer class="footer">
  <div class="container">
    <div class="grid">
      <div class="brand">
        <a href="/" class="brand-link" aria-label="Tablint home">
          <img src="/favicon.svg" width="26" height="26" alt="" />
          <span>Tablint</span>
        </a>
        <p class="tagline">Dataset profiler &amp; debugger for machine learning.</p>
        <a href="https://cachevector.org" class="family">
          <img src="/cachevector.svg" width="20" alt="" />
          A CacheVector project
        </a>
      </div>

      <nav class="col" aria-label="Product">
        <h2 class="cv-eyebrow">Product</h2>
        <ul>
          <li><a href="/#features">Features</a></li>
          <li><a href="/#how-it-works">How it works</a></li>
          <li><a href="https://pypi.org/project/tablint/" target="_blank" rel="noopener noreferrer">PyPI</a></li>
        </ul>
      </nav>

      <nav class="col" aria-label="Resources">
        <h2 class="cv-eyebrow">Resources</h2>
        <ul>
          <li><a href="/docs">Documentation</a></li>
          <li><a href="https://github.com/cachevector/tablint" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          <li><a href="https://github.com/cachevector/tablint/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">Contributing</a></li>
        </ul>
      </nav>

      <nav class="col" aria-label="CacheVector">
        <h2 class="cv-eyebrow">CacheVector</h2>
        <ul>
          <li><a href="https://cachevector.org/projects">All projects</a></li>
          <li><a href="https://cachevector.org/blog">Engineering notes</a></li>
          <li><a href="https://discord.gg/spuz77bcJg" target="_blank" rel="noopener noreferrer">Discord</a></li>
        </ul>
      </nav>
    </div>

    <div class="bottom">
      <span>&copy; {currentYear} CacheVector &middot; MIT License</span>
      <span class="dots cv-halftone cv-halftone-fade" aria-hidden="true"></span>
      <span>tablint.cachevector.org</span>
    </div>
  </div>
</footer>

<style>
  .footer {
    border-top: 1px solid var(--border-secondary);
    background: var(--cv-bg-sunken);
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 40px 24px;
    padding: 56px 0 48px;
  }

  .brand {
    grid-column: 1 / -1;
  }

  .brand-link {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--text-primary);
    font-weight: 600;
    letter-spacing: -0.02em;
  }

  .tagline {
    margin-top: 16px;
    max-width: 300px;
    font-size: 0.875rem;
  }

  .family {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-tertiary);
    transition: color var(--transition-fast);
  }

  .family:hover {
    color: var(--text-primary);
  }

  .col h2 {
    margin-bottom: 14px;
  }

  .col li + li {
    margin-top: 8px;
  }

  .col a {
    font-size: 0.875rem;
    color: var(--text-secondary);
    transition: color var(--transition-fast);
  }

  .col a:hover {
    color: var(--text-primary);
  }

  .bottom {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px 16px;
    padding: 20px 0 28px;
    border-top: 1px solid var(--border-secondary);
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }

  .dots {
    flex: 1;
    min-width: 40px;
    height: 8px;
    --cv-ht-color: var(--cv-fg-subtle);
    --cv-ht-gap: 5px;
    --cv-ht-size: 0.8px;
  }

  @media (min-width: 769px) {
    .grid {
      grid-template-columns: 2fr 1fr 1fr 1fr;
    }

    .brand {
      grid-column: auto;
    }
  }
</style>

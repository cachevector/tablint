<script lang="ts">
  const currentYear = new Date().getFullYear();
</script>

<footer class="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo">
          <img src="/favicon.svg" width="32" height="32" alt="" />
          <span class="footer-name">Tablint</span>
        </div>
        <p class="footer-tagline">Dataset Profiler & Debugger for Machine Learning</p>
      </div>

      <div class="footer-links">
        <div class="footer-col">
          <h4 class="footer-heading">Product</h4>
          <a href="/#features">Features</a>
          <a href="/#how-it-works">How It Works</a>
          <a href="https://pypi.org/project/tablint/">PyPI</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-heading">Resources</h4>
          <a href="/docs">Documentation</a>
          <a href="https://github.com/cachevector/tablint">GitHub</a>
          <a href="https://github.com/cachevector/tablint/blob/main/CONTRIBUTING.md">Contributing</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-heading">Legal</h4>
          <a href="https://github.com/cachevector/tablint/blob/main/LICENSE">MIT License</a>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; {currentYear} Tablint. Open source under MIT License.</p>
    </div>
  </div>
</footer>

<style>
  .footer {
    padding: 64px 0 32px;
    border-top: 1px solid var(--border-secondary);
  }

  .footer-inner {
    display: grid;
    grid-template-columns: 1.2fr 2fr;
    gap: 48px;
    margin-bottom: 48px;
  }

  .footer-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }

  .footer-name {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: -0.02em;
  }

  .footer-tagline {
    font-size: 0.85rem;
    color: var(--text-tertiary);
    line-height: 1.6;
    max-width: 280px;
  }

  .footer-links {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }

  .footer-col {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .footer-heading {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
  }

  .footer-col a {
    font-size: 0.85rem;
    color: var(--text-secondary);
    transition: color var(--transition-fast);
  }

  .footer-col a:hover {
    color: var(--accent);
  }

  .footer-bottom {
    padding-top: 24px;
    border-top: 1px solid var(--border-secondary);
  }

  .footer-bottom p {
    font-size: 0.8rem;
    color: var(--text-tertiary);
  }

  @media (max-width: 768px) {
    .footer-inner {
      grid-template-columns: 1fr;
      gap: 40px;
    }

    .footer-links {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  @media (max-width: 480px) {
    .footer {
      padding: 40px 0 20px;
    }

    .footer-inner {
      gap: 32px;
      margin-bottom: 32px;
    }

    .footer-links {
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }

    .footer-bottom p {
      font-size: 0.75rem;
    }
  }
</style>

<script lang="ts">
  import { page } from '$app/state';
  import Logo from './Logo.svelte';
  import ThemeToggle from './ThemeToggle.svelte';

  let mobileOpen = $state(false);

  const navLinks = [
    { label: 'Features', href: '/#features' },
    { label: 'How it works', href: '/#how-it-works' },
    { label: 'Docs', href: '/docs' }
  ];

  function closeMobile() {
    mobileOpen = false;
  }
</script>

<nav class="navbar">
  <div class="container navbar-inner">
    <Logo />

    <div class="nav-right">
      <div class="nav-links">
        {#each navLinks as link}
          <a href={link.href} class="nav-link" class:active={page.url.pathname === link.href}>{link.label}</a>
        {/each}
        <a href="https://github.com/cachevector/tablint" target="_blank" rel="noopener noreferrer" class="nav-link">
          GitHub <span class="ext" aria-hidden="true">&#8599;</span>
        </a>
      </div>

      <ThemeToggle />

      <a href="/docs#installation" class="cv-btn nav-cta">Get started</a>

      <button
        class="hamburger"
        onclick={() => (mobileOpen = !mobileOpen)}
        aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={mobileOpen}
        type="button"
      >
        {#if mobileOpen}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="square">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        {:else}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="square">
            <line x1="4" y1="8" x2="20" y2="8"/><line x1="4" y1="16" x2="20" y2="16"/>
          </svg>
        {/if}
      </button>
    </div>
  </div>

  {#if mobileOpen}
    <div class="mobile-menu">
      {#each navLinks as link}
        <a href={link.href} class="mobile-link" onclick={closeMobile}>{link.label}</a>
      {/each}
      <a href="https://github.com/cachevector/tablint" target="_blank" rel="noopener noreferrer" class="mobile-link">GitHub &#8599;</a>
      <a href="/docs#installation" class="cv-btn mobile-cta" onclick={closeMobile}>Get started</a>
    </div>
  {/if}
</nav>

<style>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background-color: color-mix(in srgb, var(--cv-bg) 88%, transparent);
    backdrop-filter: saturate(140%) blur(10px);
    -webkit-backdrop-filter: saturate(140%) blur(10px);
    border-bottom: 1px solid var(--border-secondary);
  }

  .navbar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: var(--nav-height);
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .nav-links {
    display: none;
    align-items: center;
    gap: 28px;
    margin-right: 12px;
  }

  .nav-link {
    position: relative;
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    padding: 6px 0;
    transition: color var(--transition-fast);
  }

  .nav-link:hover,
  .nav-link.active {
    color: var(--text-primary);
  }

  .nav-link.active::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    bottom: -1px;
    height: 1.5px;
    background: var(--accent);
  }

  .ext {
    font-size: 0.75em;
    color: var(--text-tertiary);
  }

  .nav-cta {
    display: none;
    height: 36px;
    padding: 0 16px;
    margin-left: 8px;
  }

  .hamburger {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    min-height: 44px;
    color: var(--text-primary);
  }

  .mobile-menu {
    display: flex;
    flex-direction: column;
    padding: 4px var(--cv-gutter) 16px;
    border-top: 1px solid var(--border-secondary);
    background-color: var(--bg-primary);
  }

  .mobile-link {
    padding: 14px 0;
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.9375rem;
    border-bottom: 1px solid var(--border-secondary);
  }

  .mobile-cta {
    margin-top: 16px;
    justify-content: center;
  }

  @media (min-width: 769px) {
    .nav-links,
    .nav-cta {
      display: flex;
    }

    .hamburger,
    .mobile-menu {
      display: none;
    }
  }
</style>

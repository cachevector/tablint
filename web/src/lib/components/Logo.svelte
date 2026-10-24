<script lang="ts">
  let { size = 22, showParent = true }: { size?: number; showParent?: boolean } = $props();
</script>

<div class="logo">
  {#if showParent}
    <a href="https://cachevector.org" class="parent" aria-label="CacheVector">
      <img src="/cachevector.svg" alt="" width="26" />
      <span class="parent-name">CacheVector</span>
    </a>
    <span class="sep" aria-hidden="true">/</span>
  {/if}
  <a href="/" class="product" aria-label="Tablint home">
    <img src="/favicon.svg" alt="" width={size} height={size} />
    <span class="product-name">Tablint</span>
  </a>
</div>

<style>
  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
  }

  .parent,
  .product {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .parent-name {
    font-size: 0.9375rem;
    font-weight: 500;
    letter-spacing: -0.02em;
    color: var(--text-tertiary);
    transition: color var(--transition-fast);
  }

  .parent:hover .parent-name {
    color: var(--text-primary);
  }

  .sep {
    font-family: var(--font-mono);
    color: var(--border-secondary);
    font-size: 1.125rem;
    font-weight: 300;
  }

  .product-name {
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text-primary);
  }

  @media (max-width: 480px) {
    .parent-name {
      display: none;
    }
  }
</style>

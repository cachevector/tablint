<script lang="ts">
  let { size = 32, showText = true }: { size?: number; showText?: boolean } = $props();
</script>

<a href="/" class="logo" aria-label="Tablint home">
  <img
    src="https://raw.githubusercontent.com/cachevector/tablint/refs/heads/main/docs/assets/tablint-wobg.svg"
    alt="Tablint logo"
    width={size}
    height={size}
    loading="lazy"
  />
  {#if showText}
    <span class="logo-text">Tablint</span>
  {/if}
</a>

<style>
  .logo {
    display: flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    flex-shrink: 0;
    min-width: 0;
  }

  .logo-text {
    font-family: var(--font-mono);
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    text-transform: uppercase;
  }
</style>

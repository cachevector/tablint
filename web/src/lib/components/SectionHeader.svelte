<script lang="ts">
  // Mirrors cachevector.org's SectionHeader so sections read the same across sites.
  let {
    index,
    title,
    intro = '',
    link = null
  }: { index: string; title: string; intro?: string; link?: { href: string; label: string } | null } = $props();
</script>

<header class="section-header">
  <div class="rule">
    <span class="cv-eyebrow">{index}</span>
    <span class="dots cv-halftone cv-halftone-fade" aria-hidden="true"></span>
  </div>
  <div class="row">
    <div>
      <h2>{title}</h2>
      {#if intro}
        <p class="intro">{intro}</p>
      {/if}
    </div>
    {#if link}
      <a href={link.href} class="more">{link.label} <span aria-hidden="true">&rarr;</span></a>
    {/if}
  </div>
</header>

<style>
  .section-header {
    margin-bottom: 40px;
  }

  .rule {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
  }

  .dots {
    flex: 1;
    height: 10px;
    --cv-ht-color: var(--cv-fg-subtle);
    --cv-ht-gap: 5px;
    --cv-ht-size: 0.8px;
  }

  .row {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px 32px;
  }

  .intro {
    margin-top: 10px;
    max-width: 560px;
  }

  .more {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--accent);
    white-space: nowrap;
  }

  .more:hover {
    color: var(--text-primary);
  }
</style>

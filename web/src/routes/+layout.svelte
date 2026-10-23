<script lang="ts">
  import '../app.css';
  import { page } from '$app/state';
  import { siteOrigin } from '$lib/site';
  import { theme } from '$lib/theme.svelte';
  import { onMount } from 'svelte';
  import type { Snippet } from 'svelte';

  let { children }: { children: Snippet } = $props();
  const canonical = $derived(`${siteOrigin}${page.url.pathname}`);

  onMount(() => {
    theme.init();
  });
</script>

<svelte:head>
  <title>Tablint — Dataset Profiler & Debugger for Machine Learning</title>
  <link rel="canonical" href={canonical} />
  <meta property="og:url" content={canonical} />
  <meta property="og:title" content="Tablint" />
  <meta property="og:description" content="Dataset Profiler & Debugger for Machine Learning." />
</svelte:head>

{@render children()}

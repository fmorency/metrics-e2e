<script lang="ts">
  import '@carbon/charts-svelte/styles.css';
  import { readable } from 'svelte/store';
  import { invalidateAll } from '$app/navigation';
  import ChartCard from "$lib/components/ChartCard.svelte";
  import type {ChartConfig, ChartDataPoint} from "$lib/types";

  let { title, data, configs } = $props<{
    title: string,
    data: Promise<ChartDataPoint[]>,
    configs: ChartConfig[]
  }>();

  const tick = readable(Date.now(), (set) => {
    const id = setInterval(() => set(Date.now()), 10000);
    return () => clearInterval(id);
  });

  $effect(() => {
    if ($tick) {
      invalidateAll();
    }
  });
</script>

<main class="p-4">
  <h2 class="text-xl font-bold mb-4">{title} Metrics</h2>
  {#await Promise.resolve(data) }
    <p>Loading {title.toLowerCase()} metrics data...</p>
  {:then datasets}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      {#each configs as config, i}
        <div class="card preset-filled-surface-100-900 overflow-hidden p-4">
          {#if datasets[i]?.length}
            <ChartCard config={config} data={datasets[i]} />
          {:else}
            <p>No data available for {config.title}</p>
          {/if}
        </div>
      {/each}
    </div>
  {:catch err}
    <p>Error: {err.message}</p>
  {/await}
</main>
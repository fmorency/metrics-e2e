<script lang="ts">
  import { AreaChart } from '@carbon/charts-svelte';
  import '@carbon/charts-svelte/styles.css';
  import { getChartOptions } from '$lib/options';
  import { readable } from 'svelte/store';
  import { invalidateAll } from '$app/navigation';
  import type {PageProps} from "../../.svelte-kit/types/src/routes/$types";

  let { data }: PageProps = $props();

  const configs = $derived(data.configs)
  const initialDatasets = $derived(data.data)

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

<main>
  {#await Promise.resolve(initialDatasets) }
    <p>Loading metrics data...</p>
  {:then datasets}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      {#each configs as config, i}
        <div class="rounded-lg overflow-hidden p-4">
          {#if datasets[i]?.length}
            <AreaChart
              data={datasets[i]}
              options={getChartOptions(config)}
              style="padding:2rem;"
            />
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
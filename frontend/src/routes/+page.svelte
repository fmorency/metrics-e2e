<script lang="ts">
  import '@carbon/charts-svelte/styles.css';
  import { readable } from 'svelte/store';
  import { invalidateAll } from '$app/navigation';
  import type {PageProps} from "../../.svelte-kit/types/src/routes/$types";
  import ChartCard from "$lib/ChartCard.svelte";

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
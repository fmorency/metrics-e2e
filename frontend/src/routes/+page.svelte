<script lang="ts">
  import '@carbon/charts-svelte/styles.css';
  import {ChoroplethChart, type ChoroplethChartOptions, Projection} from '@carbon/charts-svelte'
  import {worldTopoJson} from './options';
  import {data as mapData} from './data';
  import ChartCard from "$lib/components/ChartCard.svelte";
  import type {PageProps} from "../../.svelte-kit/types/src/routes/disk/$types";
  import {readable} from "svelte/store";
  import {invalidateAll} from "$app/navigation";
  import {configs} from "./config";

  let { data }: PageProps = $props();

  const tick = readable(Date.now(), (set) => {
    const id = setInterval(() => set(Date.now()), 10000);
    return () => clearInterval(id);
  });

  $effect(() => {
    if ($tick) {
      invalidateAll();
    }
  });

  const options: ChoroplethChartOptions = {
    geoData: worldTopoJson,
    height: "1000px",
    thematic: {
      projection: Projection.geoMercator
    },
    legend: {
      enabled: false
    },
    toolbar: {
      enabled: false
    },
    color: {
      gradient: {
        colors: [
          '#0f62fe',
          '#ffc2c5',
          '#8d8d8d'
        ]
      }
    }
  }
</script>

<main class="p-4">
  <h2 class="text-2xl font-extrabold">The Manifest Network</h2>
<!--  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">-->
<!--    <div class="p-4">-->
<!--      {#await Promise.resolve(data.data) }-->
<!--        <p>Loading blockchain metrics</p>-->
<!--      {:then datasets}-->
<!--        {#each configs as config, i}-->
<!--          <div class="rounded-lg overflow-hidden p-4">-->
<!--            {#if datasets[i]?.length}-->
<!--              <ChartCard config={config} data={datasets[i]} />-->
<!--            {:else}-->
<!--              <p>No data available for {config.title}</p>-->
<!--            {/if}-->
<!--          </div>-->
<!--        {/each}-->
<!--      {:catch err}-->
<!--        <p>Error: {err.message}</p>-->
<!--      {/await}-->
<!--    </div>-->

    <div class="p-4">
      <ChoroplethChart data={mapData} {options} />
    </div>
<!--  </div>-->
</main>
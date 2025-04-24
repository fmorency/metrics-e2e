<script lang="ts">
  import '@carbon/charts-svelte/styles.css';
  import {ChoroplethChart, type ChoroplethChartOptions, Projection} from '@carbon/charts-svelte'
  import {worldTopoJson} from './options';
  import {data as mapData} from './data';
  import {getColorFromCSS} from "$lib/utils/colors";

  let themeColor = getColorFromCSS('--color-surface-900')

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
          themeColor
        ]
      }
    }
  }
</script>

<main class="p-4">
      <ChoroplethChart data={mapData} {options} />
</main>
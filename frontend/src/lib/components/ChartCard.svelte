<!-- AreaChart with theme context support -->
<script lang="ts">
  import { theme } from '$lib/stores/theme';
  import { AreaChart } from '@carbon/charts-svelte';
  import type { ChartConfig, ChartDataPoint } from '$lib/types';
  import { getChartOptions } from '$lib/options';

  const { config, data } : { config: ChartConfig, data: ChartDataPoint[] } = $props();

  let chartOptions = $derived({
      ...getChartOptions(config, data[0]),
      theme: $theme === 'dark' ? 'g90' : 'g10'
  });
</script>

<AreaChart {data} options={chartOptions} />

<!-- AreaChart with theme context support -->
<script lang="ts">
  import { AreaChart } from '@carbon/charts-svelte';
  import { getChartOptions } from '$lib/options';
  import { mode } from '$lib/stores/theme';

  const { config, data } : { config: ChartConfig, data: ChartDataPoint[] } = $props();

  let isDark = $derived($mode === 'dark');
  let chartOptions = $derived({
      ...getChartOptions(config, data[0]),
      theme: isDark ? 'g90' : 'g10'
  });
</script>

<AreaChart {data} options={chartOptions} />

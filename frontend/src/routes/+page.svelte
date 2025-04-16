<script lang="ts">
  import '../app.css';
  import {LineChart, ScaleTypes} from '@carbon/charts-svelte'
  import '@carbon/charts-svelte/styles.css'
  import {onMount} from 'svelte';

  interface MetricRecord {
        timestamp: string;
        chart: string;
        dimension: string;
        value: number;
        family: string;
        instance: string;
    }

    interface ChartDataPoint {
        group: string;
        key: string;
        value: number;
        date: Date;
    }

    let chartData: ChartDataPoint[] = [];
    let loading = true;
    let error: string | null = null;

    $: chartOptions = {
        title: 'Memory available',
        axes: {
          bottom: {
            title: 'Timestamp',
            mapsTo: 'date',
            scaleType: ScaleTypes.TIME,
          },
          left: {
            mapsTo: 'value',
            title: 'Available Memory (MiB)',
            scaleType: ScaleTypes.LINEAR,
            domain: calculateDomain(chartData)
          }
        },
        height: '400px',
        theme: 'g100',
      };

    function calculateDomain(data: ChartDataPoint[]): [number, number] {
        if (data.length === 0) return [0, 100];

        const values = data.map(item => item.value);
        const min = Math.floor(Math.min(...values) * 0.9); // 10% padding below
        const max = Math.ceil(Math.max(...values) * 1.1);  // 10% padding above

        return [min, max];
      }

    async function fetchMetricsData() {
        try {
            // Adjust the URL to match your PostgREST endpoint
            const response = await fetch('http://localhost:3000/netdata_metrics?order=timestamp.desc&limit=100');

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }

            const rawData = await response.json() as MetricRecord[];

            // Transform data to match Carbon charts format
          chartData = rawData.map((record: MetricRecord): ChartDataPoint => ({
              group: record.chart,
              key: new Date(record.timestamp).toLocaleString(),
              value: record.value,
              date: new Date(record.timestamp),
            }));
        } catch (err) {
            console.error('Error fetching data:', err);
            error = err instanceof Error ? err.message : 'Unknown error';
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        fetchMetricsData();

        // Optional: Set up an interval to refresh data
        const intervalId = setInterval(fetchMetricsData, 10000); // refresh every 10 seconds

        return () => clearInterval(intervalId); // cleanup on component destroy
    });
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<main>
    <button type="button" class="btn preset-filled-primary-500">Button</button>

    {#if loading}
        <p>Loading metrics data...</p>
    {:else if error}
        <p>Error: {error}</p>
    {:else if chartData.length === 0}
        <p>No data available</p>
    {:else}
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
        <LineChart data={chartData} options={chartOptions} style="padding:2rem;" />
    {/if}
</main>

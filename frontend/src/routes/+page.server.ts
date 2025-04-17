import type { PageServerLoad } from './$types';
import type { ChartConfig, MetricRecord, ChartDataPoint } from '$lib/types';
import { error } from '@sveltejs/kit';

// Define your chart configurations once
const configs: ChartConfig[] = [
  { id: 'system.ram', title: 'Total RAM Available', yAxisTitle: 'Available Memory (MiB)' },
  { id: 'disk.space', title: 'Used Disk Space', yAxisTitle: 'Used Space (GiB)' },
  { id: 'system.network.received', title: 'Total IPv4 Bandwidth Received', yAxisTitle: '' },
  { id: 'system.network.sent', title: 'Total IPv4 Bandwidth Sent', yAxisTitle: '' },
  { id: 'system.tcp.sent', title: 'Total IPv4 TCP Packets Sent', yAxisTitle: 'Number of packets' },
  { id: 'cpu.count', title: 'Number of CPU cores', yAxisTitle: '' }
];

export const load: PageServerLoad = async ({ fetch }) => {
  // Fetch all datasets in parallel
  const data = await Promise.all(
    configs.map(async (config) => {
      const res = await fetch(`/netdata_metrics?chart=eq.${config.id}&order=timestamp.desc&limit=100`);
      if (!res.ok) throw error(500, `Failed to fetch data for ${config.id}`);

      const raw: MetricRecord[] = await res.json();
      return raw.map((r) => ({
        group: r.chart,
        key: new Date(r.timestamp).toLocaleString(),
        value: r.value,
        date: new Date(r.timestamp)
      })) as ChartDataPoint[];
    })
  );

  return { configs, data };
};
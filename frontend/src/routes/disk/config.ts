import type { ChartConfig } from '$lib/types';

export const configs: ChartConfig[] = [
  {
    id: 'disk.space.total',
    title: 'Total Disk Space',
    yAxisTitle: 'Total Space (GiB)',
    category: 'disk'
  },
  {
    id: 'disk.space',
    title: 'Used Disk Space',
    yAxisTitle: 'Used Space (GiB)',
    category: 'disk'
  },
];
import type {ChartConfig} from "$lib/types";

export const configs: ChartConfig[] = [
  {
    id: 'system.memory',
    title: 'Total RAM Available',
    yAxisTitle: 'Available Memory (MiB)'
  },
  { id: 'system.cpu.cores',
    title: 'Number of CPU cores',
    yAxisTitle: 'CPU cores'
  }
];

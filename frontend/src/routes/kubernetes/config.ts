import type { ChartConfig } from '$lib/types';

export const configs: ChartConfig[] = [
  {
    id: 'kube.pods',
    title: 'Kubernetes Pods Count',
    yAxisTitle: 'Number of Pods',
    category: 'kube'
  },
  {
    id: 'kube.nodes',
    title: 'Kubernetes Nodes Count',
    yAxisTitle: 'Number of Nodes',
    category: 'kube'
  },
  {
    id: 'kube.cpu',
    title: 'Kubernetes CPU Count',
    yAxisTitle: 'Number of CPU',
    category: 'kube'
  },
  {
    id: 'kube.memory',
    title: 'Kubernetes Memory (TiB)',
    yAxisTitle: 'Memory (TiB)',
    category: 'kube'
  },
];
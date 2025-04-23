import type { ChartConfig } from '$lib/types';

export const configs: ChartConfig[] = [
  {
    id: 'system.network.received',
    title: 'Total IPv4 Bandwidth Received',
    yAxisTitle: '',
    category: 'network'
  },
  {
    id: 'system.network.sent',
    title: 'Total IPv4 Bandwidth Sent',
    yAxisTitle: '',
    category: 'network'
  },
  {
    id: 'system.tcp.received',
    title: 'Total IPv4 TCP Packets Received',
    yAxisTitle: 'Number of packets',
    category: 'network'
  },
  {
    id: 'system.tcp.sent',
    title: 'Total IPv4 TCP Packets Sent',
    yAxisTitle: 'Number of packets',
    category: 'network'
  },
];
export const configs: ChartConfig[] = [
  {
    id: 'gpu.total',
    title: 'Total Number of GPU',
    yAxisTitle: 'Number of GPU',
    category: 'gpu'
  },
  {
    id: 'gpu.memory',
    title: 'Total GPU Memory',
    yAxisTitle: 'Memory (MiB)',
    category: 'gpu'
  },
  {
    id: 'gpu.nvidia.total',
    title: 'Total Number of NVIDIA GPU',
    yAxisTitle: 'Number of NVIDIA GPU',
    category: 'gpu'
  },
  {
    id: 'gpu.nvidia.memory',
    title: 'Total NVIDIA GPU Memory',
    yAxisTitle: 'NVIDIA GPU Memory (MiB)',
    category: 'gpu'
  },
  {
    id: 'gpu.nvidia.cuda.total',
    title: 'Total Number of NVIDIA CUDA Cores',
    yAxisTitle: 'Number of NVIDIA CUDA Cores',
    category: 'gpu'
  },
  {
    id: 'gpu.amd.total',
    title: 'Total Number of AMD GPU',
    yAxisTitle: 'Number of AMD GPU',
    category: 'gpu'
  },
  {
    id: 'gpu.amd.memory',
    title: 'Total AMD GPU Memory',
    yAxisTitle: 'AMD GPU Memory',
    category: 'gpu'
  },
];

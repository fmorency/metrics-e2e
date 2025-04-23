type ChartCategory = 'disk' | 'network' | 'minio' | 'kube' | 'gpu' | 'blockchain';

export interface ChartConfig {
  id: string;
  title: string;
  yAxisTitle: string;
  category?: ChartCategory;
}

export interface MetricRecord {
  timestamp: string;
  chart: string;
  dimension: string;
  value: number;
  family: string;
  instance: string;
}

export interface ChartDataPoint {
  group: string;
  key: string;
  value: number;
  date: Date;
}
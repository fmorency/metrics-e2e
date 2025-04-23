type ChartCategory = 'disk' | 'network' | 'minio' | 'kube' | 'gpu' | 'blockchain';
export type TimeInterval = '15s' | '1m' | '1h' | '1d' | '1w' | '1M' | '1y';

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
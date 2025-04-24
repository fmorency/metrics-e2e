type ChartCategory = 'disk' | 'network' | 'minio' | 'kube' | 'gpu' | 'blockchain';
type TimeInterval = '15 seconds' | '1 minute' | '1 hour' | '1 day' | '1 week' | '1 month' | '1 year';

interface ChartConfig {
  id: string;
  title: string;
  yAxisTitle: string;
  category?: ChartCategory;
}

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

type Theme = {
  value: 'system' | 'light' | 'dark'
}
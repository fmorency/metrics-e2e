import {error} from "@sveltejs/kit";
import type {ChartConfig, ChartDataPoint, MetricRecord} from "$lib/types";
import type { PageServerLoad } from "../../routes/$types";

export function createLoad(configs: ChartConfig[]) {
  const loadFn: PageServerLoad = async ({ fetch }) => {
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

  return loadFn;
}

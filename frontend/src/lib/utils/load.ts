import {error} from "@sveltejs/kit";
import type { PageServerLoad } from "../../routes/$types";
import {ALLOWED_INTERVALS, IntervalMap, isValidDateString, isValidTimeInterval} from "$lib/utils/time";

/**
 * Extracts, validates, and prepares URL search parameters for the API call.
 * Throws SvelteKit errors for invalid parameters.
 * Returns a URLSearchParams object ready for the API request.
 */
function extractAndPrepareApiParams(url: URL): URLSearchParams | null {
  const intervalParam = url.searchParams.get("interval");
  if (!intervalParam) {
    return null
  }
  if (!isValidTimeInterval(intervalParam)) {
    throw error(400, `Invalid interval parameter. Allowed values are: ${ALLOWED_INTERVALS.join(', ')}`);
  }
  const interval = intervalParam;
  const scale = IntervalMap[interval];
  const now = new Date();

  switch (interval) {
    case '1 minute':
      now.setMinutes(now.getMinutes() - 1);
      break;
    case '1 hour':
      now.setHours(now.getHours() - 1);
      break;
    case '1 day':
      now.setDate(now.getDate() - 1);
      break;
    case '1 week':
      now.setDate(now.getDate() - 7);
      break;
    case '1 month':
      now.setMonth(now.getMonth() - 1);
      break;
    case '1 year':
      now.setFullYear(now.getFullYear() - 1);
      break;
  }

  // Prepare validated parameters for API call
  const apiParams = new URLSearchParams({
    order: 'timestamp.desc',
    interval_str: scale,
  });

  apiParams.set('time_from', now.toISOString());
  apiParams.set('time_to', new Date().toISOString());

  return apiParams;
}

export function createLoad(configs: ChartConfig[]) {
  const loadFn: PageServerLoad = async ({ fetch, url }) => {
    const baseApiParams = extractAndPrepareApiParams(url);
    if (!baseApiParams) {
      return { configs, data: [] };
    }

    const data = await Promise.all(
      configs.map(async (config) => {
        const currentParams = new URLSearchParams(baseApiParams);
        currentParams.set('chart_name', config.id);

        let apiUrl = `/rpc/get_aggregated_metrics?${currentParams.toString()}`;

        try {
          const res = await fetch(apiUrl);
          if (!res.ok) {
            console.error(`Failed to fetch data for ${config.id}: ${res.status}`);
            throw new Error(`API request failed with status ${res.status}`);
          }

          const raw: MetricRecord[] = await res.json();
          return raw.map((r) => ({
            group: r.chart,
            key: new Date(r.timestamp).toLocaleString(),
            value: r.value,
            date: new Date(r.timestamp)
          })) as ChartDataPoint[];
        } catch (e) {
          console.error(`Error fetching data for ${config.id}:`, e);
          throw error(500, `Error fetching data for ${config.id}`);
        }
      })
    );

    return { configs, data };
  };

  return loadFn;
}

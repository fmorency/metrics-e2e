import {error} from "@sveltejs/kit";
import type {ChartConfig, ChartDataPoint, MetricRecord} from "$lib/types";
import type { PageServerLoad } from "../../routes/$types";
import {ALLOWED_INTERVALS, isValidDateString, isValidTimeInterval} from "$lib/utils/time";

/**
 * Extracts, validates, and prepares URL search parameters for the API call.
 * Throws SvelteKit errors for invalid parameters.
 * Returns a URLSearchParams object ready for the API request.
 */
function extractAndPrepareApiParams(url: URL): URLSearchParams {
  // Extract and validate interval
  const intervalParam = url.searchParams.get("interval") || '1m'; // Default interval
  if (!isValidTimeInterval(intervalParam)) {
    throw error(400, `Invalid interval parameter. Allowed values are: ${ALLOWED_INTERVALS.join(', ')}`);
  }
  const interval = intervalParam; // Assign validated interval

  // Extract and validate time_from
  const timeFrom = url.searchParams.get("time_from");
  if (timeFrom && !isValidDateString(timeFrom)) {
    throw error(400, `Invalid time_from parameter. Expected a valid date string.`);
  }

  // Extract and validate time_to
  const timeTo = url.searchParams.get("time_to");
  if (timeTo && !isValidDateString(timeTo)) {
    throw error(400, `Invalid time_to parameter. Expected a valid date string.`);
  }

  // Prepare validated parameters for API call
  const apiParams = new URLSearchParams({
    order: 'timestamp.desc',
    interval_str: interval, // Use validated interval
  });

  if (timeFrom) {
    // Convert valid date string to ISO string for the API
    apiParams.set('time_from', new Date(timeFrom).toISOString());
  }
  if (timeTo) {
    // Convert valid date string to ISO string for the API
    apiParams.set('time_to', new Date(timeTo).toISOString());
  }

  return apiParams;
}

export function createLoad(configs: ChartConfig[]) {
  const loadFn: PageServerLoad = async ({ fetch, url }) => {
    const baseApiParams = extractAndPrepareApiParams(url);

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

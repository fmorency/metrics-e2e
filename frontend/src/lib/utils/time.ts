import type {TimeInterval} from "$lib/types";

export const ALLOWED_INTERVALS: TimeInterval[] = ['15s', '1m', '1h', '1d', '1w', '1M', '1y'];

export function isValidTimeInterval(interval: string | null): interval is TimeInterval {
  return !!interval && ALLOWED_INTERVALS.includes(interval as TimeInterval);
}

export function isValidDateString(dateString: string | null): boolean {
  if (!dateString) return false;
  const date = new Date(dateString);
  return !isNaN(date.getTime());
}
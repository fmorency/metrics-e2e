export const ALLOWED_INTERVALS: TimeInterval[] = ['15 seconds', '1 minute', '1 hour', '1 day', '1 week', '1 month', '1 year'];

export function isValidTimeInterval(interval: string | null): interval is TimeInterval {
  return !!interval && ALLOWED_INTERVALS.includes(interval as TimeInterval);
}

export function isValidDateString(dateString: string | null): boolean {
  if (!dateString) return false;
  const date = new Date(dateString);
  return !isNaN(date.getTime());
}
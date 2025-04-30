-- Create hypertable for Netdata metrics
CREATE TABLE IF NOT EXISTS netdata_metrics (
    timestamp TIMESTAMPTZ NOT NULL,
    chart VARCHAR(4096) NOT NULL,
    family VARCHAR(4096) NOT NULL,
    dimension VARCHAR(4096) NOT NULL,
    instance VARCHAR(4096) NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('netdata_metrics', 'timestamp', if_not_exists => TRUE);
ALTER TABLE netdata_metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'chart,family,dimension,instance'
);
SELECT add_retention_policy('netdata_metrics', INTERVAL '365 days');
SELECT add_compression_policy('netdata_metrics', INTERVAL '1 month');

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_netdata_metrics_chart ON netdata_metrics (chart, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_netdata_metrics_family ON netdata_metrics (family, timestamp DESC);

CREATE OR REPLACE FUNCTION get_aggregated_metrics(
    chart_name VARCHAR,
    interval_str VARCHAR DEFAULT '1 hour',
    time_from TIMESTAMPTZ DEFAULT NULL,
    time_to TIMESTAMPTZ DEFAULT NULL
)
RETURNS TABLE (
    "timestamp" TIMESTAMPTZ,
    chart VARCHAR,
    family VARCHAR,
    dimension VARCHAR,
    instance VARCHAR,
    "value" DOUBLE PRECISION
) AS $$
BEGIN
    -- Set default time range if not specified
    IF time_from IS NULL THEN
        time_from := NOW() - INTERVAL '1 day';
    END IF;

    IF time_to IS NULL THEN
        time_to := NOW();
    END IF;

    RETURN QUERY
    SELECT
        time_bucket(interval_str::INTERVAL, nm.timestamp) as timestamp,
        nm.chart,
        nm.family,
        nm.dimension,
        nm.instance,
        AVG(nm.value) as value
    FROM netdata_metrics nm
    WHERE
        nm.chart = chart_name
        AND nm.timestamp >= time_from
        AND nm.timestamp <= time_to
    GROUP BY
        time_bucket(interval_str::INTERVAL, nm.timestamp),
        nm.chart,
        nm.family,
        nm.dimension,
        nm.instance
    ORDER BY
        timestamp DESC;
END;
$$ LANGUAGE plpgsql;
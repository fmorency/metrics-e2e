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

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_netdata_metrics_chart ON netdata_metrics (chart, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_netdata_metrics_family ON netdata_metrics (family, timestamp DESC);
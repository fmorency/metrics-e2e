import os
import time
import logging
import requests
import psycopg2
import schedule
import random
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('prometheus-etl')

# Get configuration from environment variables
PROMETHEUS_URL = os.environ.get('PROMETHEUS_URL', 'http://prometheus:9090')
TIMESCALEDB_HOST = os.environ.get('TIMESCALEDB_HOST', 'timescaledb')
TIMESCALEDB_PORT = os.environ.get('TIMESCALEDB_PORT', '5432')
TIMESCALEDB_DATABASE = os.environ.get('TIMESCALEDB_DATABASE', 'metrics')
TIMESCALEDB_USER = os.environ.get('TIMESCALEDB_USER', 'postgres')
TIMESCALEDB_PASSWORD = os.environ.get('TIMESCALEDB_PASSWORD', 'postgres')
COLLECTION_INTERVAL = int(os.environ.get('COLLECTION_INTERVAL', '10'))
QUERIES_CONFIG_PATH = os.environ.get('QUERIES_CONFIG_PATH', '/app/queries.json')

# Default queries configuration
DEFAULT_QUERIES = [
    {
        "query": "netdata_mem_available_MiB_average{}",
        "chart": "mem.available",
        "family": "mem",
        "dimension": "avail",
        "add_jitter": True
    }
]

def load_queries_config():
    """Load queries configuration from file or use defaults"""
    try:
        if os.path.exists(QUERIES_CONFIG_PATH):
            with open(QUERIES_CONFIG_PATH, 'r') as f:
                queries = json.load(f)
                logger.info(f"Loaded {len(queries)} queries from config file")
                return queries
        else:
            logger.warning(f"Config file {QUERIES_CONFIG_PATH} not found, using default queries")
            return DEFAULT_QUERIES
    except Exception as e:
        logger.error(f"Error loading query configuration: {e}")
        return DEFAULT_QUERIES

def get_db_connection():
    """Create a connection to TimescaleDB"""
    return psycopg2.connect(
        host=TIMESCALEDB_HOST,
        port=TIMESCALEDB_PORT,
        dbname=TIMESCALEDB_DATABASE,
        user=TIMESCALEDB_USER,
        password=TIMESCALEDB_PASSWORD
    )

def fetch_prometheus_metrics(query):
    """Fetch metrics for a specific Prometheus query"""
    try:
        query_params = {
            'query': query,
        }
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params=query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Prometheus: {e}")
        return None

def transform_data(prometheus_json, config):
    """Transform Prometheus data based on query configuration"""
    if not prometheus_json or prometheus_json.get('status') != 'success':
        logger.error(f"Invalid response from Prometheus: {prometheus_json}")
        return []

    records = []
    results = prometheus_json.get('data', {}).get('result', [])

    if not results:
        logger.warning(f"No data points found for query: {config['query']}")
        return []

    chart = config.get('chart', 'unknown')
    family = config.get('family', 'unknown')
    dimension = config.get('dimension', 'unknown')
    add_jitter = config.get('add_jitter', False)

    for result in results:
        # Get metric metadata
        metric = result.get('metric', {})
        instance = metric.get('instance', 'unknown')
        point = result.get('value', [])

        # Process values (timestamp, value pairs)
        if len(point) == 2:
            timestamp_epoch, value = point
            iso_timestamp = datetime.fromtimestamp(timestamp_epoch).isoformat()
            try:
                float_value = float(value)
                if add_jitter:
                    jitter = random.uniform(0.05, 0.15)
                    float_value *= (1 + jitter)

                records.append({
                    'timestamp': iso_timestamp,
                    'chart': chart,
                    'family': family,
                    'dimension': dimension,
                    'instance': instance,
                    'value': float_value
                })
            except (ValueError, TypeError) as e:
                logger.error(f"Error converting value '{value}': {e}")

    return records

def load_to_timescaledb(records):
    """Insert transformed records into TimescaleDB"""
    if not records:
        logger.warning("No records to insert")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for record in records:
            cursor.execute(
                """
                INSERT INTO netdata_metrics
                (timestamp, chart, family, dimension, instance, value)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    record['timestamp'],
                    record['chart'],
                    record['family'],
                    record['dimension'],
                    record['instance'],
                    record['value']
                )
            )

        conn.commit()
        logger.info(f"Successfully inserted {len(records)} records")
    except Exception as e:
        logger.error(f"Error inserting data into TimescaleDB: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def etl_job():
    """Run the full ETL process for all configured queries"""
    logger.info("Starting ETL job")

    queries_config = load_queries_config()
    total_records = 0

    for config in queries_config:
        query = config.get('query')
        if not query:
            logger.warning(f"Skipping query config missing query string: {config}")
            continue

        logger.info(f"Processing query: {query}")
        data = fetch_prometheus_metrics(query)
        records = transform_data(data, config)
        if records:
            load_to_timescaledb(records)
            total_records += len(records)

    logger.info(f"ETL job completed - processed {total_records} records from {len(queries_config)} queries")

def main():
    """Main entry point for the ETL service"""
    logger.info("Starting Prometheus to TimescaleDB ETL service")

    # Run the job immediately once
    etl_job()

    # Schedule the job to run at the specified interval
    schedule.every(COLLECTION_INTERVAL).seconds.do(etl_job)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
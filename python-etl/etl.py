import os
import time
import logging
import requests
import psycopg2
import schedule
import random
import json
import math
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('prometheus-etl')

PROMETHEUS_URL = os.environ.get('PROMETHEUS_URL', 'http://prometheus:9090')
TIMESCALEDB_HOST = os.environ.get('TIMESCALEDB_HOST', 'timescaledb')
TIMESCALEDB_PORT = os.environ.get('TIMESCALEDB_PORT', '5432')
TIMESCALEDB_DATABASE = os.environ.get('TIMESCALEDB_DATABASE', 'metrics')
TIMESCALEDB_USER = os.environ.get('TIMESCALEDB_USER', 'postgres')
TIMESCALEDB_PASSWORD = os.environ.get('TIMESCALEDB_PASSWORD', 'postgres')
COLLECTION_INTERVAL = int(os.environ.get('COLLECTION_INTERVAL', '10'))
QUERIES_CONFIG_PATH = os.environ.get('QUERIES_CONFIG_PATH', '/app/queries.json')

DEFAULT_QUERIES = [
    {
        "query": "netdata_mem_available_MiB_average{}",
        "chart": "mem.available",
        "family": "mem",
        "dimension": "avail",
        "add_jitter": True
    }
]

def preload_historical_data(days=365, step='1m'):
    logger.info(f"Preloading {days} days of historical data from Prometheus")
    queries_config = load_queries_config()
    end = int(time.time())
    start = end - days * 86400

    for config in queries_config:
        query = config.get('query')
        if not query:
            continue
        logger.info(f"Preloading for query: {query}")
        # Prometheus limits: fetch in 7-day chunks to avoid timeouts
        chunk_seconds = 7 * 86400
        for chunk_start in range(start, end, chunk_seconds):
            chunk_end = min(chunk_start + chunk_seconds, end)
            params = {
                'query': query,
                'start': chunk_start,
                'end': chunk_end,
                'step': step
            }
            try:
                response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params=params)
                response.raise_for_status()
                prometheus_json = response.json()
                records = transform_range_data(prometheus_json, config)
                if records:
                    load_to_timescaledb(records)
                    logger.info(f"Inserted {len(records)} records for {query} ({datetime.fromtimestamp(chunk_start)} to {datetime.fromtimestamp(chunk_end)})")
            except Exception as e:
                logger.error(f"Error preloading data for {query}: {e}")

def transform_range_data(prometheus_json, config):
    if not prometheus_json or prometheus_json.get('status') != 'success':
        logger.error(f"Invalid response from Prometheus: {prometheus_json}")
        return []

    records = []
    results = prometheus_json.get('data', {}).get('result', [])
    chart = config.get('chart', 'unknown')
    family = config.get('family', 'unknown')
    dimension = config.get('dimension', 'unknown')
    add_jitter = config.get('add_jitter', False)

    for result in results:
        metric = result.get('metric', {})
        instance = metric.get('instance', 'unknown')
        values = result.get('values', [])
        for point in values:
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


def fetch_and_transform_query(config):
    query = config.get('query')
    if not query:
        logger.warning(f"Skipping query config missing query string: {config}")
        return []

    logger.info(f"Fetching data for query: {query}")
    data = fetch_prometheus_metrics(query)
    records = transform_data(data, config)
    return records

def etl_job_parallel(max_workers=5, batch_size=None):
    logger.info("Starting parallel ETL job")

    queries_config = load_queries_config()
    all_records = []

    if batch_size is None:
        batch_size = len(queries_config)

    # Process queries in batches
    for i in range(0, len(queries_config), batch_size):
        batch = queries_config[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} with {len(batch)} queries")

        batch_records = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_query = {executor.submit(fetch_and_transform_query, config): config for config in batch}

            for future in as_completed(future_to_query):
                config = future_to_query[future]
                try:
                    records = future.result()
                    batch_records.extend(records)
                    logger.info(f"Fetched {len(records)} records for query: {config.get('query')}")
                except Exception as e:
                    logger.error(f"Error processing query {config.get('query')}: {e}")

        all_records.extend(batch_records)

    if all_records:
        logger.info(f"Loading all {len(all_records)} records in a single transaction")
        load_to_timescaledb(all_records)
    else:
        logger.warning("No records to load to database")

    logger.info(f"ETL job completed - processed {len(all_records)} records from {len(queries_config)} queries")
    return len(all_records)

def load_queries_config():
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
    return psycopg2.connect(
        host=TIMESCALEDB_HOST,
        port=TIMESCALEDB_PORT,
        dbname=TIMESCALEDB_DATABASE,
        user=TIMESCALEDB_USER,
        password=TIMESCALEDB_PASSWORD
    )

def fetch_prometheus_metrics(query):
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
        metric = result.get('metric', {})
        instance = metric.get('instance', 'unknown')
        point = result.get('value', [])

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
    if not records:
        logger.warning("No records to insert")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        values = [
            (
                record['timestamp'],
                record['chart'],
                record['family'],
                record['dimension'],
                record['instance'],
                record['value']
            )
            for record in records
        ]

        cursor.executemany(
            """
            INSERT INTO netdata_metrics
            (timestamp, chart, family, dimension, instance, value)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            values
        )

        conn.commit()
        logger.info(f"Successfully inserted {len(records)} records in a single transaction")
    except Exception as e:
        logger.error(f"Error inserting data into TimescaleDB: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def main():
    logger.info("Starting Prometheus to TimescaleDB ETL service")

    preload_historical_data(days=365, step='5m')
    etl_job_parallel(max_workers=5, batch_size=10)

    schedule.every(COLLECTION_INTERVAL).seconds.do(
        lambda: etl_job_parallel(max_workers=5, batch_size=10)
    )

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
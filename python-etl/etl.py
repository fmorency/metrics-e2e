import os
import time
import json
import logging
import datetime
import requests
import psycopg2
import schedule
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('netdata-etl')

# Get configuration from environment variables
NETDATA_URL = os.environ.get('NETDATA_URL', 'http://netdata:19999')
TIMESCALEDB_HOST = os.environ.get('TIMESCALEDB_HOST', 'timescaledb')
TIMESCALEDB_PORT = os.environ.get('TIMESCALEDB_PORT', '5432')
TIMESCALEDB_DATABASE = os.environ.get('TIMESCALEDB_DATABASE', 'metrics')
TIMESCALEDB_USER = os.environ.get('TIMESCALEDB_USER', 'postgres')
TIMESCALEDB_PASSWORD = os.environ.get('TIMESCALEDB_PASSWORD', 'postgres')
COLLECTION_INTERVAL = int(os.environ.get('COLLECTION_INTERVAL', '10'))

def get_db_connection():
    """Create a connection to TimescaleDB"""
    return psycopg2.connect(
        host=TIMESCALEDB_HOST,
        port=TIMESCALEDB_PORT,
        dbname=TIMESCALEDB_DATABASE,
        user=TIMESCALEDB_USER,
        password=TIMESCALEDB_PASSWORD
    )

def fetch_netdata_metrics():
    """Fetch metrics from Netdata API"""
    try:
        response = requests.get(f"{NETDATA_URL}/api/v1/data?chart=mem.available&points=1&after=-{COLLECTION_INTERVAL}&options=seconds")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Netdata: {e}")
        return None

def transform_data(netdata_json):
    """Transform Netdata JSON to match our database schema"""
    if not netdata_json:
        return []

    records = []
    chart = 'mem.available'  # Example chart name, can be dynamic
    host = netdata_json.get('host', 'localhost')

    # Extract family from chart name
    parts = chart.split('.')
    family = parts[0] if len(parts) > 1 else 'default'

    for datapoint in netdata_json.get('data', []):
        # First element is timestamp, followed by values for each dimension
        timestamp_epoch = datapoint[0]
        iso_timestamp = datetime.fromtimestamp(timestamp_epoch).isoformat()

        # Start from index 1 (after timestamp) for dimension values
        # for i, dimension_name in enumerate(dimensions):
        value = datapoint[1]

        records.append({
            'timestamp': iso_timestamp,
            'chart': chart,
            'family': family,
            'dimension': "avail",
            'instance': host,
            'value': value
        })

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
    """Run the full ETL process"""
    logger.info("Starting ETL job")
    data = fetch_netdata_metrics()
    records = transform_data(data)
    load_to_timescaledb(records)
    logger.info("ETL job completed")

def main():
    """Main entry point for the ETL service"""
    logger.info("Starting Netdata to TimescaleDB ETL service")

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
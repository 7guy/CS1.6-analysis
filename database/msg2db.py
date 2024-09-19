import json
import os
import psycopg2
from psycopg2 import sql
from getpass import getpass
import logging
import coloredlogs

logger = logging.getLogger(__name__)
# Define custom formats for different log levels
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
coloredlogs.install(level='DEBUG', logger=logger, fmt=log_format)

# Database connection parameters
DB_NAME = "CS1.6"  # Your database name
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASSWORD = getpass("Enter your PostgreSQL password: ")   # Your PostgreSQL password
DB_HOST = "localhost"  # Usually 'localhost' if running locally
DB_PORT = "5432"  # Default port for PostgreSQL

# Connect to the database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Define the directory containing parsed JSON files
parsed_data_folder = os.path.expanduser("~/PycharmProjects/cs_analytics/database/parsed_data")


# Function to insert data into the table
def insert_kill_event(event, log_address):
    query = """
        INSERT INTO kill_events (ts, event_type, killer_name, killer_id, victim_name, victim_id, weapon, distance,headshot, log_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    data = (event.get("timestamp"), event.get("event_type"), event.get("killer_name"),
            event.get("killer_id"), event.get("victim_name"), event.get("victim_id"),
            event.get("weapon"), event.get("distance"), event.get("headshot"), log_address)

    cur.execute(query, data)


# Iterate over all JSON files in the folder and insert Player_Kill events
for file_name in os.listdir(parsed_data_folder):
    kill_event_flag = 0
    log_address = file_name.replace('_parsed.json', '')
    cur.execute("SELECT 1 FROM kill_events WHERE log_address = %s", (log_address,))
    result = cur.fetchone()
    if result:
        logger.warning(f'Events from log file {log_address} have already inserted to the DB')
        continue
    else:
        if file_name.endswith('_parsed.json'):
            file_path = os.path.join(parsed_data_folder, file_name)
            with open(file_path, 'r') as f:
                parsed_data = json.load(f)
                for event in parsed_data:
                    if event.get("event_type") == "Player_Kill":
                        insert_kill_event(event, log_address)
                        kill_event_flag = 1
                if kill_event_flag:
                    logger.info(f'Successfully inserted events from log file {log_address} to the DB')
                else:
                    logger.warning(f'Skipped log file {log_address} - no kill events')
# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

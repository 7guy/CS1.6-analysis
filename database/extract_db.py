import psycopg2
from getpass import getpass
import pandas as pd

NICK = '@batata doce'

# Database connection parameters
DB_NAME = "CS1.6"  # Your database name
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASSWORD =  getpass("Enter your PostgreSQL password: ")   # Your PostgreSQL password
DB_HOST = "localhost"  # Usually 'localhost' if running locally
DB_PORT = "5432"  # Default port for PostgreSQL

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,  # or use input to hide the password
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def get_kill_events():
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM kill_events;"
    df = pd.read_sql_query(query, conn)
    cur.close()
    conn.close()
    return df

def killer_victim_ratio():
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT SUM(CASE WHEN killer_name = '@batata doce' THEN 1 ELSE 0 END) AS kill_count, SUM(CASE WHEN victim_name = '@batata doce' THEN 1 ELSE 0 END) AS death_count FROM kill_events;"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def kills_by_weapon():
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT weapon, COUNT(*) as kills
    FROM kill_events
    WHERE killer_name = '@batata doce'
    GROUP BY weapon
    ORDER BY kills DESC;
    """
    cur.execute(query)
    result = cur.fetchall()

    # Convert result to DataFrame
    df = pd.DataFrame(result, columns=['Weapon', 'Kills'])

    cur.close()
    conn.close()

    return df

def deaths_by_weapon():
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT weapon, COUNT(*) as kills
    FROM kill_events
    WHERE victim_name = '@batata doce'
    GROUP BY weapon
    ORDER BY kills DESC;
    """
    cur.execute(query)
    result = cur.fetchall()

    # Convert result to DataFrame
    df = pd.DataFrame(result, columns=['Weapon', 'Deaths'])

    cur.close()
    conn.close()

    return df

def kills_by_distance():
    query = """
        SELECT distance, COUNT(*) as kills
        FROM kill_events
        WHERE killer_name = '@batata doce'
        GROUP BY distance
        ORDER BY distance;
    """
    # Execute the query and return the data as a DataFrame
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    df_kills = pd.read_sql(query, conn)
    conn.close()
    return df_kills

def deaths_by_distance():
    query = """
        SELECT distance, COUNT(*) as deaths
        FROM kill_events
        WHERE victim_name = '@batata doce'
        GROUP BY distance
        ORDER BY distance;
    """
    # Execute the query and return the data as a DataFrame
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    df_deaths = pd.read_sql(query, conn)
    conn.close()
    return df_deaths


def avg_kill_distance_per_weapon():
    conn = get_connection()
    cur = conn.cursor()
    query_kills = """
     SELECT weapon, ROUND(AVG(distance)::numeric, 2) as avg_kill_distance, VAR_POP(distance) AS var_kill_distance
     FROM kill_events
     WHERE killer_name = '@batata doce' AND distance IS NOT NULL
     GROUP BY weapon;
     """

    cur.execute(query_kills)
    kills_df = pd.DataFrame(cur.fetchall(), columns=['Weapon', 'Avg_Kill_Distance','Var_Kill_Distance'])
    cur.close()
    conn.close()
    return kills_df


def avg_death_distance_per_weapon():
    conn = get_connection()
    cur = conn.cursor()
    query_deaths = """
       SELECT weapon, ROUND(AVG(distance)::numeric, 2) as avg_death_distance,VAR_POP(distance) AS var_death_distance
       FROM kill_events
       WHERE victim_name = '@batata doce' AND distance IS NOT NULL
       GROUP BY weapon;
       """

    cur.execute(query_deaths)
    deaths_df = pd.DataFrame(cur.fetchall(), columns=['Weapon', 'Avg_Death_Distance', 'Var_Death_Distance'])
    cur.close()
    conn.close()
    return deaths_df

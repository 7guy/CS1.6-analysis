import psycopg2
from getpass import getpass
import pandas as pd
from datetime import datetime, timedelta

NICK = '@batata doce'

# Database connection parameters
DB_NAME = "CS1.6"
DB_USER = "postgres"
DB_PASSWORD =  getpass("Enter your PostgreSQL password: ")
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
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
    query = f"""
    SELECT SUM(CASE WHEN killer_name = '{NICK}' THEN 1 ELSE 0 END) AS kill_count,
     SUM(CASE WHEN victim_name = '{NICK}' THEN 1 ELSE 0 END) AS death_count FROM kill_events;
     """
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def kills_by_weapon():
    conn = get_connection()
    cur = conn.cursor()
    query = f"""
    SELECT weapon, COUNT(*) as kills
    FROM kill_events
    WHERE killer_name = '{NICK}'
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
    query = f"""
    SELECT weapon, COUNT(*) as kills
    FROM kill_events
    WHERE victim_name = '{NICK}'
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
    query = f"""
        SELECT distance, COUNT(*) as kills
        FROM kill_events
        WHERE killer_name = '{NICK}'
        GROUP BY distance
        ORDER BY distance;
    """
    # Execute the query and return the data as a DataFrame
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    df_kills = pd.read_sql(query, conn)
    conn.close()
    return df_kills

def deaths_by_distance():
    query = f"""
        SELECT distance, COUNT(*) as deaths
        FROM kill_events
        WHERE victim_name = '{NICK}'
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
    query_kills = f"""
     SELECT weapon, ROUND(AVG(distance)::numeric, 2) as avg_kill_distance, VAR_POP(distance) AS var_kill_distance
     FROM kill_events
     WHERE killer_name = '{NICK}' AND distance IS NOT NULL
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
    query_deaths = f"""
       SELECT weapon, ROUND(AVG(distance)::numeric, 2) as avg_death_distance,VAR_POP(distance) AS var_death_distance
       FROM kill_events
       WHERE victim_name = '{NICK}' AND distance IS NOT NULL
       GROUP BY weapon;
       """

    cur.execute(query_deaths)
    deaths_df = pd.DataFrame(cur.fetchall(), columns=['Weapon', 'Avg_Death_Distance', 'Var_Death_Distance'])
    cur.close()
    conn.close()
    return deaths_df


def total_headshot():
    conn = get_connection()
    cur = conn.cursor()

    # Query to get counts of headshots and non-headshots
    query = f"""
       SELECT 
           COUNT(*) FILTER (WHERE headshot IS TRUE) AS headshot_count,
           COUNT(*) FILTER (WHERE headshot IS FALSE) AS non_headshot_count
       FROM kill_events
       WHERE killer_name = '{NICK}';
       """

    cur.execute(query)
    result = cur.fetchone()
    headshot_count, non_headshot_count = result
    cur.close()
    conn.close()

    return headshot_count, non_headshot_count


def headshot_by_weapon(weapons):
        conn = get_connection()
        cur = conn.cursor()

        query = f"""
        WITH valid_dates AS (
            SELECT DISTINCT DATE(ts) AS date
            FROM kill_events
            WHERE weapon IN {weapons}
              AND headshot IS NOT NULL
              AND killer_name = '{NICK}'
        ),
        headshot_counts AS (
            SELECT DATE(ts) AS date, weapon, 
                   COUNT(*) AS headshot_count
            FROM kill_events
            WHERE weapon IN {weapons}
              AND headshot = TRUE
              AND killer_name = '{NICK}'
            GROUP BY date, weapon
        ),
        total_counts AS (
            SELECT DATE(ts) AS date, weapon, 
                   COUNT(*) AS total_count
            FROM kill_events
            WHERE weapon IN {weapons}
              AND killer_name = '{NICK}'
            GROUP BY date, weapon
        )
        SELECT v.date, t.weapon, 
               COALESCE(h.headshot_count, 0) AS headshot_count,
               COALESCE(t.total_count, 0) AS total_count,
               ROUND(COALESCE(h.headshot_count, 0)::numeric / NULLIF(COALESCE(t.total_count, 0), 0), 2) AS headshot_ratio
        FROM valid_dates v
        LEFT JOIN total_counts t ON v.date = t.date
                                   AND t.weapon IN {weapons}
        LEFT JOIN headshot_counts h ON v.date = h.date
                                      AND h.weapon = t.weapon
        ORDER BY date, weapon;
        """

        cur.execute(query)
        df = pd.DataFrame(cur.fetchall(), columns=['Date', 'Weapon', 'Headshot_Count', 'Total_Count', 'Headshot_Ratio'])
        cur.close()
        conn.close()
        return df


def headshots_by_distance():
    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT distance, COUNT(*) AS headshot_count
        FROM kill_events
        WHERE killer_name = '{NICK}' AND headshot = TRUE AND distance IS NOT NULL
        GROUP BY distance
        ORDER BY distance;
    """

    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()

    # Convert the result to a DataFrame
    headshots_df = pd.DataFrame(result, columns=['Distance', 'Headshot_Count'])

    return headshots_df

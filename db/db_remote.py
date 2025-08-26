import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

@contextmanager
def get_remote_conn():
    conn = psycopg2.connect(os.getenv("DB_REMOTE_URL"))
    try:
        yield conn
    finally:
        conn.close()

def insert_mesures(mesures: list[dict]):
    """
    Insère une liste de mesures dans la base distante PostgreSQL
    mesures = [
        {'id': 1, 'sensor_id': 'A1', 'data_type': 'temp', 'value': 23.4, 'received': '2025-08-25T14:00:00', 'unix_ts': 1692978000},
        ...
    ]
    """
    
    if not mesures:
        return

    with get_remote_conn() as conn:
        cur = conn.cursor()
        query = """
            INSERT INTO mesures (sensor_id, data_type, value, received, unix_ts)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        data = [
            (m['sensor_id'], m['data_type'], m['value'], m['received'], m['unix_ts'])
            for m in mesures
        ]
        cur.executemany(query, data)
        conn.commit()

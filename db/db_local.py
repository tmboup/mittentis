import sqlite3
from contextlib import contextmanager

DB_PATH = "mesures.db"

@contextmanager
def get_local_conn():
    conn = sqlite3.connect(DB_PATH)
    # Permet d'accéder aux résultats comme un dict (row["id"])
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_latest_mesures(limit: int = 100):
    
    """Récupère les mesures locales non envoyées (sent=0)"""
    with get_local_conn() as conn:
        cur = conn.cursor()
        
        # Lire les mesures non envoyées avec une limite
        cur.execute(
            "SELECT id, sensor_id, data_type, value, received, unix_ts "
            "FROM mesures WHERE sent = 0 ORDER BY id ASC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
    
        # Créer une liste de dictionnaires pour JSON
        mesures_list = []
        for row in rows:
            mesures_list.append({
                'id': row["id"],
                'sensor_id': row["sensor_id"],
                'data_type': row["data_type"],
                'value': row["value"],
                'received': row["received"],
                'unix_ts': row["unix_ts"]
            })
    
        return mesures_list


def mark_as_sent(ids):
    """Marque comme envoyées les mesures locales"""
    if not ids:
        return
    with get_local_conn() as conn:
        cur = conn.cursor()
        cur.executemany(
            "UPDATE mesures SET sent = 1 WHERE id = ?",
            [(i,) for i in ids]
        )
        conn.commit()

import sqlite3
import time

# Connexion à la base locale
conn = sqlite3.connect("/opt/vmbase/scripts/mesures.db")
cursor = conn.cursor()

# Exemple de données à insérer
data = [
    (101, 1, 250, 1, 1, int(time.time())),
    (102, 2, 480, 0, 1, int(time.time())),
    (103, 3, 999, 1, 0, int(time.time())),
    (104, 4, 123, 0, 0, int(time.time()))
]

cursor.executemany("""
INSERT INTO mesures (sensor_id, data_type, value, sent, received, unix_ts)
VALUES (?, ?, ?, ?, ?, ?)
""", data)

conn.commit()
conn.close()

print("✅ Données insérées avec succès dans mesures.db")

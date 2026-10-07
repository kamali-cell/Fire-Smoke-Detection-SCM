import sqlite3

connection = sqlite3.connect("fire_smoke.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detection_type TEXT,
    detection_time TEXT,
    status TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")
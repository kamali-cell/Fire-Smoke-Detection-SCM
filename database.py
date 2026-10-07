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

cursor.execute("""
CREATE TABLE IF NOT EXISTS change_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    priority TEXT,
    status TEXT,
    created_time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuration_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT UNIQUE,
    item_type TEXT,
    version TEXT,
    status TEXT,
    owner TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")
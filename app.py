from flask import Flask, send_from_directory, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DATABASE = os.path.join(BASE_DIR, "fire_smoke.db")


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Detection table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        detection_type TEXT,
        detection_time TEXT,
        status TEXT
    )
    """)

    # Change Request table
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

    # Configuration Item table
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

    # Insert 4 Configuration Items
    items = [
        ("Fire Detection Module", "Software", "v1.0", "Active", "SCM Team"),
        ("Smoke Detection Module", "Software", "v1.0", "Active", "SCM Team"),
        ("SCM Dashboard", "Web Module", "v1.0", "Active", "SCM Team"),
        ("Fire-Smoke Database", "Database", "v1.0", "Active", "SCM Team")
    ]

    for item in items:
        cursor.execute("""
        INSERT OR IGNORE INTO configuration_items
        (item_name, item_type, version, status, owner)
        VALUES (?, ?, ?, ?, ?)
        """, item)

    connection.commit()
    connection.close()


create_database()


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/dashboard")
def dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/add-detection/<detection_type>")
def add_detection(detection_type):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO detections
    (detection_type, detection_time, status)
    VALUES (?, ?, ?)
    """, (
        detection_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Detected"
    ))

    connection.commit()
    connection.close()

    return "Detection saved successfully!"


@app.route("/api/detections")
def get_detections():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, detection_type, detection_time, status
    FROM detections
    ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return jsonify([
        {
            "id": r[0],
            "type": r[1],
            "time": r[2],
            "status": r[3]
        }
        for r in records
    ])


@app.route("/add-change-request")
def add_change_request():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO change_requests
    (title, description, priority, status, created_time)
    VALUES (?, ?, ?, ?, ?)
    """, (
        "Update Fire Detection",
        "Improve fire detection sensitivity",
        "High",
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()

    return "Change Request Added Successfully!"


@app.route("/api/change-requests")
def get_change_requests():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, description, priority, status, created_time
    FROM change_requests
    ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return jsonify([
        {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "priority": r[3],
            "status": r[4],
            "time": r[5]
        }
        for r in records
    ])


@app.route("/api/configuration-items")
def get_configuration_items():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, item_name, item_type, version, status, owner
    FROM configuration_items
    ORDER BY id
    """)

    records = cursor.fetchall()
    connection.close()

    return jsonify([
        {
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "version": r[3],
            "status": r[4],
            "owner": r[5]
        }
        for r in records
    ])


if __name__ == "__main__":
    app.run(debug=True)
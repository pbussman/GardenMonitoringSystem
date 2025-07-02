import sqlite3
import json
import os

class DatabaseManager:
    def __init__(self, db_file="aggregator.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zone TEXT,
                type TEXT,
                payload TEXT,
                timestamp DATETIME
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS command_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zone TEXT,
                command TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def store_sensor_reading(self, topic, payload, timestamp):
        _, kind, zone, dtype = topic.split("/")
        self.cursor.execute("""
            INSERT INTO sensor_data (zone, type, payload, timestamp)
            VALUES (?, ?, ?, ?)
        """, (zone, dtype, payload, timestamp))
        self.conn.commit()

    def get_recent_sensor_readings(self, zone, limit=10):
        self.cursor.execute("""
            SELECT type, payload FROM sensor_data
            WHERE zone = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (zone, limit))
        rows = self.cursor.fetchall()
        result = {}
        for t, p in rows:
            try:
                val = json.loads(p)
                result[t] = val["value"]
            except:
                result[t] = p
        return result

    def get_active_zones(self):
        self.cursor.execute("SELECT DISTINCT zone FROM sensor_data")
        return [row[0] for row in self.cursor.fetchall()]

    def queue_command(self, zone, command_obj):
        self.cursor.execute("""
            INSERT INTO command_queue (zone, command, status)
            VALUES (?, ?, ?)
        """, (zone, json.dumps(command_obj), "pending"))
        self.conn.commit()

    def get_pending_commands(self):
        self.cursor.execute("""
            SELECT id, zone, command FROM command_queue
            WHERE status = 'pending'
        """)
        rows = self.cursor.fetchall()
        return [{"id": r[0], "zone": r[1], "command": r[2]} for r in rows]

    def mark_command_complete(self, cmd_id):
        self.cursor.execute("""
            UPDATE command_queue SET status = 'sent' WHERE id = ?
        """, (cmd_id,))
        self.conn.commit()

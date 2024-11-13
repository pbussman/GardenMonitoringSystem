import sqlite3

# SQLite database setup
def setup_database():
    conn = sqlite3.connect('garden_management.db')
    cursor = conn.cursor()
    cursor.executescript('''
        -- Create GardenBeds Table
        CREATE TABLE IF NOT EXISTS GardenBeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            plant TEXT NOT NULL,
            plant_date DATE NOT NULL
        );

        -- Create Maintenance Table
        CREATE TABLE IF NOT EXISTS Maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            garden_bed_id INTEGER,
            activity TEXT NOT NULL,
            date DATE NOT NULL,
            notes TEXT,
            FOREIGN KEY (garden_bed_id) REFERENCES GardenBeds(id)
        );
    ''')
    conn.commit()
    conn.close()

# Set up the database
setup_database()

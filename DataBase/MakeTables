import sqlite3
import paho.mqtt.client as mqtt
import json
import secrets

# SQLite database setup
def setup_database():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.executescript('''
        -- Create Sensors Table
        CREATE TABLE IF NOT EXISTS Sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        );

        -- Create Readings Table
        CREATE TABLE IF NOT EXISTS Readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            air_temperature REAL,
            humidity REAL,
            soil_moisture REAL,
            soil_temperature REAL,
            ambient_light REAL,
            rain REAL,
            FOREIGN KEY (sensor_id) REFERENCES Sensors(id)
        );
    ''')
    conn.commit()
    conn.close()

# Insert sensor reading into the database
def insert_sensor_reading(sensor_data):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Readings (sensor_id, air_temperature, humidity, soil_moisture, soil_temperature, ambient_light, rain)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        sensor_data['sensor_id'],
        sensor_data.get('air_temperature'),
        sensor_data.get('humidity'),
        sensor_data.get('soil_moisture'),
        sensor_data.get('soil_temperature'),
        sensor_data.get('ambient_light'),
        sensor_data.get('rain')
    ))
    
    conn.commit()
    conn.close()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("garden/sensors")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    sensor_data = json.loads(msg.payload.decode())
    insert_sensor_reading(sensor_data)

# MQTT client setup
mqtt_client = mqtt.Client(client_id='DataBase')
mqtt_client.username_pw_set(secrets.MQTT_USERNAME, secrets.MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(secrets.MQTT_SERVER)

# Set up the database
setup_database()

# Run the MQTT client
mqtt_client.loop_forever()

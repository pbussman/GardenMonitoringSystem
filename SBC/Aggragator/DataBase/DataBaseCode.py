import sqlite3
import paho.mqtt.client as mqtt
import json
import requests
from datetime import datetime
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

        -- Create Weather Table
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature_f REAL,
            humidity REAL,
            precipitation_inches REAL,
            heat_index_f REAL,
            will_it_rain INTEGER,
            chance_of_rain REAL,
            sunrise TEXT,
            sunset TEXT,
            wind_speed_mph REAL
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

# Fetch and insert weather data into the database
def fetch_and_insert_weather_data():
    api_key = secrets.WEATHER_API_KEY
    location = secrets.WEATHER_LOCATION
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1'

    response = requests.get(url)
    weather_data = response.json()

    current = weather_data['current']
    forecast = weather_data['forecast']['forecastday'][0]['day']
    astro = weather_data['forecast']['forecastday'][0]['astro']

    temperature_f = current['temp_f']
    humidity = current['humidity']
    precipitation_inches = current['precip_in']
    heat_index_f = current['heatindex_f']
    will_it_rain = forecast['daily_will_it_rain']
    chance_of_rain = forecast['daily_chance_of_rain']
    sunrise = astro['sunrise']
    sunset = astro['sunset']
    wind_speed_mph = current['wind_mph']

    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Weather (timestamp, temperature_f, humidity, precipitation_inches, heat_index_f, will_it_rain, chance_of_rain, sunrise, sunset, wind_speed_mph)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now(), temperature_f, humidity, precipitation_inches, heat_index_f, will_it_rain, chance_of_rain, sunrise, sunset, wind_speed_mph))

    conn.commit()
    conn.close()

    return sunrise, sunset

# Publish sunrise and sunset data to MQTT
def publish_sunrise_sunset(client, sunrise, sunset):
    data = {
        'sunrise': sunrise,
        'sunset': sunset
    }
    client.publish("garden/sunrise_sunset", json.dumps(data))

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("garden/sensors")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    sensor_data = json.loads(msg.payload.decode())
    insert_sensor_reading(sensor_data)
    sunrise, sunset = fetch_and_insert_weather_data()
    publish_sunrise_sunset(client, sunrise, sunset)

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

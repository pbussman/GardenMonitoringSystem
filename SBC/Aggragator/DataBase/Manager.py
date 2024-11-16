import sqlite3
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='sensor_data.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.executescript('''
                -- SQL script to create tables
            ''')
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database setup error: {e}")
        finally:
            conn.close()

    def insert_sensor_reading(self, sensor_data):
        try:
            conn = sqlite3.connect(self.db_name)
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
        except sqlite3.Error as e:
            logging.error(f"Insert sensor reading error: {e}")
        finally:
            conn.close()

    def insert_float_sensor_reading(self, barrel, sensor_data):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO FloatSensorReadings (barrel, sensor_1, sensor_2, sensor_3, sensor_4)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                barrel,
                sensor_data[0],
                sensor_data[1],
                sensor_data[2],
                sensor_data[3]
            ))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Insert float sensor reading error: {e}")
        finally:
            conn.close()

    def insert_weather_data(self, weather_data):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Weather (timestamp, temperature_f, humidity, precipitation_inches, heat_index_f, will_it_rain, chance_of_rain, sunrise, sunset, wind_speed_mph)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                weather_data['temperature_f'],
                weather_data['humidity'],
                weather_data['precipitation_inches'],
                weather_data['heat_index_f'],
                weather_data['will_it_rain'],
                weather_data['chance_of_rain'],
                weather_data['sunrise'],
                weather_data['sunset'],
                weather_data['wind_speed_mph']
            ))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Insert weather data error: {e}")
        finally:
            conn.close()

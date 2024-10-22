import paho.mqtt.client as mqtt
import psycopg2
import json

# MQTT settings
broker = "localhost"
port = 1883
topic = "garden/sensors"

# Database settings
db_host = "192.168.1.100"  # IP address of the central controller
db_name = "garden_db"
db_user = "your_db_user"
db_password = "your_db_password"

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# MQTT callback function
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    temp_f = data['temperature_f']
    humidity = data['humidity']
    rain_status = data['rain_status']
    soil_moisture = data['soil_moisture_percentage']
    soil_temp_f = data['soil_temperature_f']
    
    # Insert data into the database
    cur.execute(
        "INSERT INTO sensor_data (temperature_f, humidity, rain_status, soil_moisture, soil_temperature_f) VALUES (%s, %s, %s, %s, %s)",
        (temp_f, humidity, rain_status, soil_moisture, soil_temp_f)
    )
    conn.commit()

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)
client.loop_forever()

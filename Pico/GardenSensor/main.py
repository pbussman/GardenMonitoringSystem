from communications import wifi
from communications import mqtt_client
import utime
from machine import Pin, deepsleep
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
from veml7700 import VEML7700  # Import the VEML7700 class
import json
from datetime import datetime

# Initialize MQTT client
mqtt_client = mqtt_client.MQTTClient(
    client_id='GardenSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='garden/sensors'
)
mqtt_client.connect()

# Define the sensors for this platform
dht22 = DHT22Sensor(pin_number=22)
rain_sensor = RainSensor(power_pin=27, data_pin=21)
soil_moisture_sensor = SoilMoistureSensor(power_pin=18, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)
ambient_light_sensor = VEML7700(sda_pin=0, scl_pin=1, power_pin=2)  # Define the ambient light sensor

# Function to read and publish sensor data
def read_sensors(sensor_id):
    dht22_data = dht22.read()
    rain_data = rain_sensor.read()
    soil_moisture_data = soil_moisture_sensor.read()
    soil_temp_data = soil_temp_sensor.read()
    ambient_light = ambient_light_sensor.read_lux()  # Read ambient light data

    sensor_data = {
        "sensor_id": sensor_id,
        "air_temperature": dht22_data['temperature_f'] if dht22_data else None,
        "humidity": dht22_data['humidity'] if dht22_data else None,
        "soil_moisture": soil_moisture_data['moisture_percentage'] if soil_moisture_data else None,
        "soil_temperature": soil_temp_data['temperature_f'] if soil_temp_data else None,
        "ambient_light": ambient_light,  # Include ambient light data
        "rain": rain_data if rain_data else None
    }

    mqtt_client.publish(json.dumps(sensor_data))

# Function to check if it's daytime
def is_daytime(sunrise, sunset):
    now = datetime.now().time()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunset_time = datetime.strptime(sunset, '%I:%M %p').time()
    return sunrise_time <= now <= sunset_time

# Main function
wlan = wifi.connect_wifi()
while True:
    mqtt_client.client.check_msg()  # Check for new MQTT messages
    if wlan.isconnected() and mqtt_client.sunrise and mqtt_client.sunset:
        if is_daytime(mqtt_client.sunrise, mqtt_client.sunset):
            sensor_id = read_dip_switch()
            read_sensors(sensor_id)
            utime.sleep(600)  # Pause for 10 minutes (600 seconds)
        else:
            print("It's night time. Going to sleep.")
            deepsleep(3600000)  # Sleep for 1 hour (3600000 milliseconds) during the night
    else:
        print("Reconnecting to WiFi...")
        wlan = wifi.connect_wifi()

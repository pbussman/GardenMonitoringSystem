import utime
import logging
from machine import Pin, deepsleep
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
from veml7700 import VEML7700
from wifi import connect_wifi, reconnect_wifi
from mqtt_client import MQTTClient
from datetime import datetime, timedelta
from bed_identifier import read_bed_id  # DIP switch logic

# 🌐 Load secrets from SD card
try:
    import secrets
    logging.info(f"WiFi SSID: {secrets.SSID}")
except ImportError:
    logging.error("Failed to load secrets.py from SD card")
    raise SystemExit("Critical error: secrets.py not found on SD card")

# 📝 Initialize logging
log_file_path = "/sd/garden_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logging.info("Logging initialized")

# 📡 Connect WiFi
wlan = connect_wifi(secrets)

# 🔗 Initialize MQTT
mqtt_client = MQTTClient(
    client_id='GardenSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='garden/sensors'
)
mqtt_client.connect(secrets.MQTT_USERNAME, secrets.MQTT_PASSWORD)

# 🌱 Initialize sensors
pin = Pin("LED", Pin.OUT)
dht22 = DHT22Sensor(pin_number=17, power_pin=16)
rain_sensor = RainSensor(power_pin=21, data_pin=20)
soil_moisture_sensor = SoilMoistureSensor(power_pin=22, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)
ambient_light_sensor = VEML7700(sda_pin=0, scl_pin=1, power_pin=2)

# ☀️ Daylight logic
def is_daytime(sunrise, sunset):
    now = datetime.now().time()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunset_time = datetime.strptime(sunset, '%I:%M %p').time()
    return sunrise_time <= now <= sunset_time

def calculate_sleep_duration(sunrise):
    now = datetime.now()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunrise_datetime = datetime.combine(now.date(), sunrise_time)
    if now.time() > sunrise_time:
        sunrise_datetime = datetime.combine(now.date() + timedelta(days=1), sunrise_time)
    return (sunrise_datetime - now).total_seconds()

# 📊 Sensor reading and publishing
def read_sensors(sensor_id):
    try:
        dht22_data = dht22.read()
        rain_data = rain_sensor.read()
        soil_moisture_data = soil_moisture_sensor.read()
        soil_temp_data = soil_temp_sensor.read()
        ambient_light = ambient_light_sensor.read_lux()

        sensor_data = {
            "sensor_id": sensor_id,
            "air_temperature": dht22_data.get('temperature_f') if dht22_data else None,
            "humidity": dht22_data.get('humidity') if dht22_data else None,
            "soil_moisture": soil_moisture_data.get('moisture_percentage') if soil_moisture_data else None,
            "soil_temperature": soil_temp_data.get('temperature_f') if soil_temp_data else None,
            "ambient_light": ambient_light,
            "rain": rain_data if rain_data else None
        }

        sensor_data = {k: v for k, v in sensor_data.items() if v is not None}
        mqtt_client.publish(sensor_data)
        logging.info("Sensor data published: %s", sensor_data)

    except Exception as e:
        logging.error(f"Error reading sensors: {e}")

# 🔁 Main loop
while True:
    try:
        mqtt_client.client.check_msg()
        if wlan.isconnected():
            if mqtt_client.sunrise and mqtt_client.sunset:
                if not is_daytime(mqtt_client.sunrise, mqtt_client.sunset):
                    logging.info("It's nighttime. Entering deep sleep.")
                    sleep_duration = calculate_sleep_duration(mqtt_client.sunrise)
                    deepsleep(int(sleep_duration * 1000))

            sensor_id = read_bed_id()
            logging.info(f"Garden Bed ID: {sensor_id}")
            read_sensors(sensor_id)
            utime.sleep(600)  # 10-minute interval

        else:
            logging.warning("WiFi disconnected. Attempting reconnection...")
            wlan = reconnect_wifi(secrets)

    except Exception as e:
        logging.error(f"Error in main loop: {e}")

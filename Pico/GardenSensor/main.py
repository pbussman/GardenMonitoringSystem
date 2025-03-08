import os
import sys
import utime
import json
import network
import logging
from sdcard import SDCard
from machine import Pin, SPI, deepsleep
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
from veml7700 import VEML7700
import umqtt.simple as mqtt
from datetime import datetime, timedelta

# SD Card Initialization
def init_sd():
    """Initialize and mount the SD card."""
    spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
    cs = Pin(5, Pin.OUT)
    sd = SDCard(spi, cs)
    os.mount(sd, "/sd")
    print("SD card initialized and mounted!")
    
    # Add SD card path to system path for dynamic imports
    sys.path.append("/sd")
    return "/sd"

# Configure Logging to SD Card
def configure_logging(sd_path):
    """Redirect logging to an SD card file."""
    log_file_path = f"{sd_path}/garden_log.txt"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),  # Log to file on SD card
            logging.StreamHandler()             # Also log to console
        ]
    )
    logging.info("Logging setup complete on SD card")

# Connect to WiFi
def connect_wifi():
    """Connect to WiFi using credentials from secrets.py."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        logging.info("Waiting for WiFi connection...")
        utime.sleep(1)

    if wlan.isconnected():
        logging.info("WiFi connected: %s", wlan.ifconfig()[0])
        pin.value(1)  # Turn on onboard LED to indicate success
    else:
        logging.error("Failed to connect to WiFi")
        pin.value(0)  # Turn off onboard LED
    return wlan

# MQTT Client Class
class MQTTClient:
    def __init__(self, client_id, mqtt_server, topic_pub):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.topic_pub = topic_pub
        self.client = mqtt.MQTTClient(self.client_id, self.mqtt_server)
        self.sunrise = None
        self.sunset = None

    def connect(self, username, password):
        try:
            self.client.connect(user=username, password=password)
            logging.info('Connected to MQTT Broker')
            self.client.subscribe("garden/sunrise_sunset")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT Broker: {e}")

    def publish(self, message):
        try:
            self.client.publish(self.topic_pub, message)
            logging.info('Published: %s', message)
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")

    def on_message(self, topic, msg):
        if topic == b'garden/sunrise_sunset':
            data = json.loads(msg)
            self.sunrise = data['sunrise']
            self.sunset = data['sunset']
            logging.info(f"Received sunrise: {self.sunrise}, sunset: {self.sunset}")

# Read Sensor Data
def read_sensors(sensor_id):
    try:
        dht22_data = dht22.read()
        rain_data = rain_sensor.read()
        soil_moisture_data = soil_moisture_sensor.read()
        soil_temp_data = soil_temp_sensor.read()
        ambient_light = ambient_light_sensor.read_lux()

        sensor_data = {
            "sensor_id": sensor_id,
            "air_temperature": dht22_data['temperature_f'] if dht22_data else None,
            "humidity": dht22_data['humidity'] if dht22_data else None,
            "soil_moisture": soil_moisture_data['moisture_percentage'] if soil_moisture_data else None,
            "soil_temperature": soil_temp_data['temperature_f'] if soil_temp_data else None,
            "ambient_light": ambient_light,
            "rain": rain_data if rain_data else None
        }

        mqtt_client.publish(json.dumps(sensor_data))
        logging.info("Sensor data published: %s", sensor_data)
    except Exception as e:
        logging.error("Error reading sensors: %s", e)

# Main Setup
sd_path = init_sd()  # Initialize SD card

# Import secrets from SD card
try:
    import secrets
    logging.info(f"WiFi SSID: {secrets.SSID}")
except ImportError:
    logging.error("Failed to load secrets.py from SD card")
    raise SystemExit("Critical error: secrets.py not found on SD card")

configure_logging(sd_path)  # Configure logging to SD card

# Initialize components
pin = Pin("LED", Pin.OUT)
wlan = connect_wifi()
mqtt_client = MQTTClient(
    client_id='GardenSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='garden/sensors'
)
mqtt_client.connect(secrets.MQTT_USERNAME, secrets.MQTT_PASSWORD)

# Define sensors
dht22 = DHT22Sensor(pin_number=17, power_pin=16)
rain_sensor = RainSensor(power_pin=21, data_pin=20)
soil_moisture_sensor = SoilMoistureSensor(power_pin=22, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)
ambient_light_sensor = VEML7700(sda_pin=0, scl_pin=1, power_pin=2)

# Main loop
while True:
    try:
        mqtt_client.client.check_msg()
        if wlan.isconnected():
            sensor_id = 0  # Assuming sensor ID logic to be added
            read_sensors(sensor_id)
            utime.sleep(600)  # Sleep for 10 minutes before the next reading
        else:
            logging.warning("Reconnecting to WiFi...")
            wlan = connect_wifi()
    except Exception as e:
        logging.error("Error in main loop: %s", e)

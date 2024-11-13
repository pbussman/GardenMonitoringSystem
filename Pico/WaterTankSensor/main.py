import utime
import json
import network
from machine import Pin, deepsleep
import umqtt.simple as mqtt
import secrets
from float_sensor import FloatSensor  # Import the FloatSensor class
from datetime import datetime, timedelta

# Initialize onboard LED for status
pin = Pin("LED", Pin.OUT)

# Function to connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for WiFi connection...")
        utime.sleep(1)

    if wlan.isconnected():
        print("WiFi connection made:", wlan.isconnected())
        print("IP Address:", wlan.ifconfig()[0])
        pin.value(1)  # Turn on onboard LED
    else:
        print("Failed to connect to WiFi")
        pin.value(0)  # Turn off onboard LED

    return wlan

# MQTT client class
class MQTTClient:
    def __init__(self, client_id, mqtt_server, topic_pub):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.topic_pub = topic_pub
        self.client = mqtt.MQTTClient(self.client_id, self.mqtt_server)
        self.sunrise = None
        self.sunset = None

    def connect(self):
        self.client.connect(user=secrets.MQTT_USERNAME, password=secrets.MQTT_PASSWORD)
        print('Connected to MQTT Broker')
        self.client.subscribe("garden/sunrise_sunset")

    def publish(self, message):
        self.client.publish(self.topic_pub, message)
        print('Published:', message)

    def on_message(self, topic, msg):
        if topic == b'garden/sunrise_sunset':
            data = json.loads(msg)
            self.sunrise = data['sunrise']
            self.sunset = data['sunset']
            print(f"Received sunrise: {self.sunrise}, sunset: {self.sunset}")

# Initialize MQTT client
mqtt_client = MQTTClient(
    client_id='WaterTankSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='water_tank/sensors'
)
mqtt_client.connect()
mqtt_client.client.set_callback(mqtt_client.on_message)

# Define the float sensors
float_sensor_1 = FloatSensor(pin_number=22)
float_sensor_2 = FloatSensor(pin_number=23)  # Add more sensors as needed

# Function to read and publish float sensor data
def read_sensors():
    try:
        float_sensor_1_state = float_sensor_1.read()
        float_sensor_2_state = float_sensor_2.read()

        sensor_data = {
            "float_sensor_1": float_sensor_1_state,
            "float_sensor_2": float_sensor_2_state
        }

        mqtt_client.publish(json.dumps(sensor_data))
    except Exception as e:
        print(f"Failed to read sensors or publish data: {e}")

# Function to check if it's daytime
def is_daytime(sunrise, sunset):
    now = datetime.now().time()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunset_time = datetime.strptime(sunset, '%I:%M %p').time()
    return sunrise_time <= now <= sunset_time

# Function to calculate sleep duration until sunrise
def calculate_sleep_duration(sunrise):
    now = datetime.now()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunrise_datetime = datetime.combine(now.date(), sunrise_time)
    if now.time() > sunrise_time:
        sunrise_datetime = datetime.combine(now.date() + timedelta(days=1), sunrise_time)
    sleep_duration = (sunrise_datetime - now).total_seconds()
    return sleep_duration

# Main function
wlan = connect_wifi()
while True:
    mqtt_client.client.check_msg()  # Check for new MQTT messages
    if wlan.isconnected() and mqtt_client.sunrise and mqtt_client.sunset:
        if is_daytime(mqtt_client.sunrise, mqtt_client.sunset):
            read_sensors()
            utime.sleep(600)  # Pause for 10 minutes (600 seconds)
        else:
            print("It's night time. Going to sleep.")
            sleep_duration = calculate_sleep_duration(mqtt_client.sunrise)
            deepsleep(int(sleep_duration * 1000))  # Sleep until sunrise
    else:
        print("Reconnecting to WiFi...")
        wlan = connect_wifi()

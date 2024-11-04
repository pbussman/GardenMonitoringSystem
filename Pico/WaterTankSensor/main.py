import utime
import json
import network
from machine import Pin
import umqtt.simple as mqtt
import secrets
from float_sensor import FloatSensor  # Import the FloatSensor class

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

    def connect(self):
        self.client.connect(user=secrets.MQTT_USERNAME, password=secrets.MQTT_PASSWORD)
        print('Connected to MQTT Broker')

    def publish(self, message):
        self.client.publish(self.topic_pub, message)
        print('Published:', message)

# Initialize MQTT client
mqtt_client = MQTTClient(
    client_id='WaterTankSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='water_tank/sensors'
)
mqtt_client.connect()

# Define the float sensors
float_sensor_1 = FloatSensor(pin_number=22)
float_sensor_2 = FloatSensor(pin_number=23)  # Add more sensors as needed

# Function to read and publish float sensor data
def read_sensors():
    float_sensor_1_state = float_sensor_1.read()
    float_sensor_2_state = float_sensor_2.read()

    sensor_data = {
        "float_sensor_1": float_sensor_1_state,
        "float_sensor_2": float_sensor_2_state
    }

    mqtt_client.publish(json.dumps(sensor_data))

# Main function
wlan = connect_wifi()
while True:
    if wlan.isconnected():
        read_sensors()
        utime.sleep(600)  # Pause for 10 minutes (600 seconds)
    else:
        print("Reconnecting to WiFi...")
        wlan = connect_wifi()

import utime
import json
import network
from machine import Pin
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
import umqtt.simple as mqtt
import secrets

# Initialize onboard LED for status
pin = Pin("LED", Pin.OUT)

# Define the pins connected to the DIP switch
dip_pins = [Pin(2, Pin.IN), Pin(3, Pin.IN), Pin(4, Pin.IN), Pin(5, Pin.IN)]

def read_dip_switch():
    sensor_id = 0
    for i, pin in enumerate(dip_pins):
        sensor_id |= (pin.value() << i)
    return sensor_id

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

# Function to read and publish sensor data
def read_sensors(sensor_id):
    dht22_data = dht22.read()
    rain_data = rain_sensor.read()
    soil_moisture_data = soil_moisture_sensor.read()
    soil_temp_data = soil_temp_sensor.read()

    sensor_data = {
        "sensor_id": sensor_id,
        "air_temperature": dht22_data['temperature_f'] if dht22_data else None,
        "humidity": dht22_data['humidity'] if dht22_data else None,
        "soil_moisture": soil_moisture_data['moisture_percentage'] if soil_moisture_data else None,
        "soil_temperature": soil_temp_data['temperature_f'] if soil_temp_data else None,
        "ambient_light": None,  # Assuming you have a way to get this data
        "rain": rain_data if rain_data else None
    }

    mqtt_client.publish(json.dumps(sensor_data))

# Main function
wlan = connect_wifi()
while True:
    if wlan.isconnected():
        sensor_id = read_dip_switch()
        read_sensors(sensor_id)
        utime.sleep(600)  # Pause for 10 minutes (600 seconds)
    else:
        print("Reconnecting to WiFi...")
        wlan = connect_wifi()

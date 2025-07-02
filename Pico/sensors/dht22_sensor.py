import dht
import machine
import network
import time
import json
from umqtt.simple import MQTTClient

# Configuration
MQTT_BROKER = "your.mqtt.broker"
SENSOR_NAME = "bed1"
CLIENT_ID = "dht22_" + SENSOR_NAME

pin = machine.Pin(15)
sensor = dht.DHT22(pin)

def connect_wifi():
    # Your existing Wi-Fi logic here
    pass

def read_and_publish():
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()

        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.connect()

        client.publish(f"garden/sensor/{SENSOR_NAME}/air_temperature", json.dumps({
            "value": temp,
            "unit": "°C"
        }))
        client.publish(f"garden/sensor/{SENSOR_NAME}/humidity", json.dumps({
            "value": humidity,
            "unit": "%"
        }))

        client.disconnect()
    except Exception as e:
        print("Failed to read/publish:", e)

connect_wifi()
while True:
    read_and_publish()
    time.sleep(300)  # every 5 mins

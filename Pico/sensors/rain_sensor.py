import machine, time, json
from umqtt.simple import MQTTClient

MQTT_BROKER = "your.mqtt.broker"
SENSOR_NAME = "roof1"
CLIENT_ID = "rain_" + SENSOR_NAME

pin = machine.ADC(28)

def read_and_publish():
    value = pin.read_u16()  # Range varies by sensor
    rain_detected = value < 30000

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()

    client.publish(f"garden/sensor/{SENSOR_NAME}/rain_detected", json.dumps({
        "value": rain_detected
    }))

    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)

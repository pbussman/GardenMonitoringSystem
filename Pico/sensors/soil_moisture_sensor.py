import machine, time, json
from umqtt.simple import MQTTClient

MQTT_BROKER = "your.mqtt.broker"
SENSOR_NAME = "bed1"
CLIENT_ID = "moisture_" + SENSOR_NAME

adc = machine.ADC(26)

def read_and_publish():
    raw = adc.read_u16()
    moisture = round((65535 - raw) / 655.35, 1)  # Convert to pseudo-percent

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()

    client.publish(f"garden/sensor/{SENSOR_NAME}/soil_moisture", json.dumps({
        "value": moisture,
        "unit": "%"
    }))

    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)

import machine, time, network, json
from umqtt.simple import MQTTClient

SENSOR_NAME = "tank1"
MQTT_BROKER = "your.mqtt.broker"
CLIENT_ID = "float_" + SENSOR_NAME

pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def connect_wifi():
    pass  # your existing Wi-Fi logic

def check_and_publish():
    state = pin.value()  # 0 = submerged
    full = state == 0

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()

    client.publish(f"garden/sensor/{SENSOR_NAME}/water_level", json.dumps({
        "value": "full" if full else "low"
    }))
    client.disconnect()

connect_wifi()
while True:
    check_and_publish()
    time.sleep(300)

import machine, time, json
from umqtt.simple import MQTTClient

MQTT_BROKER = "your.mqtt.broker"
SENSOR_NAME = "bed1"
CLIENT_ID = "soiltemp_" + SENSOR_NAME

adc = machine.ADC(27)

def read_and_publish():
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535
    temp_c = (voltage - 0.5) * 100  # Adjust for your sensor model

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()

    client.publish(f"garden/sensor/{SENSOR_NAME}/soil_temperature", json.dumps({
        "value": temp_c,
        "unit": "°C"
    }))

    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)

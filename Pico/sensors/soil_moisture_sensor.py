from config import load_config
from umqtt.simple import MQTTClient
import machine, time, json

cfg = load_config()
adc = machine.ADC(26)

def read_and_publish():
    raw = adc.read_u16()
    moisture = round((65535 - raw) / 655.35, 1)

    client = MQTTClient(
        client_id=cfg["client_id"],
        server=cfg["mqtt_broker"],
        port=cfg["mqtt_port"],
        user=cfg["username"],
        password=cfg["password"]
    )

    client.connect()
    client.publish(f"garden/sensor/{cfg['sensor_name']}/soil_moisture", json.dumps({
        "value": moisture,
        "unit": "%"
    }))
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)

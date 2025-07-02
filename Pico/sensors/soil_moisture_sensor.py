from config import load_config
from umqtt.simple import MQTTClient
import machine, time, json

cfg = load_config()
adc = machine.ADC(27)

def read_and_publish():
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535
    temp_c = (voltage - 0.5) * 100  # Adjust for your sensor’s calibration

    client = MQTTClient(
        client_id=cfg["client_id"],
        server=cfg["mqtt_broker"],
        port=cfg["mqtt_port"],
        user=cfg["username"],
        password=cfg["password"]
    )

    client.connect()
    client.publish(f"garden/sensor/{cfg['sensor_name']}/soil_temperature", json.dumps({
        "value": round(temp_c, 1),
        "unit": "°C"
    }))
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)

from config import load_config
from umqtt.simple import MQTTClient
import machine, time, json
import dht

cfg = load_config()
sensor = dht.DHT22(machine.Pin(15))

def read_and_publish():
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()

        client = MQTTClient(
            client_id=cfg["client_id"],
            server=cfg["mqtt_broker"],
            port=cfg["mqtt_port"],
            user=cfg["username"],
            password=cfg["password"]
        )

        client.connect()
        client.publish(f"garden/sensor/{cfg['sensor_name']}/air_temperature", json.dumps({
            "value": temp,
            "unit": "°C"
        }))
        client.publish(f"garden/sensor/{cfg['sensor_name']}/humidity", json.dumps({
            "value": humidity,
            "unit": "%"
        }))
        client.disconnect()

    except Exception as e:
        print("Sensor error:", e)

while True:
    read_and_publish()
    time.sleep(300)

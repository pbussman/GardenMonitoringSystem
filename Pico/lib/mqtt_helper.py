# mqtt_helper.py

from umqtt.simple import MQTTClient

def connect_mqtt(cfg):
    return MQTTClient(
        client_id=cfg["client_id"],
        server=cfg["mqtt_broker"],
        port=cfg["mqtt_port"],
        user=cfg["username"],
        password=cfg["password"]
    )

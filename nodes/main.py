import sys
sys.path.append("/lib")

from config import load_config
from mqtt_helper import connect_mqtt
from ota_updater import fetch_remote_version, update_if_needed

import machine, time, json

# OTA check
info = fetch_remote_version("http://<pi-ip>:8000/remote_version.json")
if info:
    update_if_needed(info)

cfg = load_config()
name = cfg["sensor_name"]

# Initialize relays
relays = {
    alias: machine.Pin(pin, machine.Pin.OUT)
    for alias, pin in cfg.get("relays", {}).items()
}

# Optional flow sensors
sensors = {
    alias: machine.Pin(pin, machine.Pin.IN)
    for alias, pin in cfg.get("flow_sensors", {}).items()
}

# Relay control (active LOW)
def set_relay(alias, state):
    if alias in relays:
        relays[alias].value(0 if state else 1)

def get_relay_states():
    return {
        alias: "on" if pin.value() == 0 else "off"
        for alias, pin in relays.items()
    }

def get_flow_status():
    return {
        f"{alias}_flow": "yes" if pin.value() == 0 else "no"
        for alias, pin in sensors.items()
    }

# MQTT command handler
def message_callback(topic, msg):
    try:
        data = json.loads(msg)
        alias = data.get("channel")     # Now uses alias instead of number
        state = data.get("state")
        if alias in relays and state in ["on", "off"]:
            set_relay(alias, state == "on")
            print(f"Relay {alias} set to {state}")
    except Exception as e:
        print("Command error:", e)

# MQTT setup
client = connect_mqtt(cfg)
client.set_callback(message_callback)
client.connect()
client.subscribe(f"garden/command/{name}/relay")

def publish_status():
    status = {**get_relay_states(), **get_flow_status()}
    topic = f"garden/status/{name}/relay"
    client.publish(topic, json.dumps(status))

print(f"[{name}] Node online.")

# Main loop
while True:
    try:
        client.check_msg()
        publish_status()
        time.sleep(10)
    except Exception as e:
        print("Loop error:", e)
        time.sleep(10)

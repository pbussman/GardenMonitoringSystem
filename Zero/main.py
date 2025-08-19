# main.py

import time
from config_loader import Config
from drivers import SourcePumpUnit
from mqtt_client import MQTTClient

def main():
    cfg = Config("config.yaml")
    unit = SourcePumpUnit(cfg)
    mqc = MQTTClient(
        broker=cfg.mqtt['broker'],
        port=cfg.mqtt['port'],
        client_id=cfg.mqtt['client_id'],
        tls_conf=cfg.mqtt.get('tls')
    )

    # Register valve topics
    for name, vcfg in cfg.valves.items():
        topic = vcfg['topic']
        mqc.register(topic, lambda payload, n=name: on_valve_cmd(n, payload, unit))

    # Register pump topic
    pump_topic = cfg.pump['pressure']['topic']
    mqc.register(pump_topic, lambda p: unit.set_pump(p.lower()=="on"))

    # Heartbeat loop
    heartbeat_topic = cfg.general['heartbeat_topic']
    interval = cfg.general['heartbeat_interval']
    try:
        while True:
            status = {
                name: vc.current_position for name, vc in unit.valves.items()
            }
            status['pump'] = unit.pump.state
            mqc.publish(heartbeat_topic, status)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        unit.pump.off()
        for vc in unit.valves.values():
            vc.release()     # clean up GPIO

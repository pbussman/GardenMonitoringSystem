# Zero/main.py

import time
from config_loader import Config
from drivers import SourcePumpUnit
from mqtt_client import MQTTClient
from Zero.logger import setup_logger

logger = setup_logger()

def on_valve_cmd(name, payload, unit):
    try:
        position = int(payload)
        logger.info("Received command: move valve '%s' to %d°", name, position)
        unit.move_valve(name, position)
    except Exception as e:
        logger.error("Failed to move valve '%s': %s", name, str(e))

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
    mqc.register(pump_topic, lambda p: unit.set_pump(p.lower() == "on"))

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
            logger.debug("Published heartbeat: %s", status)
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully")
    finally:
        unit.pump.off()
        for vc in unit.valves.values():
            vc.release()
        logger.info("GPIO cleanup complete")


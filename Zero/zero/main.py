from location_identifier import read_dip_config, parse_config
from config_loader import Config
from mqtt_client import MQTTClient
from drivers.source_pump_unit import SourcePumpUnit
from logger import setup_logger
import time

logger = setup_logger()

def main():
    dip_config = read_dip_config()
    location_id, float_enabled = parse_config(dip_config)
    logger.info(f"Location ID: {location_id}, Float Sensors Enabled: {float_enabled}")

    cfg = Config("config.yaml")

    if location_id == 0:
        cfg.valves = cfg.location_1['valves']
        cfg.pump = None
        cfg.float_sensors_enabled = False
    elif location_id == 1:
        cfg.valves = cfg.location_2['valves']
        cfg.pump = cfg.location_2['pump']
        cfg.float_sensors_enabled = float_enabled
    else:
        logger.warning("Unknown location ID. Entering safe mode.")
        return

    unit = SourcePumpUnit(cfg)
    mqc = MQTTClient(cfg.mqtt)

    unit.register_topics(mqc)

    try:
        while True:
            mqc.check_messages()
            mqc.publish(cfg.general['heartbeat_topic'], unit.status())
            time.sleep(cfg.general['heartbeat_interval'])
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully")
        unit.shutdown()

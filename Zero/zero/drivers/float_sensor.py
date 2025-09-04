# drivers/float_sensor.py

from machine import Pin
import logging

logger = logging.getLogger("FloatSensor")

class FloatSensor:
    def __init__(self, config):
        self.sensors = {}
        for name, pin_num in config.items():
            self.sensors[name] = Pin(pin_num, Pin.IN, Pin.PULL_UP)
            logger.info(f"Float sensor '{name}' initialized on pin {pin_num}")

    def read(self):
        readings = {}
        for name, pin in self.sensors.items():
            # Float sensor ON = LOW (water present)
            readings[name] = not pin.value()
        logger.debug(f"Float sensor readings: {readings}")
        return readings

# drivers/pump_controller.py

from machine import Pin
import logging

logger = logging.getLogger("PumpController")

class PumpController:
    def __init__(self, config):
        self.pin = Pin(config["pressure"]["pin"], Pin.OUT)
        self.topic = config["pressure"]["topic"]
        self.state = "off"
        self.off()

    def on(self):
        self.pin.value(1)
        self.state = "on"
        logger.info("Pump turned ON")

    def off(self):
        self.pin.value(0)
        self.state = "off"
        logger.info("Pump turned OFF")

    def set(self, state: bool):
        if state:
            self.on()
        else:
            self.off()

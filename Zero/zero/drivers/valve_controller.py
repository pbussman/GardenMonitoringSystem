# drivers/valve_controller.py

from machine import Pin
import logging

logger = logging.getLogger("ValveController")

class ValveController:
    def __init__(self, config):
        self.name = config.get("name", "unnamed_valve")
        self.pin = Pin(config["pin"], Pin.OUT)
        self.topic = config["topic"]
        self.current_position = "off"
        self.off()

    def on(self):
        self.pin.value(1)
        self.current_position = "on"
        logger.info(f"{self.name} turned ON")

    def off(self):
        self.pin.value(0)
        self.current_position = "off"
        logger.info(f"{self.name} turned OFF")

    def handle(self, payload):
        if payload.lower() == "on":
            self.on()
        elif payload.lower() == "off":
            self.off()
        else:
            logger.warning(f"Unknown command for {self.name}: {payload}")

    def release(self):
        self.off()
        logger.info(f"{self.name} released")

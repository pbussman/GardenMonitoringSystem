# Zero/drivers.py

import RPi.GPIO as GPIO
from SBC.valve_controller import ValveController
from SBC.pump_controller import PumpController
from Zero.logger import setup_logger

logger = setup_logger()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class SourcePumpUnit:
    def __init__(self, cfg):
        self.valves = {}
        for name, vcfg in cfg.valves.items():
            vc = ValveController(
                coil_a_pin=vcfg['coil_a_pin'],
                coil_b_pin=vcfg['coil_b_pin'],
                eot_a_pin=vcfg['eot_a_pin'],
                eot_b_pin=vcfg['eot_b_pin'],
                timeout=cfg.general['valve_move_timeout']
            )
            self.valves[name] = vc
            logger.info("Initialized valve controller: %s", name)

        pump_pin = cfg.pump['pressure']['pin']
        self.pump = PumpController(pin=pump_pin)
        logger.info("Initialized pressure pump on GPIO %d", pump_pin)

    def move_valve(self, name, position_deg):
        if name not in self.valves:
            logger.error("Unknown valve: %s", name)
            return
        logger.info("Moving valve '%s' to %d°", name, position_deg)
        self.valves[name].move_to(position_deg)

    def set_pump(self, state: bool):
        logger.info("Setting pressure pump: %s", "ON" if state else "OFF")
        if state:
            self.pump.on()
        else:
            self.pump.off()

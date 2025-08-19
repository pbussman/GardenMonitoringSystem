# drivers.py

import RPi.GPIO as GPIO
import time
from SBC.valve_controller import ValveController  # reuse your GitHub code
from SBC.pump_controller import PumpController    # reuse your GitHub code

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class SourcePumpUnit:
    def __init__(self, cfg):
        # Valve controllers
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

        # Pressure pump
        pump_pin = cfg.pump['pressure']['pin']
        self.pump = PumpController(pin=pump_pin)

    def move_valve(self, name, position_deg):
        """Position in {0, 90, 180} degrees."""
        if name not in self.valves:
            raise KeyError(f"Unknown valve: {name}")
        self.valves[name].move_to(position_deg)

    def set_pump(self, state: bool):
        if state:
            self.pump.on()
        else:
            self.pump.off()

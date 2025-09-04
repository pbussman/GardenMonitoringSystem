from drivers.valve_controller import ValveController
from drivers.pump_controller import PumpController
from drivers.float_sensor import FloatSensor

class SourcePumpUnit:
    def __init__(self, cfg):
        self.valves = {name: ValveController(vcfg) for name, vcfg in cfg.valves.items()}
        self.pump = PumpController(cfg.pump) if cfg.pump else None
        self.float_sensors = FloatSensor(cfg.float_sensors) if cfg.float_sensors_enabled else None

    def register_topics(self, mqc):
        for name, valve in self.valves.items():
            mqc.register(valve.topic, lambda payload, v=valve: v.handle(payload))
        if self.pump:
            mqc.register(self.pump.topic, lambda p: self.pump.set(p.lower() == "on"))

    def status(self):
        return {
            "valves": {name: v.current_position for name, v in self.valves.items()},
            "pump": self.pump.state if self.pump else None,
            "float_sensors": self.float_sensors.read() if self.float_sensors else None
        }

    def shutdown(self):
        if self.pump:
            self.pump.off()
        for valve in self.valves.values():
            valve.release()

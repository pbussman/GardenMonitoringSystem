from machine import Pin
import utime

class RainSensor:
    def __init__(self, power_pin, data_pin):
        self.power_pin = Pin(power_pin, Pin.OUT)
        self.data_pin = Pin(data_pin, Pin.IN)

    def read(self):
        self.power_pin.value(1)  # Turn the rain sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        rain_state = self.data_pin.value()
        self.power_pin.value(0)  # Turn the rain sensor's power OFF
        return "It's raining!" if rain_state == 0 else "No rain."

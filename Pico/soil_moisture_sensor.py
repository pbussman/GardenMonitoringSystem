from machine import Pin, ADC
import utime

class SoilMoistureSensor:
    def __init__(self, power_pin, data_pin):
        self.power_pin = Pin(power_pin, Pin.OUT)
        self.data_pin = ADC(Pin(data_pin))

    def read(self):
        self.power_pin.value(1)  # Turn the soil moisture sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        moisture_value = self.data_pin.read_u16()
        self.power_pin.value(0)  # Turn the soil moisture sensor's power OFF
        moisture_percentage = (moisture_value / 65535.0) * 100
        return {'moisture_value': moisture_value, 'moisture_percentage': moisture_percentage}

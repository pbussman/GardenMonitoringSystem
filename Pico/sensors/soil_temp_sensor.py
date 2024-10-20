from machine import Pin
import onewire, ds18x20
import utime

class SoilTempSensor:
    def __init__(self, power_pin, data_pin):
        self.power_pin = Pin(power_pin, Pin.OUT)
        self.data_pin = Pin(data_pin)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.data_pin))

    def read(self):
        self.power_pin.value(1)  # Turn the soil temperature sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        self.ds_sensor.convert_temp()
        utime.sleep_ms(750)
        temp_c = self.ds_sensor.read_temp(self.ds_sensor.scan()[0])
        self.power_pin.value(0)  # Turn the soil temperature sensor's power OFF
        temp_f = temp_c * 9 / 5 + 32
        return {'temperature_c': temp_c, 'temperature_f': temp_f}

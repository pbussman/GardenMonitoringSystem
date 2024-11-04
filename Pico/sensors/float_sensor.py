from machine import Pin

class FloatSensor:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)  # Use PULL_UP if the sensor pulls the pin low when activated

    def read(self):
        return self.pin.value()  # Returns 0 if the float sensor is activated (closed), 1 if not (open)

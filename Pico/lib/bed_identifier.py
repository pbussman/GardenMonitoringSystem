# bed_identifier.py
from machine import Pin

def read_bed_id(pin_nums=(10, 11, 12, 13)):
    dip_pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in pin_nums]
    bits = [not pin.value() for pin in dip_pins]  # DIP ON = LOW
    return sum(bit << idx for idx, bit in enumerate(reversed(bits)))

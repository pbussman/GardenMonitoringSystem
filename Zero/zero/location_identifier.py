from machine import Pin

def read_dip_config(pin_nums=(10, 11, 12, 13)):
    dip_pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in pin_nums]
    bits = [not pin.value() for pin in dip_pins]
    return sum(bit << idx for idx, bit in enumerate(reversed(bits)))

def parse_config(config):
    location_id = config & 0b1         # bit 0
    float_enabled = (config >> 1) & 0b1  # bit 1
    return location_id, bool(float_enabled)

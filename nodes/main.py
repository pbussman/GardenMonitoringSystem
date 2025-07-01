import RPi.GPIO as GPIO
import time

# Map relay channels to GPIO pins (BCM numbering)
RELAY_PINS = {
    1: 17,
    2: 27,
    3: 22,
    4: 23,
    5: 24,
    6: 25,
    7: 5,
    8: 6
}

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # Set HIGH to deactivate (active LOW)

def set_relay(channel, state):
    if channel not in RELAY_PINS:
        raise ValueError(f"Invalid channel {channel}. Must be 1–8.")
    GPIO.output(RELAY_PINS[channel], GPIO.LOW if state else GPIO.HIGH)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        print("Relays initialized. Turning each ON for 1 sec, then OFF.")
        for ch in RELAY_PINS:
            print(f"Relay {ch} → ON")
            set_relay(ch, True)
            time.sleep(1)
            print(f"Relay {ch} → OFF")
            set_relay(ch, False)
        print("Done.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        cleanup()

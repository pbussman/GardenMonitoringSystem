import os
from sdcard import SDCard
from machine import SPI, Pin

def init_sd():
    """Initialize and mount the SD card."""
    spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))  # Using pins GP6, GP7, GP8
    cs = Pin(5, Pin.OUT)  # Chip select on GP5
    sd = SDCard(spi, cs)
    os.mount(sd, "/sd")  # Mount SD card at /sd
    print("SD card initialized and mounted!")
    return "/sd"

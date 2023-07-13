from typing import Any
from machine import Pin, SPI
from pin_lib import *
from ssd1306 import SSD1306_SPI

class Display:
    def __init__(self):
        self.SCREEN_HEIGHT = 64
        self.SCREEN_WIDTH = 128

        spi_sck = Pin(DS_SCLK_PIN) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
        spi_sda = Pin(DS_SDA_PIN) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
        spi_res = Pin(DS_RES_PIN) # res stands for reset; to be connected to a free GPIO pin
        spi_dc  = Pin(DS_DC_PIN) # dc stands for data/command; to be connected to a free GPIO pin
        spi_cs  = Pin(DS_CS_PIN) # chip select; to be connected to the SPI chip select of the Pico

        SPI_DEVICE = 0
        oled_spi = SPI(SPI_DEVICE, baudrate=100000, sck=spi_sck, mosi=spi_sda)
        self.oled = SSD1306_SPI(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True)
    
    def __getattribute__(self, __name: str) -> Any: # this allows all functions passed to Display to go to oled
        return getattr(self.oled, __name)
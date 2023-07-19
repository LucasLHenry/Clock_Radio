from machine import Pin, SPI
from pin_lib import *
from settings_lib import DISPLAY_SCREEN_HEIGHT, DISPLAY_SCREEN_WIDTH
from ssd1306 import SSD1306_SPI
import math

class Display:
    def __init__(self):
        spi_sck = Pin(DS_SCLK_PIN) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
        spi_sda = Pin(DS_SDA_PIN) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
        spi_res = Pin(DS_RES_PIN) # res stands for reset; to be connected to a free GPIO pin
        spi_dc  = Pin(DS_DC_PIN) # dc stands for data/command; to be connected to a free GPIO pin
        spi_cs  = Pin(DS_CS_PIN) # chip select; to be connected to the SPI chip select of the Pico

        SPI_DEVICE = 0
        oled_spi = SPI(SPI_DEVICE, baudrate=100000, sck=spi_sck, mosi=spi_sda)
        self.oled = SSD1306_SPI(DISPLAY_SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True)
    
    def char_varsize(self, c, x, y, size):
        pass
    
    # wrapper for char_varsize, so you can print sentences without worrying about cursor location
    def text_varsize(self, text, x, y, size):
        i = 0
        for c in text:
            pos_x = (x + i*11*size)
            pos_y = y + math.floor(pos_x / DISPLAY_SCREEN_WIDTH) * 26
            self.char_varsize(c, pos_x % DISPLAY_SCREEN_WIDTH, pos_y, size)
            i += 1

    # prints a character at a specified location with a specified size, using the line function
    def char_varsize(self, c, x, y, size):
        if c=="A" or c=="a":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+1*size),math.floor(x+10*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+11*size),math.floor(x+8*size),math.floor(y+11*size),1)
        elif c=="B" or c=="b":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+6*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+1*size),math.floor(x+8*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+3*size),math.floor(x+8*size),math.floor(y+4*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+4*size),math.floor(x+6*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+7*size),math.floor(x+9*size),math.floor(y+10*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+10*size),math.floor(x+9*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+12*size),math.floor(x+6*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+15*size),1)
        elif c=="C" or c=="c":
            self.oled.line(math.floor(x+10*size),math.floor(y+2*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+8*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+13*size),1)
        elif c=="D" or c=="d":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+6*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+3*size),math.floor(x+9*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+12*size),math.floor(x+6*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+15*size),1)
        elif c=="E" or c=="e":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+7*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+15*size),1)
        elif c=="F" or c=="f":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+6*size),math.floor(y+7*size),1)
        elif c=="G" or c=="g":
            self.oled.line(math.floor(x+9*size),math.floor(y+2*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+8*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+13*size),math.floor(x+10*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+9*size),math.floor(x+6*size),math.floor(y+9*size),1)    
        elif c=="H" or c=="h":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+9*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="I" or c=="i":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+1*size),1)
        elif c=="J" or c=="j":
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+10*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+10*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+10*size),1)
        elif c=="K" or c=="k":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+9*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+7*size),math.floor(x+9*size),math.floor(y+15*size),1)
        elif c=="L" or c=="l":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+15*size),1)
        elif c=="M" or c=="m":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+5*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+5*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="N" or c=="n":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="O" or c=="o":
            self.oled.line(math.floor(x+10*size),math.floor(y+5*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+12*size),math.floor(x+10*size),math.floor(y+5*size),1)
        elif c=="P" or c=="p":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+4*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+4*size),math.floor(x+9*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+6*size), math.floor(x+6*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+9*size),math.floor(x+1*size),math.floor(y+9*size),1)
        elif c=="Q" or c=="q":
            self.oled.line(math.floor(x+10*size),math.floor(y+5*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+12*size),math.floor(x+10*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+10*size),math.floor(x+10*size),math.floor(y+15*size),1)
        elif c=="R" or c=="r":
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+4*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+4*size),math.floor(x+9*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+6*size), math.floor(x+6*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+9*size),math.floor(x+1*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+9*size),math.floor(x+9*size),math.floor(y+15*size),1)
        elif c=="S" or c=="s":
            self.oled.line(math.floor(x+9*size),math.floor(y+2*size),math.floor(x+7*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+1*size),math.floor(x+3*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+2*size),1)    
            self.oled.line(math.floor(x+2*size),math.floor(y+2*size),math.floor(x+1*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+5*size),math.floor(x+5*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+7*size),math.floor(x+9*size),math.floor(y+8*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+8*size),math.floor(x+10*size),math.floor(y+11*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+11*size),math.floor(x+10*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+13*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+13*size),1)
        elif c=="T" or c=="t":
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="U" or c=="u":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+13*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+13*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="V" or c=="v":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+5*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+1*size),1)
        elif c=="W" or c=="w":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+8*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+8*size),math.floor(x+8*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+1*size),1)
        elif c=="X" or c=="x":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+15*size),1)
        elif c=="Y" or c=="y":
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+7*size),math.floor(x+10*size),math.floor(y+1*size),1)
        elif c=="Z" or c=="z":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+15*size),1)
        elif c==".":
            self.oled.line(math.floor(x+1*size),math.floor(y+14*size),math.floor(x+2*size),math.floor(y+14*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+2*size),math.floor(y+15*size),1)
        elif c=="!":
            self.oled.line(math.floor(x+1*size),math.floor(y+14*size),math.floor(x+1*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+10*size),1)
        elif c=="?":
            self.oled.line(math.floor(x+5*size),math.floor(y+14*size),math.floor(x+6*size),math.floor(y+14*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+6*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+10*size),math.floor(x+5*size),math.floor(y+8*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+8*size),math.floor(x+8*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+6*size),math.floor(x+9*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
        elif c=="/":
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+15*size),1)
        elif c==":":
            self.oled.line(math.floor(x+1*size),math.floor(y+14*size),math.floor(x+2*size),math.floor(y+14*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+2*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+6*size),math.floor(x+2*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+5*size),math.floor(x+2*size),math.floor(y+5*size),1)
        elif c==",":
            self.oled.line(math.floor(x+1*size),math.floor(y+13*size),math.floor(x+1*size),math.floor(y+14*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+13*size),math.floor(x+2*size),math.floor(y+17*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+17*size),math.floor(x+2*size),math.floor(y+17*size),1)
        elif c=="&":
            self.oled.line(math.floor(x+4*size),math.floor(y+7*size),math.floor(x+2*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+5*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+3*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+2*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+6*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+2*size),math.floor(x+8*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+3*size),math.floor(x+8*size),math.floor(y+4*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+4*size),math.floor(x+6*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+6*size),math.floor(x+1*size),math.floor(y+10*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+10*size),math.floor(x+1*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+13*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+6*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+8*size),math.floor(x+10*size),math.floor(y+15*size),1)
        elif c=="+":
            self.oled.line(math.floor(x+5*size),math.floor(y+5*size),math.floor(x+5*size),math.floor(y+11*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+8*size),math.floor(x+8*size),math.floor(y+8*size),1)
        elif c=="-":
            self.oled.line(math.floor(x+2*size),math.floor(y+8*size),math.floor(x+8*size),math.floor(y+8*size),1)
        elif c=="=":
            self.oled.line(math.floor(x+2*size),math.floor(y+6*size),math.floor(x+8*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+9*size),math.floor(x+8*size),math.floor(y+9*size),1)
        elif c=="0":
            self.oled.line(math.floor(x+10*size),math.floor(y+5*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+12*size),math.floor(x+10*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+4*size),math.floor(x+2*size),math.floor(y+12*size),1)
        elif c=="1":
            self.oled.line(math.floor(x+5*size),math.floor(y+15*size),math.floor(x+5*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+5*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
        elif c=="2":
            self.oled.line(math.floor(x+1*size),math.floor(y+3*size),math.floor(x+2*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+1*size),1)    
            self.oled.line(math.floor(x+7*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+3*size),math.floor(x+9*size),math.floor(y+6*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+6*size),math.floor(x+2*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+13*size),math.floor(x+1*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+15*size),1)
        elif c=="3":
            self.oled.line(math.floor(x+1*size),math.floor(y+3*size),math.floor(x+2*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+1*size),1)    
            self.oled.line(math.floor(x+7*size),math.floor(y+1*size),math.floor(x+9*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+3*size),math.floor(x+9*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+5*size),math.floor(x+7*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+7*size),math.floor(x+4*size),math.floor(y+7*size),1)    
            self.oled.line(math.floor(x+7*size),math.floor(y+8*size),math.floor(x+9*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+9*size),math.floor(x+9*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+12*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+13*size),1)    
        elif c=="4":
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+8*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+9*size),math.floor(y+7*size),1)
        elif c=="5":
            self.oled.line(math.floor(x+9*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+7*size),1)    
            self.oled.line(math.floor(x+7*size),math.floor(y+8*size),math.floor(x+9*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+9*size),math.floor(x+9*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+12*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+13*size),1)
        elif c=="6":
            self.oled.line(math.floor(x+10*size),math.floor(y+3*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+1*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+7*size),math.floor(x+1*size),math.floor(y+12*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+12*size),math.floor(x+4*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+10*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+13*size),math.floor(x+10*size),math.floor(y+9*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+9*size),math.floor(x+8*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+7*size),math.floor(x+4*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+7*size),math.floor(x+2*size),math.floor(y+9*size),1)
        elif c=="7":
            self.oled.line(math.floor(x+1*size),math.floor(y+1*size),math.floor(x+10*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+1*size),math.floor(x+3*size),math.floor(y+15*size),1)
        elif c=="8":
            self.oled.line(math.floor(x+4*size),math.floor(y+7*size),math.floor(x+2*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+5*size),math.floor(x+2*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+2*size),math.floor(y+3*size),math.floor(x+3*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+2*size),math.floor(x+4*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+1*size),math.floor(x+6*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+1*size),math.floor(x+7*size),math.floor(y+2*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+2*size),math.floor(x+8*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+3*size),math.floor(x+8*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+5*size),math.floor(x+6*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+10*size),math.floor(x+1*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+13*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+9*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+13*size),math.floor(x+9*size),math.floor(y+10*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+10*size),math.floor(x+6*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+6*size),math.floor(y+7*size),math.floor(x+4*size),math.floor(y+7*size),1)
            self.oled.line(math.floor(x+4*size),math.floor(y+7*size),math.floor(x+2*size),math.floor(y+9*size),1)
        elif c=="9":
            self.oled.line(math.floor(x+10*size),math.floor(y+6*size),math.floor(x+8*size),math.floor(y+8*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+8*size),math.floor(x+3*size),math.floor(y+8*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+8*size),math.floor(x+1*size),math.floor(y+5*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+5*size),math.floor(x+1*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+1*size),math.floor(y+3*size),math.floor(x+3*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+1*size),math.floor(x+8*size),math.floor(y+1*size),1)
            self.oled.line(math.floor(x+8*size),math.floor(y+1*size),math.floor(x+10*size),math.floor(y+3*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+3*size),math.floor(x+10*size),math.floor(y+10*size),1)
            self.oled.line(math.floor(x+10*size),math.floor(y+10*size),math.floor(x+9*size),math.floor(y+13*size),1)
            self.oled.line(math.floor(x+9*size),math.floor(y+13*size),math.floor(x+7*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+7*size),math.floor(y+15*size),math.floor(x+3*size),math.floor(y+15*size),1)
            self.oled.line(math.floor(x+3*size),math.floor(y+15*size),math.floor(x+1*size),math.floor(y+13*size),1)
        elif c==" ":
            pass

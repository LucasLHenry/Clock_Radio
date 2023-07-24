from machine import Pin, ADC


# simple sensor class, just reads from analog input and spits it out
class Sensor:
    def __init__(self, pinnum):
        self.pin = Pin(pinnum, Pin.IN)
        self.adc = ADC(self.pin)
    
    def get_voltage(self):
        val = self.adc.read_u16()
        return val * 3.3 / 65535.0

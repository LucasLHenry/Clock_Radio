from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from pin_lib import *
from machine import Pin, RTC

clock = RTC()
radio = Radio(101.9, 1, False)
display = Display()

clock_sel_btn = Pin(BTN1_PIN, Pin.IN)
alarm_sel_btn = Pin(BTN2_PIN, Pin.IN)
plant_sel_btn = Pin(BTN3_PIN, Pin.IN)
snooze_btn = Pin(BTN4_PIN, Pin.IN)

alarm_swt = Pin(SWT1_PIN, Pin.IN)
radio_swt = Pin(SWT2_PIN, Pin.IN)

tune_knob = Encoder(ENC1A_PIN, ENC1B_PIN)
vol_knob = Encoder(ENC2A_PIN, ENC2B_PIN)

while True:
    pass
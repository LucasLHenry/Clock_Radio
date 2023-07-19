from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from clock_class import Clock
from button_class import Button
from pin_lib import *
from settings_lib import RADIO_STATION

clock = Clock()
radio = Radio(RADIO_STATION, 1, False)
display = Display()

clock_sel_btn = Button(BTN1_PIN)
alarm_sel_btn = Button(BTN2_PIN)
plant_sel_btn = Button(BTN3_PIN)
snooze_btn = Button(BTN4_PIN)

alarm_swt = Button(SWT1_PIN)
radio_swt = Button(SWT2_PIN)

tune_knob = Encoder(ENC1A_PIN, ENC1B_PIN)
vol_knob = Encoder(ENC2A_PIN, ENC2B_PIN)


while True:
    pass
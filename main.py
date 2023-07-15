from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from clock_class import Clock
from pin_lib import *
from machine import Pin, RTC

clock = Clock()
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

def get_button_values():
    return (clock_sel_btn.value(), alarm_sel_btn.value(), plant_sel_btn.value(), snooze_btn.value())

def get_switch_values():
    return (alarm_swt.value(), radio_swt.value())

def get_knob_values():
    return (tune_knob.get(), vol_knob.get())


while True:
    (cbtn_val, abtn_val, pbtn_val, sbtn_val) = get_button_values()
    (tswt_val, vswt_val) = get_switch_values()
    (tknb_val, vknb_val) = get_knob_values()

    display.fill(0)
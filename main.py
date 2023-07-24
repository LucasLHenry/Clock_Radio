from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from clock_class import Clock
from button_class import Button
from sensor_class import Sensor
from pin_lib import *
from machine import Pin, Timer
import settings_lib as settings
from math import floor

# class Disp_Mode(enum):
#     CLOCK_DISP = 0
#     CLOCK_SET = 1
#     ALARM_SET = 2
#     PLANT_DISP = 3

# class Time_Mode(enum):
#     H12 = 0
#     H24 = 1

class Device:
    def __init__(self):
        self.clock = Clock()
        self.r_freq = settings.RADIO_STATION
        self.r_vol = 1
        self.r_mute = True
        self.radio = Radio(self.r_freq, self.r_vol, self.r_mute)
        self.display = Display()
        self.timeout = 0
        self.alarm_primed = False
        self.alarm_active = False
        self.alarm_snoozed = False
        self.snooze_timeout = 0
        self.curr_mode = 0
        self.next_mode = 0
        self.t_mode = 0
        self.newtime = (0, 0)
        self.newalarm = (0, 0)
        self.clock_sel_btn = Button(BTN1_PIN)
        self.alarm_sel_btn = Button(BTN2_PIN)
        self.plant_sel_btn = Button(BTN3_PIN)
        self.snooze_btn = Button(BTN4_PIN)
        self.alarm_swt = Pin(SWT1_PIN, Pin.IN)
        self.radio_swt = Pin(SWT2_PIN, Pin.IN)
        self.tune_knob = Encoder(ENC1A_PIN, ENC1B_PIN)
        self.vol_knob = Encoder(ENC2A_PIN, ENC2B_PIN)
        self.soil_sensor = Sensor(SOIL_A_PIN)

dh = Device()
loop_timer = Timer()

def display_time(dh, time):
    if dh.t_mode == 0:
        hour = time[0]
        if hour == 0:
            time_str = f"12:{floor(time[1]):02} AM"
        elif hour < 12:
            time_str = f"{floor(hour):2}:{floor(time[1]):02} AM"
        else:
            time_str = f"{floor(hour-12):2}:{floor(time[1]):02} PM"
        dh.display.text_varsize(time_str, 20, 28, 1)
    else:
        time_str = f"{floor(time[0]):02}:{floor(time[1]):02}"
        dh.display.text_varsize(time_str, 20, 28, 1)

def offset_with_bounds(value, offset, lower_bound, upper_bound):
    newvalue = value + offset
    while newvalue < lower_bound:
        newvalue += upper_bound - lower_bound
    while newvalue >= upper_bound:
        newvalue -= upper_bound - lower_bound
    return newvalue

def update(_timer):
    global dh

    dh.display.oled.fill(0)

    # Steady-state logic
    if dh.curr_mode == 0:
        time = dh.clock.get_time()
        display_time(dh, time)

        freq_offset = dh.tune_knob.get()
        vol_offset = dh.vol_knob.get()

        if freq_offset or vol_offset:
            dh.r_freq = offset_with_bounds(dh.r_freq, freq_offset*settings.FREQ_MULTIPLIER, 76, 108)
            dh.r_vol = offset_with_bounds(dh.r_vol, vol_offset*settings.VOL_MULTIPLIER, 1, 16)
            dh.radio.SetFrequency(floor(dh.r_freq))
            dh.radio.SetVolume(floor(dh.r_vol))
            freq_vol_str = f"Freq: {floor(dh.r_freq):5.1f},   Vol: {floor(dh.r_vol):2d}"
            dh.display.text_varsize(freq_vol_str, 10, 28, 1)


    elif dh.curr_mode == 1:
        h_offset = dh.tune_knob.get()
        m_offset = dh.vol_knob.get()
        dh.newtime = (
            offset_with_bounds(dh.newtime[0], h_offset*settings.TIME_MULTIPLIER, 0, 24),
            offset_with_bounds(dh.newtime[1], m_offset*settings.TIME_MULTIPLIER, 0, 60)
        )
        display_time(dh, dh.newtime)

        if dh.clock_sel_btn.get_held():
            dh.t_mode = 1 if dh.t_mode == 0 else 0

    elif dh.curr_mode == 2:
        h_offset = dh.tune_knob.get()
        m_offset = dh.vol_knob.get()
        dh.newalarm = (
            offset_with_bounds(dh.newalarm[0], h_offset*settings.TIME_MULTIPLIER, 0, 24),
            offset_with_bounds(dh.newalarm[1], m_offset*settings.TIME_MULTIPLIER, 0, 60)
        )
        display_time(dh, dh.newalarm)

        if dh.alarm_sel_btn.get_held() and dh.alarm_active:
            dh.snooze_timeout = settings.SNOOZE_DELAY*60*settings.UPDATE_FREQ
            dh.alarm_snoozed = True

    elif dh.curr_mode == 3:
        moisture = floor((dh.soil_sensor.get_voltage() / 5)*100)
        moisture_str = f"Soil Water: {moisture:2d}%"
        dh.display.text_varsize("moisture_str", 20, 28, 1)


    # Toggle radio
    if dh.radio_swt.value() and dh.r_mute and not dh.alarm_active:
        dh.r_mute = False
        dh.radio.SetMute(dh.r_mute)
    elif not dh.radio_swt.value() and not dh.r_mute and not dh.alarm_active:
        dh.r_mute = True
        dh.radio.SetMute(dh.r_mute)

    if dh.r_mute and dh.alarm_active and not dh.alarm_snoozed:
        dh.r_mute = False
        dh.radio.SetMute(dh.r_mute)
    elif not dh.r_mute and dh.alarm_active and dh.alarm_snoozed:
        dh.r_mute = True
        dh.radio.SetMute(dh.r_mute)

    # Trigger alarm
    if dh.alarm_swt.value():
        time = dh.clock.get_time()
        alarm = dh.clock.get_alarm()
        if alarm[0] == time[0] and alarm[1] == time[1]:
            if dh.alarm_primed:
                dh.alarm_primed = False
                dh.alarm_snoozed = False
                dh.alarm_active = True
        else:
            dh.alarm_primed = True
    else:
        dh.alarm_primed = False
        dh.alarm_active = False

    if dh.alarm_snoozed and dh.snooze_timeout > 0:
        dh.snooze_timeout -= 1
    elif dh.alarm_snoozed and dh.snooze_timeout <= 0:
        dh.alarm_snoozed = False

    # Set next state
    if dh.clock_sel_btn.get():
        dh.next_mode = 1 if not dh.curr_mode == 1 else 0
    elif dh.alarm_sel_btn.get():
        dh.next_mode = 2 if not dh.curr_mode == 2 else 0
    elif dh.plant_sel_btn.get():
        dh.next_mode = 3 if not dh.curr_mode == 3 else 0
    else:
        pass
        # dh.timeout += 1
        # if dh.timeout >= settings.UPDATE_FREQ*settings.MODE_TIMEOUT:
        #     dh.next_mode = 0
        # else:
        #     dh.next_mode = dh.curr_mode

    # State transition logic
    if dh.next_mode != dh.curr_mode:
        dh.timeout = 0
        if dh.next_mode == 1:
            dh.newtime = dh.clock.get_time()
        elif dh.next_mode == 2:
            dh.newalarm == dh.clock.get_alarm()
        elif dh.curr_mode == 1:
            dh.clock.set_time(int(floor(dh.newtime[0])), int(floor(dh.newtime[1])))
        elif dh.curr_mode == 2:
            dh.clock.set_alarm(int(floor(dh.newalarm[0])), int(floor(dh.newalarm[1])))

    # Mutate state
    dh.curr_mode = dh.next_mode

    dh.display.oled.show()


loop_timer.init(mode=Timer.PERIODIC, freq=settings.UPDATE_FREQ, callback=update)

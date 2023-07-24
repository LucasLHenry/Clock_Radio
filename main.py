from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from clock_class import Clock
from button_class import Button
from sensor_class import Sensor
from pin_lib import *
from machine import Pin, Timer
from settings_lib import *
from math import floor

class Disp_Mode(enum):
    CLOCK_DISP = 0
    CLOCK_SET = 1
    ALARM_SET = 2
    PLANT_DISP = 3

class Time_Mode(enum):
    H12 = 0
    H24 = 1

clock = Clock()
r_freq = RADIO_STATION
r_vol = 1
r_mute = False
radio = Radio(r_freq, r_vol, False)
display = Display()
loop_timer = Timer()
timeout = 0

alarm_primed = False
alarm_active = False
alarm_snoozed = False
snooze_timeout = 0

curr_mode = Disp_Mode(Disp_Mode.CLOCK_DISP)
t_mode = Time_Mode(Time_Mode.H12)

clock_sel_btn = Button(BTN1_PIN)
alarm_sel_btn = Button(BTN2_PIN)
plant_sel_btn = Button(BTN3_PIN)
snooze_btn = Button(BTN4_PIN)

alarm_swt = Pin(SWT1_PIN, Pin.IN)
radio_swt = Pin(SWT2_PIN, Pin.IN)

tune_knob = Encoder(ENC1A_PIN, ENC1B_PIN)
vol_knob = Encoder(ENC2A_PIN, ENC2B_PIN)

soil_sensor = Sensor(SOIL_A_PIN)

def display_time(time):
    if t_mode == H12:
            time_str = f"{ time[0] if time[0] <= 12 else time[0] - 12 :d}:{time[1]:2.d}"
            display.text_varsize(time_str, 20, 28, 1)
        else:
            time_str = f"{time[0]:2.d}:{time[1]:2.d}"
            display.text_varsize(time_str, 20, 28, 1)

def offset_with_bounds(value, offset, lower_bound, upper_bound):
    newvalue = value + offset
    if newvalue < lower_bound:
        new_value += upper_bound - lower_bound
    elif newvalue > upper_bound:
        newvalue -= upper_bound - lower_bound
    return newvalue

def update():
    # Steady-state logic
    if curr_mode == Disp_Mode.CLOCK_DISP:
        time = clock.get_time()
        display_time(time)

        freq_offset = tune_knob.get()
        vol_offset = vol_knob.get()

        if freq_offset or vol_offset:
            r_freq = offset_with_bounds(r_freq, freq_offset*FREQ_MULTIPLIER, 76, 108)
            r_vol = offset_with_bounds(r_vol, vol_offset*VOL_MULTIPLIER, 1, 16)
            radio.SetFrequency(floor(r_freq))
            radio.SetVolume(floor(r_vol))
            freq_vol_str = f"Freq: {floor(r_freq):5.1d},   Vol: {floor(r_vol):2.d}"
            display.text_varsize(freq_vol_str, 10, 28, 1)


    elif curr_mode == Disp_Mode.CLOCK_SET:
        h_offset = tune_knob.get()
        m_offset = vol_knob.get()
        newtime = (
            offset_with_bounds(newtime[0], h_offset*TIME_MULTIPLIER, 0, 60),
            offset_with_bounds(newtime[1], m_offset*TIME_MULTIPLIER, 0, 60)
        )
        display_time(newtime)

        if clock_sel_btn.get_held():
            t_mode = H24 if t_mode == H12 else H12

    elif curr_mode == Disp_Mode.ALARM_SET:
        h_offset = tune_knob.get()
        m_offset = vol_knob.get()
        newalarm = (
            offset_with_bounds(newalarm[0], h_offset*TIME_MULTIPLIER, 0, 60),
            offset_with_bounds(newalarm[1], m_offset*TIME_MULTIPLIER, 0, 60)
        )
        display_time(newalarm)

        if alarm_sel_btn.get_held() and alarm_active:
            snooze_timeout = SNOOZE_DELAY*60*UPDATE_FREQ
            alarm_snoozed = True

    elif curr_mode == Disp_Mode.PLANT_DISP:
        display.text_varsize("Under Construction", 20, 28, 1)


    # Toggle radio
    if radio_swt.value() and r_mute and not alarm_active:
        r_mute = False
        radio.setMute(r_mute)
    elif not radio_swt.value() and not r_mute and not alarm_active:
        r_mute = True
        radio.setMute(r_mute)

    if r_mute and alarm_active and not alarm_snoozed:
        r_mute = False
        radio.setMute(r_mute)
    elif not r_mute and alarm_active and alarm_snoozed:
        r_mute = True
        radio.setMute(r_mute)

    # Trigger alarm
    if alarm_swt.value():
        time = clock.get_time()
        alarm = clock.get_alarm()
        if alarm[0] == time[0] and alarm[1] == time[1]:
            if alarm_primed:
                alarm_primed = False
                alarm_snoozed = False
                alarm_active = True
        else
            alarm_primed = True
    else:
        alarm_primed = False
        alarm_active = False

    if alarm_snoozed and snooze_timeout > 0:
        snooze_timeout -= 1
    elif alarm_snoozed and snooze_timeout <= 0:
        alarm_snoozed = False

    # Set next state
    if clock_sel_btn.get():
        next_mode = Disp_Mode.CLOCK_SET if not curr_mode == Disp_Mode.CLOCK_SET else Disp_Mode.CLOCK_DISP
    elif alarm_sel_btn.get():
        next_mode = Disp_Mode.ALARM_SET if not curr_mode == Disp_Mode.ALARM_SET else Disp_Mode.CLOCK_DISP
    elif plant_sel_btn.get():
        next_mode = Disp_Mode.PLANT_DISP if not curr_mode == Disp_Mode.PLANT_DISP else Disp_Mode.CLOCK_DISP
    else:
        timeout += 1
        if timeout >= UPDATE_FREQ*MODE_TIMEOUT:
            next_mode = Disp_Mode.CLOCK_DISP
        else:
            next_mode = curr_mode

    # State transition logic
    if next_mode != curr_mode:
        timeout = 0
        if next_mode == Disp_Mode.CLOCK_SET:
            newtime = clock.get_time()
        elif next_mode == Disp_Mode.ALARM_SET:
            newalarm == clock.get_alarm()
        elif curr_mode == Disp_Mode.CLOCK_SET:
            clock.set_time((floor(newtime[0]), floor(newtime[1])))
        elif curr_mode == Disp_Mode.ALARM_SET:
            clock.set_alarm((floor(newalarm[0]), floor(newalarm[1])))

    # Mutate state
    curr_mode = next_mode


loop_timer.init(mode=Timer.PERIODIC, freq=UPDATE_FREQ, callback=update)

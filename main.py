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
        self.radio_changed = False
        self.radio_timeout = 0
        self.display = Display()
        self.alarm_primed = False
        self.alarm_active = False
        self.alarm_snoozed = False
        self.snooze_timeout = 0
        self.info_timeout = 0
        self.flash_cycle_pos = 0
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
    hour = floor(time[0])
    minute = floor(time[1])
    if dh.t_mode == 0:
        if hour == 0:
            time_str = f"12:{minute:02} AM"
        elif hour < 12:
            time_str = f"{hour:2}:{minute:02} AM"
        elif hour == 12:
            time_str = f"12:{minute:02} PM"
        else:
            time_str = f"{hour-12:2}:{minute:02} PM"
        dh.display.text_varsize(time_str, 20, 28, 1)
    else:
        time_str = f"{hour:02}:{minute:02}"
        dh.display.text_varsize(time_str, 20, 28, 1)

def offset_with_bounds(value, offset, lower_bound, upper_bound, wrap = True):
    newvalue = value + offset
    if wrap:
        while newvalue < lower_bound:
            newvalue += upper_bound - lower_bound
        while newvalue >= upper_bound:
            newvalue -= upper_bound - lower_bound
    else:
        if newvalue < lower_bound:
            newvalue = lower_bound
        elif newvalue > upper_bound - 1:
            newvalue = upper_bound - 1
    return newvalue

def update(_timer):
    global dh

    dh.display.oled.fill(0)

    # Steady-state logic
    if dh.curr_mode == 0:
        freq_offset = dh.tune_knob.get()
        vol_offset = dh.vol_knob.get()
        dh.r_freq = offset_with_bounds(dh.r_freq, freq_offset*settings.FREQ_MULTIPLIER, 88, 108)
        dh.r_vol = offset_with_bounds(dh.r_vol, vol_offset*settings.VOL_MULTIPLIER, 1, 16, False)

        if freq_offset != 0 or vol_offset != 0:
            dh.info_timeout = settings.INFO_TIMEOUT*settings.UPDATE_FREQ
            dh.radio.SetFrequency(floor(dh.r_freq*10)/10)
            dh.radio.SetVolume(dh.r_vol)
            dh.radio_changed = True

        if dh.info_timeout > 0:
            dh.info_timeout -= 1
            freq_vol_str = f"{dh.r_freq:5.1f} MHz    {dh.r_vol:2.0f}/15"
            dh.display.text_varsize(freq_vol_str, 10, 20, 0.5)
        else:
            time = dh.clock.get_time()
            display_time(dh, time)

        if dh.clock_sel_btn.get():
            dh.t_mode = 1 if dh.t_mode == 0 else 0

        if dh.alarm_sel_btn.get() and dh.alarm_active:
            dh.snooze_timeout = settings.SNOOZE_DELAY*60*settings.UPDATE_FREQ
            dh.alarm_snoozed = True


    elif dh.curr_mode == 1:
        h_offset = dh.tune_knob.get()
        m_offset = dh.vol_knob.get()
        dh.newtime = (
            offset_with_bounds(dh.newtime[0], h_offset*settings.TIME_MULTIPLIER, 0, 24),
            offset_with_bounds(dh.newtime[1], m_offset*settings.TIME_MULTIPLIER, 0, 60)
        )

        if dh.clock_sel_btn.get():
            dh.t_mode = 1 if dh.t_mode == 0 else 0

        dh.display.text_varsize("Set Time:", 20, 10, 0.5)
        if dh.flash_cycle_pos <= settings.FLASH_LENGTH*settings.FLASH_DS*settings.UPDATE_FREQ:
            display_time(dh, dh.newtime)
        dh.flash_cycle_pos = dh.flash_cycle_pos+1 if dh.flash_cycle_pos < settings.FLASH_LENGTH*settings.UPDATE_FREQ else 0

    elif dh.curr_mode == 2:
        h_offset = dh.tune_knob.get()
        m_offset = dh.vol_knob.get()
        dh.newalarm = (
            offset_with_bounds(dh.newalarm[0], h_offset*settings.TIME_MULTIPLIER, 0, 24),
            offset_with_bounds(dh.newalarm[1], m_offset*settings.TIME_MULTIPLIER, 0, 60)
        )

        dh.display.text_varsize("Set Alarm:", 20, 10, 0.5)
        if dh.flash_cycle_pos <= settings.FLASH_LENGTH*settings.FLASH_DS*settings.UPDATE_FREQ:
            display_time(dh, dh.newalarm)
        dh.flash_cycle_pos = dh.flash_cycle_pos+1 if dh.flash_cycle_pos < settings.FLASH_LENGTH*settings.UPDATE_FREQ else 0



    elif dh.curr_mode == 3:
        moisture = floor((dh.soil_sensor.get_voltage() / 5)*100)
        moisture_str = f"{moisture:2d}/100"
        dh.display.text_varsize("Plant Moisture:", 20, 10, 0.5)
        dh.display.text_varsize(moisture_str, 20, 28, 1)


    # Toggle radio
    if not dh.radio_swt.value() and dh.r_mute and not dh.alarm_active:
        dh.r_mute = False
        dh.radio.SetMute(dh.r_mute)
        dh.radio_changed = True
    elif dh.radio_swt.value() and not dh.r_mute and not dh.alarm_active:
        dh.r_mute = True
        dh.radio.SetMute(dh.r_mute)
        dh.radio_changed = True

    if dh.r_mute and dh.alarm_active and not dh.alarm_snoozed:
        dh.r_mute = False
        dh.radio.SetMute(dh.r_mute)
        dh.radio_changed = True
    elif not dh.r_mute and dh.alarm_active and dh.alarm_snoozed:
        dh.r_mute = True
        dh.radio.SetMute(dh.r_mute)
        dh.radio_changed = True

    # Trigger alarm
    if not dh.alarm_swt.value():
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

    # Program Radio
    if dh.radio_changed and dh.radio_timeout <= 0:
        dh.radio.ProgramRadio()
        dh.radio_changed = False
        dh.radio_timeout = settings.UPDATE_FREQ
    elif dh.radio_timeout > 0:
        dh.radio_timeout -= 1

    # Set next state
    if dh.clock_sel_btn.get_held():
        dh.next_mode = 1 if not dh.curr_mode == 1 else 0
    elif dh.alarm_sel_btn.get_held():
        dh.next_mode = 2 if not dh.curr_mode == 2 else 0
    elif dh.plant_sel_btn.get():
        dh.next_mode = 3 if not dh.curr_mode == 3 else 0

    # State transition logic
    if dh.next_mode != dh.curr_mode:

        if dh.next_mode == 0:
            pass
        elif dh.next_mode == 1:
            dh.newtime = dh.clock.get_time()
            dh.flash_cycle_pos = 0
        elif dh.next_mode == 2:
            dh.newalarm == dh.clock.get_alarm()
            dh.flash_cycle_pos = 0

        if dh.curr_mode == 0:
            dh.info_timeout = 0
        elif dh.curr_mode == 1:
            dh.clock.set_time(int(floor(dh.newtime[0])), int(floor(dh.newtime[1])))
        elif dh.curr_mode == 2:
            dh.clock.set_alarm(int(floor(dh.newalarm[0])), int(floor(dh.newalarm[1])))

    # Mutate state
    dh.curr_mode = dh.next_mode
    dh.clock.pass_time(1/settings.UPDATE_FREQ)

    dh.display.oled.show()


loop_timer.init(mode=Timer.PERIODIC, freq=settings.UPDATE_FREQ, callback=update)

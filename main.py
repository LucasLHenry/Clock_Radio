from radio_class import Radio
from display_class import Display
from encoder_class import Encoder
from clock_class import Clock
from button_class import Button
from sensor_class import Sensor
from pin_lib import *
from machine import Pin, Timer
from settings_lib import *

class Mode(enum):
    CLOCK_DISP = 0
    CLOCK_SET = 1
    ALARM_SET = 2
    PLANT_DISP = 3

clock = Clock()
r_freq = RADIO_STATION
r_vol = 1
radio = Radio(r_freq, r_vol, False)
display = Display()
loop_timer = Timer()

curr_mode = Mode(Mode.CLOCK_DISP)

clock_sel_btn = Button(BTN1_PIN)
alarm_sel_btn = Button(BTN2_PIN)
plant_sel_btn = Button(BTN3_PIN)
snooze_btn = Button(BTN4_PIN)

alarm_swt = Pin(SWT1_PIN, Pin.IN)
radio_swt = Pin(SWT2_PIN, Pin.IN)

tune_knob = Encoder(ENC1A_PIN, ENC1B_PIN)
vol_knob = Encoder(ENC2A_PIN, ENC2B_PIN)

soil_sensor = Sensor(SOIL_A_PIN)

def update():
    # Steady-state logic
    if curr_mode == Mode.CLOCK_DISP:
        time = clock.get_time()
        time_str = f"{time[0]:2.d}:{time[1]:2.d}"
        display.text_varsize(time_str, 20, 28, 1)

        # Adjust values all the time - display only when changes made
        # if radio_swt.value():
        #     freq_offset = tune_knob.get()
        #     vol_offset = vol_knob.get()
        #     r_freq += freq_offset
        #     r_vol += vol_offset
        #     radio.SetFrequency(r_freq)
        #     radio.SetVolume(r_vol)

    elif curr_mode == Mode.CLOCK_SET:
        h_offset = tune_knob.get()
        m_offset = vol_knob.get()
        newtime = ( newtime[0] + h_offset, newtime[1] + m_offset )
        display.text_varsize(newtime, 20, 28, 1)
    elif curr_mode == Mode.ALARM_SET:
        h_offset = tune_knob.get()
        m_offset = vol_knob.get()
        newalarm = ( newalarm[0] + h_offset, newalarm[1] + m_offset )
        display.text_varsize(newalarm, 20, 28, 1)
    elif curr_mode == Mode.PLANT_DISP:
        display.text_varsize("Under Construction", 20, 28, 1)

    # Toggle radio
    if radio_swt.value():
        radio.setMute(False)
    elif radio_swt.value():
        radio.setMute(True)

    # Trigger alarm


    # Set next state
    if clock_sel_btn.get():
        next_mode = Mode.CLOCK_SET if not curr_mode == Mode.CLOCK_SET else Mode.CLOCK_DISP
    elif alarm_sel_btn.get():
        next_mode = Mode.ALARM_SET if not curr_mode == Mode.ALARM_SET else Mode.CLOCK_DISP
    elif plant_sel_btn.get():
        next_mode = Mode.PLANT_DISP if not curr_mode == Mode.PLANT_DISP else Mode.CLOCK_DISP
    else:
        next_mode = curr_mode

    # State transition logic
    if next_mode != curr_mode:
        if next_mode == Mode.CLOCK_SET:
            newtime = clock.get_time()
        elif next_mode == Mode.ALARM_SET:
            newalarm == clock.get_alarm()
        elif curr_mode == Mode.CLOCK_SET:
            clock.set_time(newtime)
        elif curr_mode == Mode.ALARM_SET:
            clock.set_alarm(newalarm)

    # Mutate state
    curr_mode = next_mode


loop_timer.init(mode=Timer.PERIODIC, freq=UPDATE_FREQ, callback=update)

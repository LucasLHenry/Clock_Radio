from clock_class import Clock
from math import floor
from machine import Timer
from settings_lib import UPDATE_FREQ

clock = Clock()
clock.set_time(4, 0)
clock.set_alarm(4, 1)
loop_timer = Timer()
alarm_triggered = False

def display_time(clock):
    time = clock.get_time()
    hour = floor(time[0])
    minute = floor(time[1])
    print(f"{hour:02}:{minute:02}")

def update(_timer):
    global alarm_triggered
    clock.pass_time(1/UPDATE_FREQ)
    if clock.get_alarm() == clock.get_time() and not alarm_triggered:
        print("ALARM")
        alarm_triggered = True
    display_time(clock)

loop_timer.init(mode=Timer.PERIODIC, freq=UPDATE_FREQ, callback=update)
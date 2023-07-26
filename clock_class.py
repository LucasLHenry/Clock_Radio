from machine import RTC
from settings_lib import CLOCK_START_DATETIME
from math import floor

# simple wrapper for the machine.RTC class, allows parsing and the ability to set an alarm
# however, this is not a real alarm, it just stores a time. So it must be checked externally
# whether or not the alarm has gone off
class Clock:
    def __init__(self):
        self.time = 0 # (hour, minute)
        self.alarm = (0, 0)

    # does some checking to make sure everything's a valid time, then plugs it in
    def set_alarm(self, alarm_hour, alarm_minute):
        self.alarm = (alarm_hour, alarm_minute)
    
    # not necessarily needed, but maintains parallelism with get_time
    def get_alarm(self):
        return self.alarm
    
    # same as set_alarm, does some checking and then plugs it in
    def set_time(self, hour, minute):
        self.time = hour*3600 + minute*60

    def pass_time(self, interval):
        if self.time >= 24*3600:
            self.time = 0
        else:
            self.time += interval

    def get_time(self):
        hour = floor(self.time/3600)
        minute = floor((self.time-hour*3600)/60)
        return (hour, minute)

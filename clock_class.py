from machine import RTC
from settings_lib import CLOCK_START_DATETIME

# simple wrapper for the machine.RTC class, allows parsing and the ability to set an alarm
# however, this is not a real alarm, it just stores a time. So it must be checked externally
# whether or not the alarm has gone off
class Clock():
    def __init__(self):
        self.rtc = RTC()
        self.rtc.datetime(CLOCK_START_DATETIME)
        self.alarm = (0, 0) # (hour, minute)
    

    # does some checking to make sure everything's a valid time, then plugs it in
    def set_alarm(self, alarm_hour, alarm_minute):
        if not (isinstance(alarm_hour, int) or isinstance(alarm_minute, int)):
            return False
        if alarm_hour < 0 or alarm_hour > 23 or alarm_minute < 0 or alarm_minute > 59:
            return False
        self.alarm = (alarm_hour, alarm_minute)
    
    # not necessarily needed, but maintains parallelism with get_time
    def get_alarm(self):
        return self.alarm
    
    # same as set_alarm, does some checking and then plugs it in
    def set_time(self, hour, minute):
        if not (isinstance(hour, int) or isinstance(minute, int)):
            return False
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return False
        (year, month, day, _, _, second, microsecond, tzinfo) = self.rtc.datetime()
        self.rtc.datetime((year, month, day, hour, minute, second, microsecond, tzinfo))

    def get_time(self):
        (_, _, _, _, hour, minute, _, _) = self.rtc.datetime()
        return (hour, minute)
    
    # checks whether or not the current time is greater than the alarm time
    def alarm_pending(self):
        (hour, minute) = self.get_time()
        if hour > self.alarm[0] or (hour == self.alarm[0] and minute >= self.alarm[1]):
            return True
        return False
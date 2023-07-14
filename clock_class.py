from machine import RTC
from settings_lib import CLOCK_START_DATETIME

class Clock():
    def __init__(self):
        self.rtc = RTC()
        self.rtc.datetime(CLOCK_START_DATETIME)
        self.alarm = (0, 0) # (minute, second)
        self.alarm_on = False

    def parse_datetime(self):
        (_, _, _, _, hour, minute, second, _) = self.rtc.datetime()
        return (hour, minute, second)
    
    def get_time_str(self):
        (hour, minute, _) = self.parse_datetime()
        return "{:d}:{:02d}".format(hour, minute)
    
    def set_alarm(self, alarm_hour, alarm_minute):
        if not (isinstance(alarm_hour, int) or isinstance(alarm_minute, int)):
            return False
        if alarm_hour < 0 or alarm_hour > 23 or alarm_minute < 0 or alarm_minute > 59:
            return False
        self.alarm = (alarm_hour, alarm_minute)
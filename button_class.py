from machine import Pin, Timer
from settings_lib import BUTTON_DOWNTIME_MS, BUTTON_HOLDTIME_MS


class Button:
    def _timer_end(self, timer):
        self.pin.irq(handler=self._handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
    
    def _holdtimer_end(self, timer):
        self.held_db = True

    def _handler(self, pin):
        val = self.pin.value()
        self.pin.irq(handler=None)
        if val == 0: # low value, so with pullup resistor it is pressed, therefore falling edge
            self.db = True
            self.holdtimer.init(mode=Timer.ONE_SHOT, period=BUTTON_HOLDTIME_MS, callback=self._holdtimer_end)
        else:
            self.holdtimer.deinit()
        self.waittimer.init(mode=Timer.ONE_SHOT, period=BUTTON_DOWNTIME_MS, callback=self._timer_end)

    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN)
        self.waittimer = Timer()
        self.holdtimer = Timer()
        self.db = False
        self.held_db = False
        self.pin.irq(handler=self._handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def get(self):
        to_send = (self.db, self.held_db)
        (self.db, self.held_db) = (False, False)
        return to_send
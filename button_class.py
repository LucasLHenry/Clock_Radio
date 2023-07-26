from machine import Pin, Timer
from settings_lib import BUTTON_DOWNTIME_MS, BUTTON_HOLDTIME_MS


class Button:
    def _timer_end(self, timer):
        self.pin.irq(handler=self._handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
    
    def _holdtimer_end(self, timer):
        if self.pin.value() == 0:
            self.held_db = True
            self.press_gate = False

    # the debounce logic is as follows:
    #   on interrupt, set internal value to correct value as read from pin
    #   shut off interrupts
    #   set a timer for BUTTON_DOWNTIME_MS milliseconds, and call _timer_end once it's over
    #   _timer_end reattaches interrupts.
    # This means that only one interrupt can be called within a certain period

    # Additionally, there is logic for detecting a held button as well. When the button is
    # pressed down, set a timer for BUTTON_HOLDTIME_MS. If the button is released before it
    # goes off, the timer is shut off. If it isn't released, the value is checked and as
    # logn as it's still high the hold doorbell is set.
    def _handler(self, pin):
        val = self.pin.value()
        self.pin.irq(handler=None)
        if val == 0: # low value, so with pullup resistor it is pressed, therefore falling edge
            self.press_gate = True
            self.holdtimer.init(mode=Timer.ONE_SHOT, period=BUTTON_HOLDTIME_MS, callback=self._holdtimer_end)
        else:
            self.holdtimer.deinit()
            self.db = self.press_gate
        self.waittimer.init(mode=Timer.ONE_SHOT, period=BUTTON_DOWNTIME_MS, callback=self._timer_end)

    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN)
        self.waittimer = Timer()
        self.holdtimer = Timer()
        self.press_gate = False
        self.db = False
        self.held_db = False
        self.pin.irq(handler=self._handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

    # these values are doorbells, so will get reset once they're read
    # means only one reading is available at a time
    def get(self):
        to_send = self.db
        self.db = False
        return to_send

    def get_held(self):
        to_send = self.held_db
        self.held_db = False
        return to_send

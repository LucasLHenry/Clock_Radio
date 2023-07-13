from machine import Pin


class Encoder:
    def _handle_interrupt(self):
        if self.PinB.value() == 1:
            self.val += 1
        else:
            self.val -= 1


    def __init__(self, pin_a, pin_b):
        self.PinA = Pin(pin_a, Pin.IN)
        self.PinB = Pin(pin_b, Pin.IN)
        self.PinA.irq(handler=self._handle_interrupt, trigger=Pin.IRQ_FALLING)
        self.val = 0
    
    def get(self):
        to_send = self.val
        self.val = 0
        return to_send
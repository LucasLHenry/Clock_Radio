from machine import Pin
from settings_lib import ENCODER_DIR_CHANGE_MARGIN


class Encoder:
    def _disable_irq(self):
        self.PinA.irq(handler=None)
        self.PinB.irq(handler=None)
    
    # declared here so that _enable_irq can reference them
    def _handle_A(self): pass
    def _handle_B(self): pass
    
    def _enable_irq(self):
        self.PinA.irq(handler=self._handle_A, trigger=Pin.IRQ_RISING)
        self.PinB.irq(handler=self._handle_B, trigger=Pin.IRQ_RISING)

    def __init__(self, pin_a, pin_b):
        self.PinA = Pin(pin_a, Pin.IN)
        self.PinB = Pin(pin_b, Pin.IN)
        self._enable_irq()
        self.aFlag = False
        self.bFlag = False
        self.val = 0
        self.direction = 0 # positive for CW, negative for CCW
        self.DIR_CHANGE_MARGIN = ENCODER_DIR_CHANGE_MARGIN # threshold to reach for direction changes
    
    def _handle_A(self, pin): # pin is a dummy value that isn't needed, but gets passed by the IRQ
        self._disable_irq() # so that nothing interrupts the interrupt
        aVal = self.PinA.value()
        bVal = self.PinB.value()
        if aVal == 0 and bVal == 0 and self.aFlag: # B is already down and we're expecting A
            # this direction change code is to make sure that you need a bunch of incorrect
            # directions in a row before you can start affecting the value. Also means that
            # there is a dead zone when purposefully changing the encoder rotation direction
            if self.direction >= self.DIR_CHANGE_MARGIN:
                self.val += 1
            else:
                self.direction += 1
                
            self.bFlag = False
            self.aFlag = False
        elif aVal == 1 and bVal == 0: # B down but A up, so expect B
            self.bFlag = True
        self._enable_irq()
    
    # see comments on _handle_A for explanation of this code, it's reciprocal
    def _handle_B(self, pin): # pin is a dummy value that isn't needed, but gets passed by the IRQ
        self._disable_irq()
        aVal = self.PinA.value()
        bVal = self.PinB.value()
        if aVal == 0 and bVal == 0 and self.bFlag:
            if self.direction <= -self.DIR_CHANGE_MARGIN:
                self.val -= 1
            else:
                self.direction -= 1   
            self.bFlag = False
            self.aFlag = False
        elif aVal == 0 and bVal == 1:
            self.aFlag = True
        self._enable_irq()
    
    # send out current value, clearing it
    def get(self):
        to_send = self.val
        self.val = 0
        return to_send
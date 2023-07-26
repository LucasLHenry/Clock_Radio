from machine import Pin

# you can configure a callback which will be called whenever the value changes.
class Encoder:

    def __init__(self, leftPin, rightPin, callback=None):
        self.leftPin = Pin(leftPin, Pin.IN)
        self.rightPin = Pin(rightPin, Pin.IN)
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        self.leftPin.irq(handler=self.transitionOccurred, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
        self.rightPin.irq(handler=self.transitionOccurred, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def transitionOccurred(self, channel):
        p1 = self.leftPin.value()
        p2 = self.rightPin.value()
        newState = "{}{}".format(p1, p2)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        self.state = newState

    def get(self):
        to_send = self.value
        self.value = 0
        return -to_send

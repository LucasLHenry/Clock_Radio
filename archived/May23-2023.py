import time
import machine

counter = 0
# button connected
button_pin = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)
# forever, if the button is pressed, increment the counter and print
# out it's value, then wait for 2 seconds
while True:
    if button_pin.value() == 1:
        counter += 1
        print(counter)
        time.sleep(2)

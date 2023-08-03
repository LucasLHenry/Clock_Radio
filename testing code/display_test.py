from display_class import Display

disp = Display()

while True:
    disp.oled.fill(0)
    disp.text_varsize("hello", 0, 0, 3)
    disp.text_varsize("smaller", 0, 5, 0.5)
    disp.oled.show()
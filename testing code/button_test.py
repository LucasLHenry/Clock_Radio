from button_class import Button

btn = Button(0)

while True:
    val = btn.get()
    if val == 1:
        print("pressed")
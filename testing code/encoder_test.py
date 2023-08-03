from encoder_class import Encoder

enc = Encoder(14, 15)
val = 0

while True:
    new_val = enc.get()
    if not new_val == 0:
        val += new_val
        print(new_val)
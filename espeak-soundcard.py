import os
import subprocess


def speak_to_card(text, card="hw:wm8960soundcard,0"):
    # Use espeak with aplay to target specific sound card
    command = f'espeak "{text}" --stdout | aplay -D {card}'
    os.system(command)


# Test it
speak_to_card("Hello from the wm8960 sound card!", "hw:wm8960soundcard,0")
speak_to_card("This is using the USB speaker!", "hw:UACDemoV10,0")

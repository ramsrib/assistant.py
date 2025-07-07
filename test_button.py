from gpiozero import Button

button = Button(23)

def on_press():
    print("Button was pressed!")

button.when_pressed = on_press

print("Waiting for button press on GPIO23. Press CTRL+C to exit.")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")

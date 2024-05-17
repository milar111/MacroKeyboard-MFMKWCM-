import time
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Define GP pins for the rotary encoder and button
encoder_pins = [board.GP15, board.GP14]
button_pin = board.GP13

# Initialize rotary encoder pins
pin_a = digitalio.DigitalInOut(encoder_pins[0])
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP

pin_b = digitalio.DigitalInOut(encoder_pins[1])
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

# Initialize button pin
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initialize ConsumerControl for media key emulation
cc = ConsumerControl(usb_hid.devices)


last_a = None
last_b = None
encoder_count = 0

# Function to handle volume change
def change_volume(direction):
    if direction == 1:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    else:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)

# Main loop to read rotary encoder and button
while True:
    a_state = pin_a.value
    b_state = pin_b.value

    if last_a is None or last_b is None:
        last_a = a_state
        last_b = b_state
    else:
        if a_state != last_a or b_state != last_b:
            if a_state != last_a:
                if a_state != b_state:
                    encoder_count += 1
                    change_volume(1)  # Increase volume
                else:
                    encoder_count -= 1
                    change_volume(-1)  # Decrease volume
            else:
                if a_state == b_state:
                    encoder_count += 1
                    change_volume(1)  # Increase volume
                else:
                    encoder_count -= 1
                    change_volume(-1)  # Decrease volume

            last_a = a_state
            last_b = b_state

    # Check if the button is pressed
    if not button.value:
        cc.send(ConsumerControlCode.MUTE)
        while not button.value: 
            pass

    time.sleep(0.01)  
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Define GP pins for the keyboard
row_pins = [board.GP4, board.GP5, board.GP6]
col_pins = [board.GP9, board.GP10, board.GP11]

# Initialize rows and columns
rows = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row in rows:
    row.direction = digitalio.Direction.INPUT
    row.pull = digitalio.Pull.DOWN

cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col in cols:
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP

# Define keymap for the keyboard
keymap = [
    [Keycode.ONE, Keycode.TWO, Keycode.THREE],
    [Keycode.FOUR, Keycode.FIVE, Keycode.SIX],
    [Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE]
]

# Initialize USB HID keyboard
kbd = Keyboard(usb_hid.devices)

# Initialize rotary encoder and button pins
encoder_pins = [board.GP15, board.GP14]
button_pin = board.GP13

pin_a = digitalio.DigitalInOut(encoder_pins[0])
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP

pin_b = digitalio.DigitalInOut(encoder_pins[1])
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initialize ConsumerControl for media key emulation
cc = ConsumerControl(usb_hid.devices)

INITIAL_DELAY = 0.5  # Initial delay before repeating characters (seconds)
REPEAT_DELAY = 0.1   # Delay between repeated characters (seconds)
REPEAT_RATE = 10     # Number of characters repeated per second

last_key = None
last_key_time = 0
last_a = None
last_b = None
encoder_count = 0

def scan_keyboard():
    for i in range(3):
        for j in range(3):
            cols[j].direction = digitalio.Direction.OUTPUT
            cols[j].value = True
            if rows[i].value:
                cols[j].direction = digitalio.Direction.INPUT
                return keymap[i][j]
            cols[j].direction = digitalio.Direction.INPUT
    return None

def change_volume(direction):
    if direction == 1:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    else:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)

while True:
    key = scan_keyboard()
    current_time = time.monotonic()

    if key:
        if key != last_key:
            kbd.send(key)
            last_key = key
            last_key_time = current_time
        else:
            if current_time - last_key_time >= INITIAL_DELAY:
                if (current_time - last_key_time - INITIAL_DELAY) % (1 / REPEAT_RATE) < REPEAT_DELAY:
                    kbd.send(key)
    else:
        last_key = None

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

    if not button.value:
        cc.send(ConsumerControlCode.MUTE)
        while not button.value:
            pass

    time.sleep(0.01)


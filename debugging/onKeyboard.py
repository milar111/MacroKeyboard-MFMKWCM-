import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

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

INITIAL_DELAY = 0.5  # Initial delay before repeating characters (seconds)
REPEAT_DELAY = 0.1   # Delay between repeated characters (seconds)
REPEAT_RATE = 10     # Number of characters repeated per second

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


# Main loop to scan the keyboard and print numbers
last_key = None
last_key_time = 0

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

    time.sleep(0.05)


import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

row_pins = [board.GP4, board.GP5, board.GP6]
col_pins = [board.GP7, board.GP8, board.GP9]

rows = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row in rows:
    row.direction = digitalio.Direction.INPUT
    row.pull = digitalio.Pull.DOWN

cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col in cols:
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP

keymap = [
    [Keycode.ONE, Keycode.TWO, Keycode.THREE],
    [Keycode.FOUR, Keycode.FIVE, Keycode.SIX],
    [Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE]
]

key_pressed = {}

kbd = Keyboard(usb_hid.devices)

def scan_keyboard():
    for i in range(3):
        for j in range(3):
            cols[j].direction = digitalio.Direction.OUTPUT
            cols[j].value = True
            if rows[i].value:
                if not key_pressed.get((i, j), False):
                    key_pressed[(i, j)] = True
                    cols[j].direction = digitalio.Direction.INPUT
                    return keymap[i][j]
            else:
                key_pressed[(i, j)] = False
            cols[j].direction = digitalio.Direction.INPUT
    return None

while True:
    key = scan_keyboard()
    if key:
        kbd.send(key)
    time.sleep(0.1)


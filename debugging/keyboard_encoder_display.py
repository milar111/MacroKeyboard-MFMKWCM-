import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import rtc
import adafruit_imageload
import terminalio
import microcontroller
import displayio
import busio

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
        
        
IMAGE_FILE = "pacman.bmp"
SPRITE_SIZE = (32, 32)
FRAMES = 28

def invert_colors(palette):
    palette[0], palette[1] = palette[1], palette[0]

displayio.release_displays()

sda, scl = board.GP16, board.GP17
i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

splash = displayio.Group()
display.show(splash)

temperature_text = label.Label(terminalio.FONT, text="Temp: 0°C", color=0xFFFFFF) 
temperature_text.x = 0
temperature_text.y = 25 
splash.append(temperature_text)

time_text = label.Label(terminalio.FONT, text="00:00:00", color=0xFFFFFF) 
time_text.x = 0
time_text.y = 5  
splash.append(time_text)

date_text = label.Label(terminalio.FONT, text="01/01/2000", color=0xFFFFFF) 
date_text.x = 0
date_text.y = 15 
splash.append(date_text)

icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE, bitmap=displayio.Bitmap, palette=displayio.Palette)
invert_colors(icon_pal)

icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal, width=1, height=1, tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0], default_tile=0, x=90, y=0)
splash.append(icon_grid)

rtc_r = rtc.RTC()
pointer = 0     
        
oled_update_time = time.monotonic()
encoder_check_time = time.monotonic()
frame_update_time = time.monotonic()  # Timer for animation frame updates
frame = 0  # Initial frame for the animation
FRAME_INTERVAL = 0.1  # Interval for animation frame updates (seconds)
        
while True:
    current_time = time.monotonic()
    
    key = scan_keyboard()

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

    # Update the display every second
    if current_time - oled_update_time >= 1:
        now = rtc_r.datetime
        time_text.text = "{:02}:{:02}:{:02}".format(now.tm_hour, now.tm_min, now.tm_sec)
        date_text.text = "{:02}/{:02}/{:04}".format(now.tm_mday, now.tm_mon, now.tm_year)
        temperature_text.text = "Temp: {:.1f}°C".format(microcontroller.cpu.temperature)
        oled_update_time = current_time

    if current_time - frame_update_time >= FRAME_INTERVAL:
        icon_grid[0] = frame
        frame = (frame + 1) % FRAMES
        frame_update_time = current_time

    time.sleep(0.01)


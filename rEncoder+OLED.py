import time
import board
import digitalio
import busio
import displayio
import adafruit_displayio_ssd1306
import adafruit_imageload
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

S1_PIN = board.GP15
S2_PIN = board.GP14
KEY_PIN = board.GP12

s1_button = digitalio.DigitalInOut(S1_PIN)
s1_button.direction = digitalio.Direction.INPUT
s1_button.pull = digitalio.Pull.UP

s2_button = digitalio.DigitalInOut(S2_PIN)
s2_button.direction = digitalio.Direction.INPUT
s2_button.pull = digitalio.Pull.UP

key_button = digitalio.DigitalInOut(KEY_PIN)
key_button.direction = digitalio.Direction.INPUT
key_button.pull = digitalio.Pull.UP

cc = ConsumerControl(usb_hid.devices)

def send_key(key):
    cc.send(key)
    time.sleep(0.1)

IMAGE_FILE = "skateboarding.bmp"
SPRITE_SIZE = (64, 64)
FRAMES = 28

def invert_colors(palette):
    palette[0], palette[1] = palette[1], palette[0]

displayio.release_displays()

i2c = busio.I2C(board.GP17, board.GP16)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

group = displayio.Group()

icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE, bitmap=displayio.Bitmap, palette=displayio.Palette)
invert_colors(icon_pal)

icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal, width=1, height=1, tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0], default_tile=0, x=32, y=0)
group.append(icon_grid)

display.show(group)

timer = 0
pointer = 0

while True:
    if not s1_button.value:
        send_key(ConsumerControlCode.VOLUME_DECREMENT)
        while not s1_button.value:
            pass 
    if not s2_button.value:
        send_key(ConsumerControlCode.VOLUME_INCREMENT)
        while not s2_button.value:
            pass  
    if not key_button.value:
        send_key(ConsumerControlCode.MUTE)
        while not key_button.value:
            pass 
            
    if (timer + 0.1) < time.monotonic():
        icon_grid[0] = pointer
        pointer = (pointer + 1) % FRAMES
        timer = time.monotonic()

import board
import busio
import displayio
import os
import terminalio
import microcontroller
import time
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import rtc
import adafruit_imageload
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

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

S1_PIN = board.GP15
S2_PIN = board.GP14
KEY_PIN = board.GP13

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

oled_update_time = time.monotonic()
encoder_check_time = time.monotonic()

while True:
    if time.monotonic() - oled_update_time >= 0.1: 
        temperature = round(microcontroller.cpu.temperature - 5, 1) 
        temperature_string = f"{temperature}°C"
        temperature_text.text = "Temp:" + temperature_string

        current_time = rtc_r.datetime
        time_string = "{:02d}:{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec)
        time_text.text = "Time:" + time_string

        date_string = "{:02d}/{:02d}/{:02d}".format(current_time.tm_mday, current_time.tm_mon, current_time.tm_year % 100)
        date_text.text = "Date:" + date_string

        icon_grid[0] = pointer
        pointer = (pointer + 1) % FRAMES

        oled_update_time = time.monotonic()

    if time.monotonic() - encoder_check_time >= 0.01: 
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

        encoder_check_time = time.monotonic()


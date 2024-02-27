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

temperature = 0
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

rtc_r = rtc.RTC()
while True:
    temperature = round(microcontroller.cpu.temperature - 4, 1) 
    temperature_string = f"{temperature}°C"
    temperature_text.text = "Temp:" + temperature_string

    current_time = rtc_r.datetime
    time_string = "{:02d}:{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec)
    time_text.text = "Time:" + time_string

    date_string = "{:02d}/{:02d}/{:02d}".format(current_time.tm_mday, current_time.tm_mon, current_time.tm_year % 100)
    date_text.text = "Date:" + date_string

    time.sleep(1)


from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import utime
import math

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)

oled_width = 128
oled_height = 32
display = SSD1306_I2C(oled_width, oled_height, i2c)

def draw_filled_circle(x0, y0, radius):
    for y in range(y0 - radius, y0 + radius + 1):
        for x in range(x0 - radius, x0 + radius + 1):
            if (x - x0) ** 2 + (y - y0) ** 2 <= radius ** 2:
                display.pixel(x, y, 1)

def get_current_time():
    current_time = utime.localtime()
    time_str = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    return time_str

def get_current_date():
    current_time = utime.localtime()
    date_str = "{:02d}-{:02d}-{:02d}".format(current_time[2], current_time[1], current_time[0] % 100)
    return date_str

def read_temp():
    sensor_temp = ADC(4)
    conversion_factor = 3.3 / 65535
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    formatted_temperature = "{:.1f}".format(temperature - 2.5)
    string_temperature = "Temp:" + formatted_temperature
    return string_temperature

while True:
    current_time = get_current_time()
    current_date = get_current_date()
    temperature = read_temp()
    display.fill(0)  # Clear display buffer
    display.text(current_time, 0, 0)
    display.text(current_date, 0, 12)
    display.text(temperature, 0, 24)
    draw_filled_circle(100, 16, 16)  # Drawing filled circle
    display.show()
    utime.sleep(1)  # Delay before updating again


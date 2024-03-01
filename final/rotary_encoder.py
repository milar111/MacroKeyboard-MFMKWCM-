import rtc
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

rtc_r = rtc.RTC()
pointer = 0

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

def handle_input():
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
    time.sleep(0.01) 

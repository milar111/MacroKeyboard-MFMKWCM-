# MacroKeyboard-MFMKWCM-
End term project in Micro/Circuit Python. TUES# OLED Display and USB HID Keyboard Controller

This project combines a USB HID keyboard and an OLED display to create a versatile tool with several functionalities.

## Features

1. **Custom Keypad Interface**
   - Uses a 3x3 matrix keypad with predefined key mappings.
   - Each key can be programmed to send specific keystrokes, open URLs, or launch applications when pressed.

2. **OLED Display**
   - Displays real-time information such as temperature, time, and date.
   - Supports custom images and animations.
   - Includes a built-in Dino game activated by a double-click of a button.

3. **Volume Control with Rotary Encoder**
   - A rotary encoder is used to adjust the system volume.
   - The encoder can increase or decrease volume and mute the audio with a button press.

4. **Dino Game**
   - A simple Dino game is included, displayed on the OLED.
   - Controlled via the keypad and includes jumping mechanics and score tracking.

## Components Used

- **Microcontroller**: Any microcontroller compatible with CircuitPython and USB HID.
- **OLED Display**: SSD1306 128x32 pixel OLED display.
- **Keypad**: 3x3 matrix keypad.
- **Rotary Encoder**: With a push button.
- **Temperature Sensor**: Reads and displays CPU temperature.

## Libraries Required

- `time`, `board`, `digitalio`, `usb_hid`
- `adafruit_hid.keyboard`, `adafruit_hid.keycode`, `adafruit_hid.consumer_control`, `adafruit_hid.consumer_control_code`
- `adafruit_displayio_ssd1306`, `adafruit_display_text`, `rtc`, `adafruit_imageload`, `terminalio`, `microcontroller`, `displayio`, `busio`
- `adafruit_display_shapes.rect`

## Setup Instructions

1. **Connect the Components**:
   - Wire the keypad to the specified GPIO pins.
   - Connect the OLED display via I2C.
   - Attach the rotary encoder and button to the designated pins.

2. **Install CircuitPython Libraries**:
   - Ensure all necessary CircuitPython libraries are installed on your device.

3. **Load the Code**:
   - Upload the provided Python script to your microcontroller.

4. **Run the Script**:
   - Power up your device to start using the keyboard controller and display features.

## Usage

- **Keypad**: Press keys to perform specific actions (open apps, URLs).
- **Rotary Encoder**: Rotate to adjust volume, press to mute.
- **OLED Display**: View time, date, temperature, and play the Dino game.

This project demonstrates a versatile way to combine input devices and displays to create an interactive and multifunctional tool. Enjoy experimenting and expanding its capabilities!


## Images
![image](https://github.com/user-attachments/assets/ac6ef4c2-e951-485e-95fb-2e33af029d0c)
![image](https://github.com/user-attachments/assets/6cfa5408-9d3b-4e8c-a84d-f2dd78f0c529)
![image](https://github.com/user-attachments/assets/f8262554-ed17-43fc-8ed7-3d8ea6a1f128)



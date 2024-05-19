import time
import board
import displayio
import digitalio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import adafruit_displayio_ssd1306
import busio


displayio.release_displays()
i2c = busio.I2C(scl=board.GP17, sda=board.GP16)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

row_pins = [board.GP4, board.GP5, board.GP6]
col_pins = [board.GP9, board.GP10, board.GP11]

rows = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row in rows:
    row.direction = digitalio.Direction.INPUT
    row.pull = digitalio.Pull.DOWN

cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col in cols:
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP

def scan_keyboard():
    for i in range(3):
        for j in range(3):
            cols[j].direction = digitalio.Direction.OUTPUT
            cols[j].value = True
            if rows[i].value:
                cols[j].direction = digitalio.Direction.INPUT
                return True
            cols[j].direction = digitalio.Direction.INPUT
    return False


splash = displayio.Group()
display.show(splash)

#Dino
dino = Rect(10, 24, 8, 8, fill=0xFFFFFF)
splash.append(dino)

#Obstacle
obstacle = Rect(120, 24, 8, 8, fill=0xFFFFFF)
splash.append(obstacle)

#Score
score_label = label.Label(terminalio.FONT, text="Score: 0", color=0xFFFFFF, x=5, y=5)
splash.append(score_label)

dino_y_velocity = 0
dino_jump = -5
gravity = 0.3
obstacle_speed = 1
score = 0
is_jumping = False

while True:
    if scan_keyboard() and not is_jumping:
        dino_y_velocity = dino_jump
        is_jumping = True


    dino_y_velocity += gravity
    dino.y += int(dino_y_velocity)

    # != falling through the ground
    if dino.y > 24:
        dino.y = 24
        dino_y_velocity = 0
        is_jumping = False

    # Move obstacle
    obstacle.x -= obstacle_speed
    if obstacle.x < -8:
        obstacle.x = 128
        score += 1
        score_label.text = f"Score: {score}"

    #CollisionCh
    if (dino.x < obstacle.x + 8 and
        dino.x + 8 > obstacle.x and
        dino.y < obstacle.y + 8 and
        dino.y + 8 > obstacle.y):
        score = 0
        obstacle.x = 128
        score_label.text = f"Score: {score}"

    display.show(splash)
    time.sleep(0.01)


import oled_display
import rotary_encoder

while True:
    oled_display.update_display()
    rotary_encoder.handle_input()

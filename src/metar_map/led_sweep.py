import time
from .layout import load_layout
from .pi_strip import create_strip


def run():
    layout = load_layout()
    strip, Color = create_strip(layout.led_count)

    print("Starting LED sweep...")

    while True:
        for i in range(layout.led_count):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()
            print(f"LED {i}")
            time.sleep(0.4)
            strip.setPixelColor(i, Color(0, 0, 0))

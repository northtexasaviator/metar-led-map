import os
import sys
import time

sys.path.insert(0, "/home/pi3/metar-led-map/src")

from metar_map.layout import load_layout
from metar_map.pi_strip import create_strip

layout = load_layout()
strip, Color = create_strip(layout.led_count)

green = Color(0, 255, 0)

for i in range(layout.led_count):
    strip.setPixelColor(i, green)

strip.show()

print(f"Set {layout.led_count} LEDs to green. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    pass

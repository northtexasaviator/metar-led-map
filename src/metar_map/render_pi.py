from __future__ import annotations

import math
import time

from .renderer import Renderer
from .model import LedState
from .pi_strip import create_strip


def _pulse_scale(period_s: float = 1.2, min_scale: float = 0.35) -> float:
    """
    Smooth pulse between min_scale..1.0.
    """
    t = time.monotonic()
    phase = (t % period_s) / period_s                  # 0..1
    s = (math.sin(phase * 2 * math.pi) + 1.0) / 2.0   # 0..1
    return min_scale + (1.0 - min_scale) * s


class PiRenderer(Renderer):
    def __init__(self, layout):
        super().__init__(layout)
        self.strip, self.Color = create_strip(layout.led_count)

        # Clear once at startup
        for i in range(layout.led_count):
            self.strip.setPixelColor(i, self.Color(0, 0, 0))
        self.strip.show()

    def _cat_to_rgb(self, flt_cat: str | None) -> tuple[int, int, int]:
        if not flt_cat:
            return (0, 0, 0)

        cat = flt_cat.upper()
        if cat == "VFR":
            return (0, 255, 0)      # green
        if cat == "MVFR":
            return (0, 0, 255)      # blue
        if cat == "IFR":
            return (255, 0, 0)      # red
        if cat == "LIFR":
            return (255, 0, 255)    # magenta

        return (0, 0, 0)

    def render(self, state: LedState) -> None:
        idx = self.layout.mapping.get(state.airport)
        if idx is None:
            return

        r, g, b = self._cat_to_rgb(state.flt_cat)

        # Wind pulsing for sustained wind > 15kt
        if state.wind_spd is not None and state.wind_spd > 15:
            scale = _pulse_scale(period_s=1.2, min_scale=0.35)
            r = int(r * scale)
            g = int(g * scale)
            b = int(b * scale)

        # Apply sunset brightness dimming
        brightness = state.brightness_multiplier
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)

        self.strip.setPixelColor(idx, self.Color(r, g, b))

    def flush(self) -> None:
        self.strip.show()
import os
import time

from .config import load_airports, load_airport_coords
from .layout import load_layout
from .metar_fetch import get_metars
from .translate import metar_to_state
from .model import LedState
from .sunset import get_sunset_brightness_multiplier

from .render_sim import SimRenderer
from .render_pi import PiRenderer


def run():
    mode = os.getenv("METAR_MODE", "sim").lower()  # sim | pi

    metar_refresh_s = int(os.getenv("METAR_REFRESH_S", "60"))
    frame_refresh_s = float(os.getenv("FRAME_REFRESH_S", "0.25"))
    target_brightness = float(os.getenv("NIGHT_BRIGHTNESS", "0.5"))  # Min brightness at night (0.0-1.0)
    
    # Test mode: force brightness alternating (for testing without waiting for actual sunset/sunrise)
    test_mode = os.getenv("TEST_BRIGHTNESS", "").lower() == "true"

    airports = load_airports()
    airport_coords = load_airport_coords()
    layout = load_layout()

    renderer = PiRenderer(layout) if mode == "pi" else SimRenderer(layout)

    # last-known states (so we can animate between fetches)
    states_by_airport: dict[str, LedState] = {}

    next_fetch = 0.0

    while True:
        now = time.monotonic()

        if now >= next_fetch:
            metars = get_metars(airports)

            # Treat None OR empty dict as a batch failure.
            # (An empty response for 50 airports is not a "real" state; it's an outage/timeout.)
            if not metars:
                print("METAR fetch failed/empty; keeping last-known states")
                next_fetch = now + metar_refresh_s
            else:
                for idx, a in enumerate(airports):
                    metar = metars.get(a)
                    
                    # Calculate brightness multiplier based on sunset
                    brightness = 1.0
                    
                    if test_mode:
                        # TEST MODE: Alternate between full brightness (100%) and dim (20%)
                        # This lets you see the difference without waiting for sunset/sunrise
                        brightness = 1.0 if idx % 2 == 0 else target_brightness
                    elif a in airport_coords:
                        lat, lon = airport_coords[a]
                        try:
                            brightness = get_sunset_brightness_multiplier(lat, lon, target_brightness=target_brightness)
                        except Exception as e:
                            print(f"Error calculating sunset for {a}: {e}")
                            brightness = 1.0
                    
                    if not metar:
                        # Per-airport missing METAR => LED OFF (avoid stale/false display)
                        states_by_airport[a] = LedState(
                            airport=a,
                            flt_cat=None,
                            wind_dir=None,
                            wind_spd=None,
                            wind_gust=None,
                            lightning=False,
                            brightness_multiplier=brightness,
                        )
                    else:
                        state = metar_to_state(a, metar)
                        # Add sunset brightness multiplier to the state
                        states_by_airport[a] = LedState(
                            airport=state.airport,
                            flt_cat=state.flt_cat,
                            wind_dir=state.wind_dir,
                            wind_spd=state.wind_spd,
                            wind_gust=state.wind_gust,
                            lightning=state.lightning,
                            brightness_multiplier=brightness,
                        )

                next_fetch = now + metar_refresh_s

        # render a frame
        for a in airports:
            state = states_by_airport.get(a)
            if state is None:
                continue
            renderer.render(state)

        renderer.flush()
        time.sleep(frame_refresh_s)
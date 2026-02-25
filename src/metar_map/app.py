import os
import time

from .config import load_airports
from .layout import load_layout
from .metar_fetch import get_metars
from .translate import metar_to_state
from .model import LedState

from .render_sim import SimRenderer
from .render_pi import PiRenderer


def run():
    mode = os.getenv("METAR_MODE", "sim").lower()  # sim | pi

    metar_refresh_s = int(os.getenv("METAR_REFRESH_S", "60"))
    frame_refresh_s = float(os.getenv("FRAME_REFRESH_S", "0.25"))

    airports = load_airports()
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
                for a in airports:
                    metar = metars.get(a)
                    if not metar:
                        # Per-airport missing METAR => LED OFF (avoid stale/false display)
                        states_by_airport[a] = LedState(
                            airport=a,
                            flt_cat=None,
                            wind_dir=None,
                            wind_spd=None,
                            wind_gust=None,
                            lightning=False,
                        )
                    else:
                        states_by_airport[a] = metar_to_state(a, metar)

                next_fetch = now + metar_refresh_s

        # render a frame
        for a in airports:
            state = states_by_airport.get(a)
            if state is None:
                continue
            renderer.render(state)

        renderer.flush()
        time.sleep(frame_refresh_s)
import os

from .config import load_airports
from .layout import load_layout
from .metar_fetch import get_metars
from .translate import metar_to_state

from .render_sim import SimRenderer
from .render_pi import PiRenderer


def run():
    mode = os.getenv("METAR_MODE", "sim").lower()  # sim | pi

    airports = load_airports()
    layout = load_layout()

    renderer = PiRenderer(layout) if mode == "pi" else SimRenderer(layout)

    metars = get_metars(airports)

    for a in airports:
        metar = metars.get(a)
        if not metar:
            print(f"{a}: No METAR")
            continue

        state = metar_to_state(a, metar)
        renderer.render(state)

    renderer.flush()

from .config import load_airports
from .metar_fetch import get_metars
from .translate import metar_to_state
from .render_sim import render

def run():
    airports = load_airports()
    metars = get_metars(airports)

    for a in airports:
        metar = metars.get(a)
        if not metar:
            print(f"{a}: No METAR")
            continue

        state = metar_to_state(a, metar)
        render(state)

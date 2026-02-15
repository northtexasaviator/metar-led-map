from .metar_fetch import get_metar
from .translate import metar_to_state
from .render_sim import render


def run():
    airports = ["KDTO", "KDAL", "KDFW", "KGYI"]

    for a in airports:
        metar = get_metar(a)
        if not metar:
            print(f"{a}: No METAR")
            continue

        state = metar_to_state(a, metar)
        render(state)

from .metar_fetch import get_metar
from .translate import metar_to_state


def run():
    airport = "KDTO"
    metar = get_metar(airport)
    if not metar:
        print("No METAR received")
        return

    state = metar_to_state(airport, metar)
    print(state)

from .metar_fetch import get_metar


def run():
    print("METAR LED Map booting...\n")

    airport = "KDTO"  # Denton — easy test station
    metar = get_metar(airport)

    if not metar:
        print("No METAR received")
        return

    print("Airport:", airport)
    print("Flight Category:", metar.get("fltCat") or metar.get("flight_category"))
    print("Wind:", metar.get("wdir"), "@", metar.get("wspd"))
    print("Visibility:", metar.get("visib"))

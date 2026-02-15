from .model import LedState


def metar_to_state(airport: str, metar: dict) -> LedState:
    flt_cat = metar.get("fltCat") or metar.get("flight_category")

    wind_dir = metar.get("wdir")
    wind_spd = metar.get("wspd")
    wind_gust = metar.get("wgst")

    # Simple lightning flag: look for TS in present weather text fields.
    # (We’ll refine later to handle VCTS/TSRA/etc.)
    wx = " ".join([
        str(metar.get("wx", "") or ""),
        str(metar.get("rawOb", "") or ""),
    ]).upper()
    lightning = "TS" in wx

    return LedState(
        airport=airport,
        flt_cat=flt_cat,
        wind_dir=wind_dir,
        wind_spd=wind_spd,
        wind_gust=wind_gust,
        lightning=lightning,
    )

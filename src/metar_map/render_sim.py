from .model import LedState

# Simple color convention (text for now)
CAT_COLOR = {
    "VFR":  "GREEN",
    "MVFR": "BLUE",
    "IFR":  "RED",
    "LIFR": "MAGENTA",
    None:   "OFF",
}

def render(state: LedState) -> None:
    base = CAT_COLOR.get(state.flt_cat, "OFF")

    effects = []
    if state.lightning:
        effects.append("LIGHTNING")
    if state.wind_spd and state.wind_spd >= 20:
        effects.append("WIND_PULSE")
    if state.wind_gust and state.wind_gust >= 25:
        effects.append("GUST_PULSE")

    print(f"{state.airport}: {state.flt_cat or 'UNK'} -> {base}  Effects: {', '.join(effects) or 'NONE'}")

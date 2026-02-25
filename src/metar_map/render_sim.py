from .renderer import Renderer
from .model import LedState

CAT_COLOR = {
    "VFR":  "GREEN",
    "MVFR": "BLUE",
    "IFR":  "RED",
    "LIFR": "MAGENTA",
    None:   "OFF",
}

class SimRenderer(Renderer):
    def render(self, state: LedState) -> None:
        idx = self.layout.mapping.get(state.airport)
        base = CAT_COLOR.get(state.flt_cat, "OFF")

        effects = []
        if state.lightning:
            effects.append("LIGHTNING")
        if state.wind_spd and state.wind_spd >= 20:
            effects.append("WIND_PULSE")
        if state.wind_gust and state.wind_gust >= 25:
            effects.append("GUST_PULSE")
        
        brightness_pct = int(state.brightness_multiplier * 100)
        if state.brightness_multiplier < 1.0:
            effects.append(f"SUNSET_DIM({brightness_pct}%)")

        print(
            f"LED[{idx if idx is not None else '??'}] "
            f"{state.airport}: {state.flt_cat or 'UNK'} -> {base} "
            f"Effects: {', '.join(effects) or 'NONE'}"
        )

    def flush(self) -> None:
        # nothing buffered in sim
        pass

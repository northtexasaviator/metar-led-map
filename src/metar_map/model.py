from dataclasses import dataclass


@dataclass(frozen=True)
class LedState:
    airport: str
    flt_cat: str | None   # VFR/MVFR/IFR/LIFR or None
    wind_dir: int | None
    wind_spd: int | None
    wind_gust: int | None
    lightning: bool       # True if TS in wx string (simple first pass)
    brightness_multiplier: float = 1.0  # Dimming after sunset (0.5-1.0)

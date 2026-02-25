import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

def load_airports() -> list[str]:
    """Load airport codes."""
    path = CONFIG_DIR / "airports.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    airports = data.get("airports", [])
    
    # Support both old format (list of strings) and new format (list of dicts)
    if airports and isinstance(airports[0], dict):
        return [a["code"].strip().upper() for a in airports]
    else:
        return [a.strip().upper() for a in airports]

def load_airport_coords() -> dict[str, tuple[float, float]]:
    """
    Load airport coordinates as a dict mapping airport code to (lat, lon).
    
    Returns:
        Dict mapping airport code to (latitude, longitude)
    """
    path = CONFIG_DIR / "airports.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    airports = data.get("airports", [])
    
    coords = {}
    for airport in airports:
        if isinstance(airport, dict):
            code = airport["code"].strip().upper()
            coords[code] = (airport["lat"], airport["lon"])
    
    return coords

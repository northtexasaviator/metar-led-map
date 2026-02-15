import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

def load_airports() -> list[str]:
    path = CONFIG_DIR / "airports.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return [a.strip().upper() for a in data.get("airports", [])]

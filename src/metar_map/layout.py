import json
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

@dataclass(frozen=True)
class LedLayout:
    led_count: int
    mapping: dict[str, int]  # airport -> led index

def load_layout() -> LedLayout:
    path = CONFIG_DIR / "led_layout.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    led_count = int(data["led_count"])
    mapping = {k.upper(): int(v) for k, v in data["mapping"].items()}

    return LedLayout(led_count=led_count, mapping=mapping)

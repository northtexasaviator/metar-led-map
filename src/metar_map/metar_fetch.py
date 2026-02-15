import urllib.request
import json

AVIATION_WEATHER_URL = (
    "https://aviationweather.gov/api/data/metar"
    "?ids={airport}&format=json&taf=false"
)


def get_metar(airport: str) -> dict | None:
    """Fetch METAR data for a single airport."""
    url = AVIATION_WEATHER_URL.format(airport=airport.upper())

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if not data:
                return None
            return data[0]
    except Exception as e:
        print(f"METAR fetch failed for {airport}: {e}")
        return None

import urllib.request
import json

AVIATION_WEATHER_URL_MULTI = (
    "https://aviationweather.gov/api/data/metar"
    "?ids={airports}&format=json&taf=false"
)

def get_metars(airports: list[str]) -> dict[str, dict]:
    """
    Fetch METARs for multiple airports in one call.
    Returns dict keyed by airport id.
    """
    ids = ",".join(a.upper() for a in airports)
    url = AVIATION_WEATHER_URL_MULTI.format(airports=ids)

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            items = json.loads(response.read().decode())

        out: dict[str, dict] = {}
        for m in items:
            # AWC commonly returns station id under "icaoId" or "stationId" depending on schema changes.
            key = (m.get("icaoId") or m.get("stationId") or m.get("id") or "").upper()
            if key:
                out[key] = m
        return out
    except Exception as e:
        print(f"Batch METAR fetch failed: {e}")
        return {}

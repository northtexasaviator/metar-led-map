# Sunset-Based LED Dimming Feature

## Overview
This feature automatically dims the LED brightness to 50% after sunset at each airport location, creating a more realistic and less intrusive display during evening hours.

## How It Works

### Sunset Calculation
- Uses the `astral` library to calculate precise sunset times based on each airport's latitude and longitude
- Calculations are performed in UTC to ensure accuracy across time zones
- The sunset time is recalculated each day

### Brightness Dimming
- **Before sunset**: LEDs display at full brightness (100%)
- **After sunset**: LEDs gradually fade over 60 minutes
- **Final state**: LEDs stabilize at 50% brightness for the rest of the night
- Each airport's dimming is independent based on its local sunset time

### Brightness Multiplier
The brightness multiplier is calculated as:
```
- Time before sunset: multiplier = 1.0 (full brightness)
- Time after sunset: multiplier = 1.0 - (elapsed_minutes / transition_minutes) * 0.5
- After transition window: multiplier = 0.5 (50% brightness)

Where:
- elapsed_minutes = minutes since sunset
- transition_minutes = 60 (configurable in sunset.py)
```

## Configuration

### Airport Coordinates
Airport coordinates are stored in `config/airports.json` with the structure:
```json
{
  "airports": [
    {"code": "KSEA", "lat": 47.449, "lon": -122.309},
    {"code": "KPDX", "lat": 45.589, "lon": -122.598},
    ...
  ]
}
```

The system supports both old and new formats for backward compatibility.

### Customization
To adjust the sunset dimming behavior, edit `metar_map/sunset.py`:
- `target_brightness`: Minimum brightness (default: 0.5 = 50%)
- `transition_minutes`: How long to fade over (default: 60 minutes)

Example:
```python
brightness = get_sunset_brightness_multiplier(lat, lon, target_brightness=0.3, transition_minutes=30)
```

## Implementation Details

### Files Modified
1. **`metar_map/sunset.py`** (NEW)
   - `get_sunset_brightness_multiplier()`: Calculates brightness based on sunset time
   - `get_sunset_time()`: Returns the sunset time for a location

2. **`metar_map/config.py`**
   - `load_airport_coords()`: Loads airport lat/lon from config

3. **`metar_map/model.py`**
   - Added `brightness_multiplier` field to `LedState`

4. **`metar_map/app.py`**
   - Calculates sunset brightness for each airport on each METAR update
   - Applies the multiplier to LED states

5. **`metar_map/render_pi.py`**
   - Applies brightness multiplier to RGB values when rendering

6. **`metar_map/render_sim.py`**
   - Shows `SUNSET_DIM(XX%)` effect in simulation output for debugging

7. **`config/airports.json`**
   - Updated to include latitude/longitude for all airports

8. **`requirements.txt`**
   - Added `astral>=3.0` dependency

## Installation

Install the required dependency:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install astral
```

## Usage

The feature works automatically once the system is running:
```bash
cd src
python -m main          # Run with actual LEDs
METAR_MODE=sim python -m main  # Run in simulation mode
```

### Simulation Output
In simulation mode, you'll see:
```
LED[0] KSEA: VFR -> GREEN Effects: SUNSET_DIM(75%)
LED[1] KPDX: MVFR -> BLUE Effects: WIND_PULSE, SUNSET_DIM(50%)
```

## Testing

### Manual Test
```python
from metar_map.sunset import get_sunset_brightness_multiplier
from metar_map.config import load_airport_coords

# Get brightness for Seattle right now
coords = load_airport_coords()
ksea_lat, ksea_lon = coords["KSEA"]
brightness = get_sunset_brightness_multiplier(ksea_lat, ksea_lon)
print(f"Current brightness: {brightness:.2f}")
```

## Performance Considerations

- Sunset calculations are only performed once per METAR update (default: 60 seconds)
- Uses efficient astral library with minimal overhead
- No blocking I/O or network calls
- Error handling gracefully falls back to full brightness if calculation fails

## Troubleshooting

### Missing Coordinates
If an airport is missing coordinates in `airports.json`, the system will:
1. Print an error message
2. Fall back to full brightness (1.0)
3. Continue rendering all other airports normally

### Import Errors
If you see `ModuleNotFoundError: No module named 'astral'`, install dependencies:
```bash
pip install -r requirements.txt
```

## Future Enhancements

Possible improvements:
- Add civil twilight (smoother dimming during dusk)
- Make brightness target configurable per airport
- Add sunrise brightening (gradual increase in morning)
- Implement geo-location auto-detection

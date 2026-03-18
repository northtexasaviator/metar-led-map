"""Calculate sunrise/sunset times and brightness multiplier based on solar position."""

from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sunrise, sunset


def _get_solar_events(observer, date):
    """Return sunrise/sunset times for a date in UTC, or None if unavailable."""
    try:
        return {
            "sunrise": sunrise(observer, date=date),
            "sunset": sunset(observer, date=date),
        }
    except (ValueError, KeyError):
        return None


def get_sunset_brightness_multiplier(
    latitude: float,
    longitude: float,
    target_brightness: float = 0.5,
    transition_minutes: int = 60,
) -> float:
    """
    Calculate brightness multiplier based on time relative to sunrise/sunset.
    
    - Full brightness (1.0) during the day (sunrise to sunset)
    - Gradual fade over transition_minutes after sunset
    - Minimum brightness (target_brightness) during night
    - Gradual rise over transition_minutes before sunrise
    - Full brightness (1.0) at sunrise
    
    Args:
        latitude: Airport latitude
        longitude: Airport longitude
        target_brightness: Min brightness as fraction (0.0-1.0), default 0.5 = 50%
        transition_minutes: Minutes to fade/brighten, default 60
        
    Returns:
        Brightness multiplier (1.0 = full, 0.5 = 50% dimmed)
    """
    now = datetime.now(timezone.utc)

    location = LocationInfo(latitude=latitude, longitude=longitude)

    # Build a small UTC-based window around "now" and reason from the actual
    # previous/next solar events instead of the UTC calendar date. This avoids
    # incorrect behavior for western time zones after midnight UTC.
    event_days = [now.date() - timedelta(days=1), now.date(), now.date() + timedelta(days=1)]
    sun_windows = [_get_solar_events(location.observer, day) for day in event_days]

    sunrises = sorted(
        t["sunrise"] for t in sun_windows
        if t and "sunrise" in t
    )
    sunsets = sorted(
        t["sunset"] for t in sun_windows
        if t and "sunset" in t
    )

    if not sunrises or not sunsets:
        return 1.0

    try:
        prev_sunrise = max((t for t in sunrises if t <= now), default=None)
        next_sunrise = min((t for t in sunrises if t > now), default=None)
        prev_sunset = max((t for t in sunsets if t <= now), default=None)

        last_event_is_sunset = (
            prev_sunset is not None and
            (prev_sunrise is None or prev_sunset > prev_sunrise)
        )

        if last_event_is_sunset:
            # Nighttime: after most recent sunset, before next sunrise.
            time_since_sunset = (now - prev_sunset).total_seconds() / 60.0
            if time_since_sunset <= transition_minutes:
                progress = time_since_sunset / transition_minutes  # 0..1
                multiplier = 1.0 + (target_brightness - 1.0) * progress
                return max(target_brightness, min(1.0, multiplier))

            if next_sunrise is not None:
                time_until_sunrise = (next_sunrise - now).total_seconds() / 60.0
                if time_until_sunrise <= transition_minutes:
                    progress = 1.0 - (time_until_sunrise / transition_minutes)  # 0..1
                    multiplier = target_brightness + (1.0 - target_brightness) * progress
                    return min(1.0, multiplier)

            return target_brightness

        else:
            # Daytime: between sunrise and sunset.
            return 1.0
    except Exception:
        # Fallback: return full brightness if any calculation fails
        return 1.0


def get_sunset_time(latitude: float, longitude: float) -> datetime:
    """
    Get the sunset time for today at the given location.
    
    Returns:
        Sunset datetime in UTC
    """
    now = datetime.now(timezone.utc)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    return sunset(location.observer, date=now.date())


def get_sunrise_time(latitude: float, longitude: float) -> datetime:
    """
    Get the sunrise time for today at the given location.
    
    Returns:
        Sunrise datetime in UTC
    """
    now = datetime.now(timezone.utc)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    return sunrise(location.observer, date=now.date())

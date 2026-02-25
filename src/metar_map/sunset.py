"""Calculate sunrise/sunset times and brightness multiplier based on solar position."""

from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun


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
    
    try:
        # Get sunrise/sunset for today
        sun_times_today = sun(location.observer, date=now.date())
        sunrise_today = sun_times_today["sunrise"]
        sunset_today = sun_times_today["sunset"]
    except (ValueError, KeyError):
        # Handle polar day/night where sunrise/sunset doesn't exist
        # Default to full brightness if calculation fails
        return 1.0
    
    try:
        if now < sunrise_today:
            # Before sunrise today - check yesterday's sunset
            sun_times_yesterday = sun(location.observer, date=now.date() - timedelta(days=1))
            sunset_yesterday = sun_times_yesterday["sunset"]
            
            # In night period after last sunset, before this sunrise
            # Calculate time until sunrise
            time_until_sunrise = (sunrise_today - now).total_seconds() / 60.0
            
            # If within transition window before sunrise, brighten up
            if time_until_sunrise <= transition_minutes:
                progress = 1.0 - (time_until_sunrise / transition_minutes)  # 0..1
                multiplier = target_brightness + (1.0 - target_brightness) * progress
                return min(1.0, multiplier)
            else:
                # Still in night period, maintain minimum brightness
                return target_brightness
        
        elif now >= sunset_today:
            # After sunset today
            time_since_sunset = (now - sunset_today).total_seconds() / 60.0
            
            # If within transition window after sunset, dim down
            if time_since_sunset <= transition_minutes:
                progress = time_since_sunset / transition_minutes  # 0..1
                multiplier = 1.0 + (target_brightness - 1.0) * progress
                return max(target_brightness, min(1.0, multiplier))
            else:
                # In night period, maintain minimum brightness
                return target_brightness
        
        else:
            # During the day (between sunrise and sunset)
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
    sun_times = sun(location.observer, date=now.date())
    return sun_times["sunset"]


def get_sunrise_time(latitude: float, longitude: float) -> datetime:
    """
    Get the sunrise time for today at the given location.
    
    Returns:
        Sunrise datetime in UTC
    """
    now = datetime.now(timezone.utc)
    location = LocationInfo(latitude=latitude, longitude=longitude)
    sun_times = sun(location.observer, date=now.date())
    return sun_times["sunrise"]

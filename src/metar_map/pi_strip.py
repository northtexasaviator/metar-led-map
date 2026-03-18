try:
    import rpi_ws281x as ws
    from rpi_ws281x import PixelStrip, Color
except ImportError:  # Allows Windows to run without the library
    ws = None
    PixelStrip = None
    Color = None


def create_strip(led_count: int):
    if PixelStrip is None:
        raise RuntimeError("rpi_ws281x not installed (normal on Windows)")

    import os
    
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    # Allow brightness to be set via environment variable for testing
    LED_BRIGHTNESS = int(os.getenv("LED_BRIGHTNESS", "80"))  # 0-255, default 80 (31%)

    LED_INVERT = False
    LED_CHANNEL = 0

    # Explicit color order (most WS2811/WS2812 are GRB)
    STRIP_TYPE = ws.WS2811_STRIP_GRB

    strip = PixelStrip(
        led_count,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
        STRIP_TYPE,
    )
    strip.begin()
    return strip, Color
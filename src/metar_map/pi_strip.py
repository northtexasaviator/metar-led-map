try:
    from rpi_ws281x import PixelStrip, Color
except ImportError:  # Allows Windows to run without the library
    PixelStrip = None
    Color = None


def create_strip(led_count: int):
    if PixelStrip is None:
        raise RuntimeError("rpi_ws281x not installed (normal on Windows)")

    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 80
    LED_INVERT = False
    LED_CHANNEL = 0

    strip = PixelStrip(
        led_count,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    strip.begin()
    return strip, Color

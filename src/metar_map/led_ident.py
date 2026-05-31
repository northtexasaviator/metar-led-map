import select
import sys
import termios
import tty

from .layout import load_layout
from .pi_strip import create_strip


def _turn_all_off(strip, Color, led_count: int) -> None:
    for i in range(led_count):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def _wait_for_space() -> str:
    """Wait for a single key press and return the character."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ready, _, _ = select.select([sys.stdin], [], [])
            if ready:
                ch = sys.stdin.read(1)
                if ch == "\x03":
                    raise KeyboardInterrupt
                return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def run() -> None:
    layout = load_layout()
    strip, Color = create_strip(layout.led_count)

    print("Starting LED identifier mode")
    print("Spacebar: next LED | Ctrl+C: exit")

    led_index = 0

    try:
        _turn_all_off(strip, Color, layout.led_count)

        while True:
            for i in range(layout.led_count):
                strip.setPixelColor(i, Color(0, 255, 0))
            strip.setPixelColor(led_index, Color(255, 0, 0))
            strip.show()
            print(f"LED {led_index} is ON")

            while True:
                key = _wait_for_space()
                if key == " ":
                    led_index = (led_index + 1) % layout.led_count
                    break
    except KeyboardInterrupt:
        print("\nExiting LED identifier mode...")
    finally:
        _turn_all_off(strip, Color, layout.led_count)

if __name__ == "__main__":
    run()

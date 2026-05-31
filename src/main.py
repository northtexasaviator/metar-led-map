import sys
from metar_map.app import run as run_map
from metar_map.led_ident import run as run_ident
from metar_map.led_sweep import run as run_sweep


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sweep":
        run_sweep()
    elif len(sys.argv) > 1 and sys.argv[1] == "ledident":
        run_ident()
    else:
        run_map()

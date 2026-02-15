from .renderer import Renderer
from .model import LedState

class PiRenderer(Renderer):
    def __init__(self, layout):
        super().__init__(layout)
        # Later: init WS281x here
        # For now: stub so the app can switch modes cleanly.

    def render(self, state: LedState) -> None:
        idx = self.layout.mapping.get(state.airport)
        # Later: set pixel color + effects
        print(f"[PI STUB] Would render {state.airport} to LED[{idx}]")

    def flush(self) -> None:
        # Later: strip.show()
        pass

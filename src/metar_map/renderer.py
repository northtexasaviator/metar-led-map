from abc import ABC, abstractmethod
from .layout import LedLayout
from .model import LedState


class Renderer(ABC):
    def __init__(self, layout: LedLayout):
        self.layout = layout

    @abstractmethod
    def render(self, state: LedState) -> None:
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError

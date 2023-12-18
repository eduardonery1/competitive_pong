from abc import ABC
from event import GameEvent, IEvent


class IModel(ABC):
    @abstractmethod
    def update(self, event) -> None:
        pass

class Model:
    def __init__(self, view):
        self.view = view
        self.running = True

    def update(self, event: IEvent) -> None:
        self.view.update(self.process_event(self, event))

    def process_event(self, event: IEvent) -> GameEvent:
        raise NotImplementedError 

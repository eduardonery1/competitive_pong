from abc import ABC, abstractmethod


class IEvent(ABC):
    def __init__(self, event):
        pass


class KeyboardEvent(IEvent):
    def __init__(self, event):
        self.y = event


class WebsocketEvent(IEvent):
    pass


class GameEvent(IEvent):
    pass

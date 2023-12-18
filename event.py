from abc import ABC, abstractmethod


class IEvent(ABC):
    pass


class KeyboardEvent(IEvent):
    pass


class GameEvent(IEvent):
    pass

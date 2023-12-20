from abc import ABC, abstractmethod
from json import dumps, loads

class IEvent(ABC):
    def __init__(self, event):
        pass

class KeyboardEvent(IEvent):
    def __init__(self, event):
        self.y = event

    def to_json(self):
        return dumps({"dy": self.y})

class WebsocketEvent(IEvent):
    def __init__(self, message):
        response = loads(message)
        self.y = response["y"]
        self.player = response["player"]

class GameEvent(IEvent):
    def __init__(self, event:IEvent, player):
        self.y = event.y
        if isinstance(event, KeyboardEvent):
            self.player = player
        else:
            self.player = event.player

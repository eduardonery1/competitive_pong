from abc import ABC, abstractmethod
from json import dumps, loads


class IEvent(ABC):
    def __init__(self, event):
        pass

    def to_json(self):
        return dumps({"y":self.y, "player":self.player})


class KeyboardEvent(IEvent):
    def __init__(self, event):
        self.y = event


class WebsocketEvent(IEvent):
    def __init__(self, message):
        response = loads(message)
        self.y = response["y"]
        self.player = response["player"]


class ChangeSceneEvent(IEvent):
    def __init__(self):
        pass


class GameEvent(IEvent):
    def __init__(self, y, player):
        self.y = y
        self.player = player

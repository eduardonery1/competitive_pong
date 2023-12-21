import pygame
from websocket import create_connection
from threading import Thread
import rel
from json import loads, dumps
from event import IEvent, KeyboardEvent, WebsocketEvent
from abc import ABC, abstractmethod 


class IController(ABC):
    @abstractmethod
    def listen(self) -> None:
        pass


class KeyboardController(IController):
    def __init__(self, model):
        self.model = model
    
    def _listen(self) -> None:
        last_key = None
        while self.model.running:
            key = self._get_keyboard()
            if last_key is None or key.y != last_key.y:
                self.model.update(key)
                last_key = key

    def listen(self) -> None:
        th = Thread(target = self._listen)
        th.start()

    def _get_keyboard(self) -> KeyboardEvent: 
        keys = pygame.key.get_pressed()
        y = 0
        if keys[pygame.K_UP]:
            y = -1
        elif keys[pygame.K_DOWN]:
            y = 1
        return KeyboardEvent(y)


class ServerController(IController):
    def __init__(self, model):
        self.model = model
        self.ws = create_connection("ws://192.168.26.228:8080/")
        wb_th = Thread(target = self.listen, args=(self, self.ws))
        wb_th.start()

    @staticmethod
    def listen(self, ws):
        print("listening to websocket")
        while self.model.running:
            event = WebsocketEvent(ws.recv())
            self.model.update(event)
        ws.close()

    def send_event(self, event: IEvent) -> None:
        self.ws.send(event.to_json())
        #print(event.to_json())

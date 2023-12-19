import pygame
import websockets
from event import IEvent, KeyboardEvent, WebsocketEvent
from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def listen(self) -> None:
        pass


class KeyboardController(IController):
    def __init__(self, model, clock, fps):
        self.model = model
        self.clock = clock
        self.fps = fps
        self.time = 0

    def listen(self) -> None:
        while self.model.running:
            self.model.update(self.get_keyboard())
            self.time = 0

    def get_keyboard(self) -> KeyboardEvent: 
        keys = pygame.key.get_pressed()
        y = 0
        if keys[pygame.K_UP]:
            y = -1
        elif keys[pygame.K_DOWN]:
            y = 1
        return KeyboardEvent(y)



class ServerController(IController):
    def __init__(self, model, websocket):
        self.model = model
        self.websocket = websocket

    async def listen(self) -> None:
        while self.model.running:
            response = await self.websocket.recv()
            self.model.update(WebsocketEvent(response))
        

import pygame
from websockets.sync.client import connect
from threading import Thread
from abc import ABC, abstractmethod
from event import GameEvent, KeyboardEvent, WebsocketEvent, IEvent
from view import View, PongViewModel
from controller import KeyboardController, ServerController



class IModel(ABC):
    @abstractmethod
    def update(self, event) -> None:
        pass


class Model(IModel):
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player = "left"

        self.view = View(self.clock, self.fps)
        self.view_model = self.view.set_scene(PongViewModel)
        renderer = Thread(target = self.view.render)
        self.running = True
        self.keyboard_controller = KeyboardController(self, self.clock, self.fps)
        keyboard_listener = Thread(target = self.keyboard_controller.listen)
        self.websocket_controller = None
        
        keyboard_listener.start() 
        renderer.start()

    def set_remote(self, websocket):
        self.websocket_controller = websocket

    async def update(self, event: IEvent) -> None:
        self.view_model.update(self.process_event(event))

    async def process_event(self, event: IEvent) -> GameEvent:
        if isinstance(event, KeyboardEvent):
            await self.websocket_controller.send_event(event)  
        elif isinstance(event, WebsocketEvent):
            pass
        return GameEvent(event, self.player) 

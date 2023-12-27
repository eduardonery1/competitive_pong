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
    def __init__(self, online = False):
        pygame.init()
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player = "left"
        
        self.websocket_controller = None
        if online:
            self.websocket_controller = ServerController(self)
        
        self.view = View(self.clock, self.fps)
        self.view_model = self.view.set_scene(PongViewModel)
        self.view.render()        

        self.keyboard = KeyboardController(self)
        self.keyboard.listen()

    def update(self, event: IEvent) -> None:
        self.view_model.update(self.process_event(event))

    def process_event(self, event: IEvent) -> GameEvent:
        if isinstance(event, KeyboardEvent):
            new_event = GameEvent(event.y, self.player)
            if self.websocket_controller is not None:
                self.websocket_controller.send_event(new_event) 
            return new_event
        elif isinstance(event, WebsocketEvent):
            print(event.to_json())
            return GameEvent(event.y, event.player)

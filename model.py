import pygame
from bot import BotPlayer
from websockets.sync.client import connect
from threading import Thread
from abc import ABC, abstractmethod
from event import *
from view_model import PongViewModel
from view import View
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
        self.bot = None
        
        self.view = View(self.clock, self.fps)
        self.view_model = self.view.set_scene(PongViewModel)
        self.view.render()        

        self.keyboard = KeyboardController(self)
        self.keyboard.listen()
        if online:
            self.websocket_controller = ServerController(self)
        else:        
            self.bot = BotPlayer(self, self.view_model)
 
    def update(self, event: IEvent) -> None:
        self.view_model.update(self.process_event(event))

    def process_event(self, event: IEvent) -> GameEvent:
        if isinstance(event, KeyboardEvent):
            new_event = GameEvent(event.y, self.player)
            if self.websocket_controller is not None:
                self.websocket_controller.send_event(new_event) 
            return new_event
        elif isinstance(event, WebsocketEvent):
            print("Server sent:", event.to_json())
            return GameEvent(event.y, event.player)
        elif isinstance(event, ChangeSceneEvent):
            pass
        elif isinstance(event, GameEvent):
            return event

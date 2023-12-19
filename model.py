import websockets
from threading import Thread
from abc import ABC, abstractmethod
from event import GameEvent, IEvent
from view import View, PongViewModel
from controller import KeyboardController


class IModel(ABC):
    @abstractmethod
    def update(self, event) -> None:
        pass


class Model(IModel):
    def __init__(self):
        self.view = View()
        self.pong = PongViewModel()
        self.view_model = self.pong
        self.view.set_scene(self.view_model)
        renderer = Thread(target = self.view.render)
        renderer.start()

        self.running = True
        self.keyboard_controller = KeyboardController(self)
        keyboard_listener = Thread(target = self.keyboard_controller.listen)
        keyboard_listener.start() 

    def update(self, event: IEvent) -> None:
        self.view_model.update(self.process_event(event))

    def process_event(self, event: IEvent) -> GameEvent:
        return event 
        

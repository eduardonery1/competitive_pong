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
        while self.model.running:
            self.model.update(self._get_keyboard())

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
        return KeyboardEvent(y, self.model.player)


class ServerController(IController):
    def __init__(self, model):
        self.model = model
        #self.ws = websocket.WebSocketApp("ws://192.168.26.228:8080/", on_message=self.listen)
        self.ws = create_connection("ws://192.168.26.228:8080/")


        #self.ws.run_forever(dispatcher=rel, reconnect=5)
        #print("ws running...")
        wb_th = Thread(target = self.listen2, args=(self, self.ws))
        wb_th.start()
        print("ws running")

        #rel.signal(2, rel.abort)  # Keyboard Interrupt
        #rel.dispatch()

    def listen2(self, ws):
        while self.model.running:
            event = loads(ws.recv())
            print(event)

        ws.close()

        

    @staticmethod
    def listen(wsapp, message):
        event_data = loads(message)
        print(event_data)
       
    def send_event(self, event):
        self.ws.send(event.to_json())
        print(event.to_json())

from event import IEvent, KeyboardEvent
from model import IModel


class IController(ABC):
    @abstractmethod
    def listen(self) -> None:
        pass


class KeyboardControlleri(IController):
    def __init__(self, model: IModel):
        self.model = model

    def listen(self) -> None:
        while self.model.running:
            self.model.update(get_keyboard(self))

    def get_keyboard(self) -> KeyboardEvent:
        key = pygame.key.get_pressed()
        x, y = (0,0)
        if keys[pygame.K_UP]:
            x = 0
            y = -5
        elif keys[pygame.K_DOWN]:
            x = 0
            y = 5
        return KeyboardEvent(x, y)



class ServerController(IController):
    def __init__(self, websocket):
        pass

    async def listen(self) -> None:
        pass


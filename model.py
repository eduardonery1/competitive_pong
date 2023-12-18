from event import GameEvent, IEvent

class Model:
    def __init__(self, view: IEvent):
        self.view = view

    def update(self, event):
        view.update(self.process_event(self, event))

    def process_event(self, event):
        return GameEvent(event)

from threading import Thread
from event import GameEvent

class BotPlayer:
    def __init__(self, model, view_model):
        self.model = model
        self.view_model = view_model
        self.play()

    def _play(self):
        while self.model.running:
            ball_pos = self.view_model.ball.centery
            player_pos = self.view_model.right_player.bottomleft[1]
            mv = 0
            if ball_pos > player_pos:
                mv = 1
            else:
                mv = -1
            self.model.update(GameEvent(mv, "right"))

    def play(self):
        th = Thread(target = self._play)
        th.start()
         

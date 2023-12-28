import pygame
import math
from threading import Thread
from abc import ABC, abstractmethod
from event import GameEvent


class IView(ABC):
    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError


class View(IView):
    def __init__(self, clock, fps, width = 1440, height = 810):
        self.clock = clock
        self.fps = fps
        self.screen_width = width
        self.screen_height = height
        self.scene = None

    def set_scene(self,scene):
        self.scene = scene(self.screen_width, self.screen_height)
        return self.scene

    def _render(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        running = True
        while running:
            #self.dt = pygame.time.get_ticks() - self.time
            #self.time += self.dt
            self.dt = self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            self.scene.draw(self.screen, self.dt)
            pygame.display.update()
    
    def render(self):
        th = Thread(target = self._render)
        th.start()
        print("rendering...")

if __name__=="__main__":
    pass


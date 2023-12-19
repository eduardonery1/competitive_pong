import pygame
from abc import ABC, abstractmethod
from event import GameEvent


class View:
    def __init__(self, clock, fps, width = 1440, height = 810):
        self.clock = clock
        self.fps = fps
        self.time = 0
        self.screen_width = width
        self.screen_height = height
        self.scene = None

    def set_scene(self,scene):
        self.scene = scene(self.screen_width, self.screen_height)
        return self.scene

    def render(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        running = True
        
        while running:
            self.dt = self.clock.tick_busy_loop(self.fps)
            self.time += self.dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            b = self.scene.draw(self.screen, self.time)
            if b:
                self.time = 0
            pygame.display.update()


class IViewModel(ABC):
    @abstractmethod
    def update(event: GameEvent) -> GameEvent:
        raise NotImplementedError

    @abstractmethod
    def draw(screen):
        pass

class PongViewModel(IViewModel):
    def __init__(self, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.current_mv = 0
        self.clock = pygame.time.Clock()
        self.time = 0

        self.screen = None
        self.background = pygame.image.load("./assets/background.png")
        self.ball_radius = 25
        self.rect_width = 50
        self.rect_height = self.screen_height / 3
        self.dist_from_border = 15

        self.left_player = pygame.Rect(  self.dist_from_border, 
                                    self.screen_height / 2 - self.rect_height / 2,
                                    self.rect_width,
                                    self.rect_height
                                )
        
        self.right_player = pygame.Rect( self.screen_width - self.rect_width - self.dist_from_border,
                                    self.screen_height / 2 - self.rect_height / 2,
                                    self.rect_width,
                                    self.rect_height
                                )
        
        self.ball = pygame.Rect( self.screen_width / 2 - self.ball_radius,
                            self.screen_height / 2 - self.ball_radius,
                            self.ball_radius * 2,
                            self.ball_radius * 2,
                        )


    def update(self, event: GameEvent) -> GameEvent :
        self.current_mv = event.y
        return event


    def draw(self, source_screen, time):
        if self.screen is None:
            self.screen = source_screen
        b = False
        if time >= 100:
            self.left_player.move_ip(0, self.current_mv*50)
            b = True

        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, (255,255,255), self.left_player)
        pygame.draw.rect(self.screen, (255,255,255), self.right_player)
        pygame.draw.rect(self.screen, (255,255,255), self.ball, border_radius=self.ball_radius)

        return b

if __name__=="__main__":
    view = View()
    pong_scene = PongScene()
    view.set_scene(pong_scene)



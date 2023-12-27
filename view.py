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
        self.right_mv = 0
        
        self.ball_mv_x = 1
        self.ball_mv_y = 1

        self.clock = pygame.time.Clock()
        self.player_time = 0
        self.ball_time = 0
        self.left_score = 0
        self.right_score = 0

        self.screen = None
        self.background = pygame.image.load("./assets/background.png")
        self.ball_radius = 25
        self.rect_width = 50
        self.rect_height = self.screen_height / 3
        self.dist_from_border = 15
        self.font = pygame.font.SysFont(None, 96)

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
        
        self.player_speed = 350 
        self.player_speed /= 1000
        
        self.ball_speed = 700
        self.ball_speed /= 1000
        
        self.player_period = math.ceil(1 / self.player_speed)
        self.ball_period = math.ceil(1 / self.ball_speed)

        self.img = None
        #self.time2 = 0
        #print(self.left_player.top)

    def update(self, event: GameEvent) -> GameEvent :
        if event.player == "left":
            self.current_mv = event.y
        else:
            self.right_mv = event.y
        return event

    def _update_game_objects(self, dt):
        self.ball_time += dt
        ballx = self.ball_time // self.ball_period
        ball_displacement = ballx * self.ball_period * self.ball_speed 
        self.ball.move_ip(self.ball_mv_x * ball_displacement, self.ball_mv_y * ball_displacement)

        if self.ball.centery - self.ball_radius < 0:
            self.ball_mv_y = 1
        elif self.ball.centery + self.ball_radius > self.screen_height:
            self.ball_mv_y = -1

        self.player_time += dt
        playerx = self.player_time // self.player_period
        player_displacement = playerx * self.player_period * self.player_speed

        self.left_player.move_ip(0, self.current_mv * player_displacement)
        self.right_player.move_ip(0, self.right_mv * player_displacement)

        collide_left, collide_right = self.ball.colliderect(self.left_player), self.ball.colliderect(self.right_player)
        if collide_left:
            self.ball_mv_x = 1
        elif collide_right:
            self.ball_mv_x = -1

        scored = False
        if self.ball.centerx - self.ball_radius < 0:
            self.right_score += 1
            scored = True
        elif self.ball.centerx + self.ball_radius > self.screen_width:
            self.left_score += 1
            scored = True

        if scored:
            self.img = self.font.render(f'{self.left_score} {self.right_score}', True, (255, 255, 255))
            self.ball_speed += self.ball_speed * 0
            self.ball = pygame.Rect( self.screen_width / 2 - self.ball_radius,
                              self.screen_height / 2 - self.ball_radius,
                              self.ball_radius * 2,
                              self.ball_radius * 2,
                          )
        self.ball_time -= ballx * self.ball_period
        self.player_time -= playerx * self.player_period
         
    def draw(self, source_screen, dt):
        if self.screen is None:
            self.screen = source_screen
        #self.time2 += dt 
                #if self.left_player.top >= 370 and self.time2 > 0:
        #    print(self.left_player.top, self.time2)
        self._update_game_objects(dt)           
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, (255,255,255), self.left_player)
        pygame.draw.rect(self.screen, (255,255,255), self.right_player)
        pygame.draw.rect(self.screen, (255,255,255), self.ball, border_radius=self.ball_radius)
        if self.img is not None:
            self.screen.blit(self.img, (self.screen_width//2 - 50/1440*self.screen_width, 20))
if __name__=="__main__":
    pass


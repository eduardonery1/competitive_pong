import pygame
import sys

class PongScene:
    def __init__(self):
        self.is_set = False

    def set_source(self, source_screen):

        self.screen = source_screen

        self.screen_width = source_screen.get_width()
        self.screen_height = source_screen.get_height()

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
        
        self.is_set = True
        
    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, (255,255,255), self.left_player)
        pygame.draw.rect(self.screen, (255,255,255), self.right_player)
        pygame.draw.rect(self.screen, (255,255,255), self.ball, border_radius=self.ball_radius)


class View:

    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 810
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
    def set_scene(self,scene):
        if not scene.is_set:
           scene.set_source(self.screen)

        self.scene = scene
        
    def game_loop(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            self.scene.draw()

            pygame.display.update()

view = View()
pong_scene = PongScene()
view.set_scene(pong_scene)

view.game_loop()


        
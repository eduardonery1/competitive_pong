import pygame
import sys

class View:

    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 810
        
    def game_loop(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            pygame.display.update()


view = View()
view.game_loop()


        
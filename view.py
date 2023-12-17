import pygame
import sys

class View:

    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 810
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.framerate = 60

        self.rect_width = 50
        self.rect_height = self.screen_height / 3
        self.dist_from_border_l = 5
        self.dist_from_border_r = self.

        left_player = pygame.Rect(self.dist_from_border, 
                                  self.screen_height / 2 - self.rect_height / 2,
                                  self.rect_width,
                                  self.rect_width
                                 )

        self.ball_radius = 25
        
import pygame
from pygame.color import THECOLORS
import sys

class SnakeGame:
    def __init__(self):
        self.score = 0


    def run(self):

        pygame.init()
        self.width = 500
        self.higth = 700
        self.head = 150
        self.etch = 10
        self.screen = pygame.display.set_mode((self.width, self.higth))
        self.field = pygame.Rect( self.etch, self.head + self.etch, self.width - 2*self.etch, self.higth - 2*self.etch - self.head)
        self.screen.fill((34, 50, 34))
        pygame.draw.rect(self.screen, (20, 200, 150), self.field, 0)
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()

        
        print("Змейка запущена! (пока заглушка)")

    def update(self):
        pass
import pygame
from pygame.color import THECOLORS
import sys
from . import snakesettings

#notation 
# x, y belong to N_0

# --------------------- Block class ---------------------
class Block:
    def __init__(self, x, y, color):
        self.x = x*snakesettings.BLOCK_SIZE
        self.y = y*snakesettings.BLOCK_SIZE
        self.color = color
    def draw(self, screen):
        self.block = pygame.Rect(
            self.x + snakesettings.ETCH, 
            self.y + snakesettings.HEAD_HEIGHT + snakesettings.ETCH, 
            snakesettings.BLOCK_SIZE, snakesettings.BLOCK_SIZE)
        pygame.draw.rect(screen, self.color, self.block, 0)

# --------------------- Snack class ---------------------
class Snack:
    pass

# --------------------- Snacke class ---------------------
class Snake:
    pass

# --------------------- Game ---------------------
class SnakeGame:
    def __init__(self):
        self.score = 0


    def run(self):
        self.running = True
        pygame.init()

        self.screen = pygame.display.set_mode((snakesettings.WIDTH, snakesettings.HEIGHT))
        self.field = pygame.Rect( 
            snakesettings.ETCH, 
            snakesettings.HEAD_HEIGHT + snakesettings.ETCH, 
            snakesettings.WIDTH - 2*snakesettings.ETCH, 
            snakesettings.HEIGHT - 2*snakesettings.ETCH - snakesettings.HEAD_HEIGHT)
        self.screen.fill(snakesettings.SCREEN_COLOR)
        pygame.draw.rect(self.screen, snakesettings.FIELD_COLOR, self.field, 0)


        print(f"Змейка{(snakesettings.HEIGHT - snakesettings.HEAD_HEIGHT- 2*snakesettings.ETCH )/snakesettings.BLOCK_SIZE}x{(snakesettings.WIDTH - 2*snakesettings.ETCH)/snakesettings.BLOCK_SIZE}")
                         
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
        
    def stop(self):
        self.running = False

    def update(self):
        pass
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
class Snake:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.snakehead = Block(self.x, self.y, self.color)
        self.snakebody = [self.snakehead] 
        self.direction = 'r'
    def draw(self, screen):
        for snakeblock in self.snakebody:
            snakeblock.draw(screen)
            

    def eat():
        pass


# --------------------- Snacke class ---------------------
class Snack:
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

        # нарисуем змейку
        self.snake = Snake(snakesettings.X // 2, snakesettings.Y // 2, snakesettings.SNAKE_COLOR)
        self.snake.draw(self.screen)

        print(f"Змейка{snakesettings.X}x{snakesettings.Y}")
                         
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
        
    # def stop(self):
    #     self.running = False

    def update(self):
        pass
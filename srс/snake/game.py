import pygame
from pygame.color import THECOLORS
import sys
from . import snakesettings

#notation 
# x, y belong to N_0

# --------------------- Block class ---------------------
class Block:
    def __init__(self, x, y, color):
        self.x = x*snakesettings.BLOCK_SIZE  + snakesettings.ETCH
        self.y = y*snakesettings.BLOCK_SIZE + snakesettings.HEAD_HEIGHT + snakesettings.ETCH
        self.color = color
    def draw(self, screen):
        self.block = pygame.Rect(
            self.x, self.y, 
            snakesettings.BLOCK_SIZE, snakesettings.BLOCK_SIZE)
        pygame.draw.rect(screen, self.color, self.block, 0)

# --------------------- Snack class ---------------------
class Snake:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
<<<<<<< HEAD:srс/snake/game.py
        self.head = Block(x, y, color)
        self.snakebody = [self.head]
    def draw(self, screen):
        for snakebloke in self.snakebody:
            snakebloke.draw(screen)
    def move():
        pass
=======
        self.snakehead = Block(self.x, self.y, self.color)
        self.snakebody = [self.snakehead] 
        self.direction = 'r'
    def draw(self, screen):
        for snakeblock in self.snakebody:
            snakeblock.draw(screen)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]: self.direction = 'd'
        if keys[pygame.K_UP]: self.direction = 'u'
        if keys[pygame.K_LEFT]: self.direction = 'l'
        if keys[pygame.K_RIGHT]: self.direction = 'r'

        for snakeblock in self.snakebody:
            if self.direction == 'd':
                snakeblock.y - 1;
            if self.direction == 'u':
                snakeblock.y + 1;
            if self.direction == 'r':
                snakeblock.x + 1;   
            if self.direction == 'l':
                snakeblock.x - 1;


>>>>>>> feature:scr/snake/game.py
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
<<<<<<< HEAD:srс/snake/game.py
        self.snake = Snake(12, 12, snakesettings.SNAKE_COLOR)    
        self.snake.draw(self.screen)
=======

        # нарисуем змейку
        self.snake = Snake(snakesettings.X // 2, snakesettings.Y // 2, snakesettings.SNAKE_COLOR)
        self.snake.draw(self.screen)
                         
>>>>>>> feature:scr/snake/game.py
        while self.running:
            # snake movement
            self.snake.move()
            self.snake.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
<<<<<<< HEAD:srс/snake/game.py
                    self.running = False
            pygame.display.flip()
        
=======
                    sys.exit()

            pygame.display.flip()
>>>>>>> feature:scr/snake/game.py
    # def stop(self):
    #     self.running = False

    def update(self):
        pass
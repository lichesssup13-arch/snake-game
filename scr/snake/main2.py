import pygame
import sys
import random
import pygame_menu
from collections import deque
import bot_exp
pygame.init() 

SIZE_BLOCK = 20
 # (Red, Green, Blue) rgb mod от 0 до 255
FRAME_COLOR  = (0, 50, 0) # зел
FORESTGREEN = (34, 139, 34)
BLACK = (0, 0, 0)
LIMEGREEN = (0, 100, 0)
GOLD = (255, 215, 0)
RED = (244, 0, 0)
HEADER_COLOR = GOLD
SNAKE_COLOR = (192, 192, 192)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
# width, higth
size = [SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
#print(size)
# окошко окрывается
screen = pygame.display.set_mode(size)
#Заголовок программы
pygame.display.set_caption('Змейка')
img = pygame.image.load("slizerin.jpg")
pygame.display.set_icon(img)
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36) # просто шрифт



def start_the_game():
 
    class SnakeBlock:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def is_inside(self):
            return 0 <= self.x < COUNT_BLOCKS  and 0 <= self.y < COUNT_BLOCKS
        
        def __eq__(self, other):
            return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y
        
    def get_random_empty_block():  # my it can be done with do while
        x = random.randint(0, COUNT_BLOCKS-1)
        y = random.randint(0, COUNT_BLOCKS-1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS-1)
            empty_block.y = random.randint(0, COUNT_BLOCKS-1)
        return empty_block

    def draw_block(color, row, colomn):

        pygame.draw.rect(screen, color, [(SIZE_BLOCK + MARGIN) * (colomn+1), 
                                                 (SIZE_BLOCK + MARGIN) * (row+1), 
                                                SIZE_BLOCK, 
                                                SIZE_BLOCK])

    # голова змейки это последний элемент
    snake_blocks = [SnakeBlock(COUNT_BLOCKS//2-1, COUNT_BLOCKS//2-1)]
    # add a snack
    apple = get_random_empty_block() 
    d_row = 0 # направление по  y 
    d_col = 1 # направление по  x
    total_coins = 0 # переменная для подсчёта очков
    speed = 1
    speed_0 = 1

# бесконечный цикл бесконечно вызывающий окошко
    while True:
        for event in pygame.event.get(): # перебераем все события которые совершает пользователь с начала работы программы
            if event.type == pygame.QUIT: # условие выхода
                print('exit')            
                pygame.quit()             #выход из pygame
                sys.exit()         
# полностью завершает программу оставим пока не пропишем условие выхода в while(на самом деле тк это обробатывает нажатие крестика то оставим навсегда)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row:
                    d_row = 0
                    d_col = 1


        screen.fill(FRAME_COLOR) # заливка экрана
        pygame.draw.rect(screen, HEADER_COLOR, [0, size[1]-HEADER_MARGIN, size[0], size[1]]) # поле для заголовак

        # создаём текст 
        text = courier.render(f"Total: {total_coins} Speed: {speed}", 0, BLACK)

        #отрисуем поле
        for row in range(COUNT_BLOCKS):
            for colomn in range(COUNT_BLOCKS):
                if (row+colomn)%2:
                    color = FORESTGREEN
                else:
                    color = LIMEGREEN
                draw_block(color, row, colomn)

        # движение по средством движения головы и удаления последнего блока
        head = snake_blocks[-1]
        new_head = SnakeBlock(head.x + d_row, head.y+ d_col) # двигаем голову

        # проверяем находится ли её гоолва за полем
        if not new_head.is_inside():
            print('crash')            
            # pygame.quit()     
            # sys.exit()
            break

        if new_head in snake_blocks:
            print("crash yourself")
            # pygame.quit()
            # sys.exit()
            break

        draw_block(RED, apple.x, apple.y) #рисуем закуску

        if apple == new_head:
            total_coins += 1
            speed = total_coins//5 + speed_0
            snake_blocks.append(apple) # тк голова находится в конце по сути добавляется новая голова
            apple = get_random_empty_block()

        # движение по средством движения головы и удаления последнего блока  
        snake_blocks.append(new_head) # движение головы
        snake_blocks.pop(0)    # удаление хвоста

        # нарисуем змейку 
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        # выводим текст на экран (мб лучше в другом месте вызвать)
        screen.blit(text, (SIZE_BLOCK, SIZE_BLOCK+size[1]-HEADER_MARGIN)) # весь текст


        pygame.display.flip() # метод применяет всё что нарисовали на экране до (вроде может принимать как аргумент область которую хочешь изменить)
        timer.tick(3 + speed)


menu = pygame_menu.Menu('', size[0],size[1],
                       theme=pygame_menu.themes.THEME_GREEN)

# Подменю для бота
bot_menu = pygame_menu.Menu('Настройки бота', size[0], size[1],
                            theme=pygame_menu.themes.THEME_GREEN)

# Переменные для хранения выбора
bot_selector = bot_menu.add.selector('Тип бота :', 
                                     [('A*', 'A*'),
                                      ('Случайный', 'Случайный'), 
                                      ('Жадный', 'Жадный')],
                                     default=0)
num_games_input = bot_menu.add.text_input('Количество игр :', default='10', input_type=pygame_menu.locals.INPUT_INT)

# Кнопка запуска серии
bot_menu.add.button('Запустить серию', 
                    lambda: bot_exp.start_bot_game(bot_selector.get_value()[0][0], 
                                                   int(num_games_input.get_value())))

bot_menu.add.button('Назад', pygame_menu.events.BACK)

# Добавляем пункты в главное меню
menu.add.text_input('Имя :', default='Lol')
menu.add.button('Играть', start_the_game)   # обычная игра с клавиатуры
menu.add.button('Бот', bot_menu)            # кнопка открывает подменю с настройками бота
menu.add.button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)



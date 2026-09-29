import pygame
import sys
import random
from collections import deque

# Константы (должны совпадать с основным файлом)
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
size = [SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

pygame.init()
screen = pygame.display.set_mode(size)
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))

def draw_block(color, row, col):
    pygame.draw.rect(screen, color,
                     [(SIZE_BLOCK + MARGIN) * (col + 1),
                     (SIZE_BLOCK + MARGIN) * (row + 1),
                      SIZE_BLOCK, SIZE_BLOCK])

def get_random_empty_block(snake_blocks):
    while True:
        x = random.randint(0, COUNT_BLOCKS-1)
        y = random.randint(0, COUNT_BLOCKS-1)
        block = SnakeBlock(x, y)
        if block not in snake_blocks:
            return block

# ---------- A* бот (улучшенный) ----------
def bfs_full_path(start, goal, obstacles, width, height):
    """Возвращает полный список направлений (dx, dy) от start до goal, или None."""
    from collections import deque
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                cell = (nx, ny)
                if cell not in obstacles and cell not in visited:
                    visited.add(cell)
                    queue.append((cell, path + [(dx, dy)]))
    return None

def count_free_cells_from_pos(pos, obstacles, width, height):
    from collections import deque
    queue = deque([pos])
    visited = {pos}
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                cell = (nx, ny)
                if cell not in obstacles and cell not in visited:
                    visited.add(cell)
                    queue.append(cell)
    return len(visited)

def is_path_safe(snake_blocks, full_path, apple, depth=4):

    # Копируем состояние
    sim_blocks = [SnakeBlock(b.x, b.y) for b in snake_blocks]
    sim_apple = SnakeBlock(apple.x, apple.y)
    
    # Проходим все шаги пути
    for step in full_path:
        head = sim_blocks[-1]
        new_head = SnakeBlock(head.x + step[0], head.y + step[1])
        if not new_head.is_inside() or new_head in sim_blocks:
            return False
        if new_head == sim_apple:
            # съели яблоко – змейка растёт
            sim_blocks.append(new_head)
            sim_apple = None   # яблока больше нет
        else:
            sim_blocks.append(new_head)
            sim_blocks.pop(0)
        # дополнительная проверка на самопересечение (хвост уже удалён)
        if new_head in sim_blocks[:-1]:
            return False
    
    # После пути делаем depth шагов, выбирая максимально свободное направление
    for _ in range(depth):
        head = sim_blocks[-1]
        obstacles = set((b.x, b.y) for b in sim_blocks[:-1])  # хвост не препятствие
        best_dir = None
        best_free = -1
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = head.x+dx, head.y+dy
            if 0 <= nx < COUNT_BLOCKS and 0 <= ny < COUNT_BLOCKS:
                if (nx, ny) not in obstacles:
                    temp_obst = obstacles.union({(nx, ny)})
                    free = count_free_cells_from_pos((nx, ny), temp_obst, COUNT_BLOCKS, COUNT_BLOCKS)
                    if free > best_free:
                        best_free = free
                        best_dir = (dx, dy)
        if best_dir is None:
            return False   # некуда идти – смерть
        new_head = SnakeBlock(head.x + best_dir[0], head.y + best_dir[1])
        if not new_head.is_inside() or new_head in sim_blocks:
            return False
        # обычный ход (без яблока)
        sim_blocks.append(new_head)
        sim_blocks.pop(0)
    
    return True

def bfs_bot(snake_blocks, apple, current_drow, current_dcol):
    """Основной бот: A* (BFS) с проверкой безопасности и выбором максимального пространства."""
    head = snake_blocks[-1]
    head_pos = (head.x, head.y)
    apple_pos = (apple.x, apple.y)
    obstacles = set((b.x, b.y) for b in snake_blocks[:-1])   # хвост не препятствие
    
    # 1. Пытаемся найти полный путь к яблоку
    full_path = bfs_full_path(head_pos, apple_pos, obstacles, COUNT_BLOCKS, COUNT_BLOCKS)
    if full_path:
        # Проверяем, безопасен ли этот путь (симуляция)
        if is_path_safe(snake_blocks, full_path, apple, depth=4):
            return full_path[0]   # берём первый шаг
    
    # 2. Если нет безопасного пути к яблоку – выбираем направление,
    #    которое максимизирует количество свободных клеток после шага
    best_dir = None
    best_free = -1
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = head.x+dx, head.y+dy
        if 0 <= nx < COUNT_BLOCKS and 0 <= ny < COUNT_BLOCKS:
            if (nx, ny) not in obstacles:
                temp_obst = obstacles.union({(nx, ny)})
                free = count_free_cells_from_pos((nx, ny), temp_obst, COUNT_BLOCKS, COUNT_BLOCKS)
                if free > best_free:
                    best_free = free
                    best_dir = (dx, dy)
    if best_dir:
        return best_dir
    
    # 3. Аварийный случай – остаёмся на месте (всё равно умрём)
    return (current_drow, current_dcol)

# ---------- Случайный бот (выбирает случайное безопасное направление) ----------
def random_bot(snake_blocks, apple, current_drow, current_dcol):
    head = snake_blocks[-1]
    obstacles = set((b.x, b.y) for b in snake_blocks[:-1])
    safe_dirs = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = head.x + dx, head.y + dy
        if 0 <= nx < COUNT_BLOCKS and 0 <= ny < COUNT_BLOCKS:
            if (nx, ny) not in obstacles:
                safe_dirs.append((dx, dy))
    if safe_dirs:
        return random.choice(safe_dirs)
    else:
        return (current_drow, current_dcol)

# ---------- Жадный бот (всегда идёт к яблоку) ----------
def greedy_bot(snake_blocks, apple, current_drow, current_dcol):
    head = snake_blocks[-1]
    obstacles = set((b.x, b.y) for b in snake_blocks[:-1])
    def dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    best_dir = None
    best_dist = float('inf')
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = head.x + dx, head.y + dy
        if 0 <= nx < COUNT_BLOCKS and 0 <= ny < COUNT_BLOCKS:
            if (nx, ny) not in obstacles:
                d = dist(nx, ny, apple.x, apple.y)
                if d < best_dist:
                    best_dist = d
                    best_dir = (dx, dy)
    if best_dir is not None:
        return best_dir
    else:
        return (current_drow, current_dcol)

# ---------- Одна игра с заданным ботом ----------
def play_one_game(bot_func):
    snake_blocks = [SnakeBlock(COUNT_BLOCKS//2-1, COUNT_BLOCKS//2-1)]
    apple = get_random_empty_block(snake_blocks)
    d_row, d_col = 0, 1
    total_coins = 0
    speed_0 = 300
    speed = speed_0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        d_row, d_col = bot_func(snake_blocks, apple, d_row, d_col)

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, size[1]- HEADER_MARGIN, size[0], size[1]])
        text = courier.render(f"Total: {total_coins} Speed: {speed}", 0, BLACK)
        screen.blit(text, (SIZE_BLOCK, size[1]- HEADER_MARGIN+SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for col in range(COUNT_BLOCKS):
                color = FORESTGREEN if (row + col) % 2 else LIMEGREEN
                draw_block(color, row, col)

        head = snake_blocks[-1]
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if not new_head.is_inside() or new_head in snake_blocks:
            break

        draw_block(RED, apple.x, apple.y)

        if apple == new_head:
            total_coins += 1
            speed = total_coins // 5 + speed_0
            snake_blocks.append(apple)
            apple = get_random_empty_block(snake_blocks)

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()
        timer.tick(3 + speed)

    return total_coins

# ---------- Запуск серии игр с заданными параметрами ----------
def run_series(bot_name, num_games):
    bots = {
        "*A": bfs_bot,
        "Случайный (хаотичный)": random_bot,
        "Жадный (прямой)": greedy_bot
    }
    bot_func = bots.get(bot_name, bfs_bot)

    scores = []
    for game_num in range(1, num_games + 1):
        print(f"Игра {game_num} из {num_games} (бот {bot_name})...")
        score = play_one_game(bot_func)
        scores.append(score)
        print(f"  Счёт: {score}")

        screen.fill(FRAME_COLOR)
        font = pygame.font.SysFont('courier', int(COUNT_BLOCKS*(2.4)))
        text = font.render(f"Game {game_num} finished! Score: {score}", True, GOLD)
        text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        # pygame.time.wait(1500)

    best = max(scores)
    worst = min(scores)
    average = sum(scores) / len(scores)

    print("\n=== Результаты серии ===")
    print(f"Бот: {bot_name}")
    print(f"Игр сыграно: {num_games}")
    print(f"Все счета: {scores}")
    print(f"Лучший: {best}")
    print(f"Худший: {worst}")
    print(f"Средний: {average:.2f}")


def start_bot_game(bot_name, num_games):
    run_series(bot_name, num_games)
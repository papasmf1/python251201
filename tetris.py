#cmd
#pip install pygame 
import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("테트리스")
clock = pygame.time.Clock()

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),      # 빨강
    (0, 255, 0),      # 초록
    (0, 0, 255),      # 파랑
    (255, 255, 0),    # 노랑
    (255, 0, 255),    # 자홍
    (0, 255, 255),    # 청록
    (255, 165, 0),    # 주황
]

# 테트로미노 모양
TETROMINOS = [
    [[1, 1, 1, 1]],           # I
    [[1, 1], [1, 1]],         # O
    [[0, 1, 1], [1, 1, 0]],   # Z
    [[1, 1, 0], [0, 1, 1]],   # S
    [[1, 0, 0], [1, 1, 1]],   # L
    [[0, 0, 1], [1, 1, 1]],   # J
    [[0, 1, 0], [1, 1, 1]],   # T
]

class Block:
    def __init__(self):
        self.shape = random.choice(TETROMINOS)
        self.color = random.choice(COLORS)
        self.x = 3
        self.y = 0

    def rotate(self):
        """블록을 시계방향으로 회전"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_block = Block()
        self.score = 0
        self.game_over = False
        self.fall_speed = 500  # 밀리초 단위
        self.last_fall_time = pygame.time.get_ticks()

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * 30, y * 30, 30, 30)
                if cell:
                    pygame.draw.rect(screen, COLORS[cell - 1], rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_block(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((block.x + x) * 30, (block.y + y) * 30, 30, 30)
                    pygame.draw.rect(screen, block.color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)

    def can_move(self, block, dx, dy):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block.x + x + dx
                    new_y = block.y + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def lock_block(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    if block.y + y >= 0:
                        self.grid[block.y + y][block.x + x] = random.randint(1, 7)
        self.clear_lines()
        self.current_block = Block()

    def clear_lines(self):
        lines_to_clear = []
        for y, row in enumerate(self.grid):
            if all(row):
                lines_to_clear.append(y)
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0] * 10)
            self.score += 100

    def can_rotate(self, block):
        """회전 가능 여부 확인"""
        original_shape = block.shape
        block.rotate()
        can_rotate = True
        
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block.x + x
                    new_y = block.y + y
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        can_rotate = False
                        break
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        can_rotate = False
                        break
            if not can_rotate:
                break
        
        if not can_rotate:
            block.shape = original_shape
        
        return can_rotate

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time >= self.fall_speed:
            if self.can_move(self.current_block, 0, 1):
                self.current_block.y += 1
            else:
                self.lock_block(self.current_block)
            self.last_fall_time = current_time

    def speed_up_fall(self):
        """블록이 빠르게 떨어지도록"""
        if self.can_move(self.current_block, 0, 1):
            self.current_block.y += 1

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_block(self.current_block)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

game = Game()
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and game.can_move(game.current_block, -1, 0):
                game.current_block.x -= 1
            elif event.key == pygame.K_RIGHT and game.can_move(game.current_block, 1, 0):
                game.current_block.x += 1
            elif event.key == pygame.K_UP:
                game.can_rotate(game.current_block)
            elif event.key == pygame.K_DOWN:
                game.speed_up_fall()

    game.update()
    game.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
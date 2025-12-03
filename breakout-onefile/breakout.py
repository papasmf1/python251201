import pygame
import random

class BreakoutGame:
    def __init__(self):
        import pygame
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # 패들 폭을 기존의 3배로 확장 (100 -> 300)
        self.paddle = pygame.Rect(self.width // 2 - 150, self.height - 30, 300, 10)
        self.ball = pygame.Rect(self.width // 2 - 15, self.height - 50, 30, 30)
        self.ball_speed = [5, -5]

        # 다채로운 팔레트를 사용하여 벽돌 생성 (각 벽돌에 색상 포함)
        palette = [
            (255, 69, 0),    # orangered
            (255, 140, 0),   # darkorange
            (255, 215, 0),   # gold
            (60, 179, 113),  # mediumseagreen
            (0, 191, 255),   # deepskyblue
            (65, 105, 225),  # royalblue
            (138, 43, 226),  # blueviolet
            (255, 20, 147),  # deeppink
            (255, 105, 180), # hotpink
            (148, 0, 211),   # darkviolet
        ]
        self.bricks = []
        brick_w = 75
        brick_h = 20
        cols = 10
        rows = 5
        x_margin = (self.width - cols * brick_w) // 2
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x_margin + x * brick_w, 50 + y * (brick_h + 5), brick_w - 5, brick_h)
                color = palette[(x + y) % len(palette)]
                self.bricks.append((rect, color))

        # 아이템(떨어지는 보너스), 총알, 탄약 관리
        self.items = []      # each: {'rect':Rect, 'type':'gun', 'speed':int}
        self.bullets = []    # each: Rect moving up
        self.ammo = 0

    def run(self):
        import pygame
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        import pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 스페이스바: 총알 발사 (탄약이 있을 때)
                    if self.ammo > 0:
                        bx = self.paddle.centerx - 3
                        by = self.paddle.top - 10
                        self.bullets.append(pygame.Rect(bx, by, 6, 10))
                        self.ammo -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.move_ip(-10, 0)
        if keys[pygame.K_RIGHT] and self.paddle.right < self.width:
            self.paddle.move_ip(10, 0)

    def update(self):
        # 공 이동 및 충돌
        self.ball.move_ip(self.ball_speed)
        if self.ball.left <= 0 or self.ball.right >= self.width:
            self.ball_speed[0] = -self.ball_speed[0]
        if self.ball.top <= 0:
            self.ball_speed[1] = -self.ball_speed[1]
        if self.ball.colliderect(self.paddle):
            self.ball_speed[1] = -abs(self.ball_speed[1])
            # 공의 수평속도에 패들 접촉 위치 보정
            offset = (self.ball.centerx - self.paddle.centerx) / (self.paddle.width / 2)
            self.ball_speed[0] = int(self.ball_speed[0] + offset * 2)
        if self.ball.bottom >= self.height:
            self.running = False

        # 벽돌 충돌 처리 (공)
        for brick in self.bricks[:]:
            rect, color = brick
            if self.ball.colliderect(rect):
                self.bricks.remove(brick)
                self.ball_speed[1] = -self.ball_speed[1]
                # 벽돌 파괴 시 아이템 생성 확률
                if random.random() < 0.35:
                    item_rect = pygame.Rect(rect.centerx - 10, rect.centery - 10, 20, 20)
                    self.items.append({'rect': item_rect, 'type': 'gun', 'speed': 3})
                break

        # 총알 이동 및 벽돌 충돌 처리
        for bullet in self.bullets[:]:
            bullet.move_ip(0, -12)
            if bullet.bottom < 0:
                self.bullets.remove(bullet)
                continue
            # 총알-벽돌 충돌
            for brick in self.bricks[:]:
                rect, color = brick
                if bullet.colliderect(rect):
                    try:
                        self.bricks.remove(brick)
                    except ValueError:
                        pass
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    # 총알로 파괴 시에도 아이템 생성 확률 (약간 낮게)
                    if random.random() < 0.20:
                        item_rect = pygame.Rect(rect.centerx - 10, rect.centery - 10, 20, 20)
                        self.items.append({'rect': item_rect, 'type': 'gun', 'speed': 3})
                    break

        # 아이템 떨어짐 및 패들과 충돌 처리
        for item in self.items[:]:
            item['rect'].move_ip(0, item['speed'])
            if item['rect'].colliderect(self.paddle):
                # gun 아이템: 탄약 획득
                if item['type'] == 'gun':
                    self.ammo += 5
                try:
                    self.items.remove(item)
                except ValueError:
                    pass
            elif item['rect'].top > self.height:
                # 화면 하단 벗어나면 제거
                try:
                    self.items.remove(item)
                except ValueError:
                    pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        # 패들, 공
        pygame.draw.rect(self.screen, (255, 255, 255), self.paddle)
        pygame.draw.ellipse(self.screen, (255, 0, 0), self.ball)

        # 벽돌
        for rect, color in self.bricks:
            pygame.draw.rect(self.screen, color, rect)

        # 아이템 (노란색 상자)
        for item in self.items:
            pygame.draw.rect(self.screen, (255, 255, 0), item['rect'])
            # 간단 아이콘: 작은 총 모양 표시
            pygame.draw.line(self.screen, (0,0,0), (item['rect'].left+3, item['rect'].centery), (item['rect'].right-3, item['rect'].centery), 2)

        # 총알
        for b in self.bullets:
            pygame.draw.rect(self.screen, (200, 200, 255), b)

        # HUD: 남은 탄약 표시
        font = pygame.font.SysFont(None, 24)
        ammo_surf = font.render(f"Ammo: {self.ammo}", True, (255,255,255))
        self.screen.blit(ammo_surf, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
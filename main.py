import pygame
import random
import time
from datetime import datetime

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [500, 700]
screen = pygame.display.set_mode(size)

title = "Jet Plane vs. Ghost"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()


class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, addr):
        if addr[-3:] == 'png':
            self.img = pygame.image.load(addr).convert_alpha()
        else:
            self.img = pygame.image.load(addr)
        self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))


def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False


jet = obj()
jet.put_img("./image/jet.png")
jet.change_size(50, 50)
jet.x = round((size[0] - jet.sx) / 2)
jet.y = size[1] - 5 - jet.sy
jet.move = 5

left_go = False
right_go = False
space_go = False

bomb_list = []
ghost_list = []
k = 0

black = (0, 0, 0)
white = (255, 255, 255)

GAME_OVER = False
kill = 0  # 죽인 유령개수
loss = 0  # 놓친 유령개수

# 4-0. 게임 시작 대기 화면
SB = True
EXIT = False
while SB:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = False
            EXIT = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = False
    screen.fill(black)
    font = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.ttf', 20)
    text_start = font.render('PRESS SPACE KEY TO START THE GAME', True, (255, 255, 255))
    screen.blit(text_start, (50, round(size[1] / 2 + 50)))

    font_title = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.ttf', 30)
    text_title = font_title.render('JET PLANE vs GHOST', True, (255, 255, 255))
    screen.blit(text_title, (90, round(size[1] / 2 - 50)))
    pygame.display.flip()

# 4. 메인 이벤트
start_time = datetime.now()
SB = True
while SB and not EXIT:
    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds(), 1)

    if left_go:
        jet.x -= jet.move
        if jet.x <= 0:
            jet.x = 0
    elif right_go:
        jet.x += jet.move
        if jet.x >= size[0] - jet.sx:
            jet.x = size[0] - jet.sx

    if space_go and k % 5 == 0:
        bomb = obj()
        bomb.put_img("./image/bomb.svg")
        bomb.change_size(7, 15)
        bomb.x = round(jet.x + (jet.sx - bomb.sx) / 2)
        bomb.y = jet.y
        bomb.move = 15
        bomb_list.append(bomb)
    k += 1
    d_list = []
    for i in range(len(bomb_list)):
        b = bomb_list[i]
        b.y -= b.move
        if b.y <= -b.sy:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del bomb_list[d]

    if random.random() > 0.98:
        ghost = obj()
        ghost.put_img("./image/ghost.svg")
        ghost.change_size(30, 30)
        ghost.x = random.randrange(0, size[0] - ghost.sx - round(jet.sx / 2))
        ghost.y = 10
        ghost.move = 2
        ghost_list.append(ghost)
    d_list = []
    for i in range(len(ghost_list)):
        g = ghost_list[i]
        g.y += g.move
        if g.y >= size[1]:
            d_list.append(i)
            loss += 1
    d_list.reverse()
    for d in d_list:
        del ghost_list[d]

    # 미사일과 유령 충돌 시 제거
    db_list = []
    dg_list = []
    for i in range(len(bomb_list)):
        for j in range(len(ghost_list)):
            b = bomb_list[i]
            g = ghost_list[j]
            if crash(b, g):
                db_list.append(i)
                dg_list.append(j)
                kill += 1
    db_list = list(set(db_list))
    dg_list = list(set(dg_list))
    db_list.reverse()
    dg_list.reverse()
    for db in db_list:
        del bomb_list[db]
    for dg in dg_list:
        del ghost_list[dg]

    # 유령과 제트기 충돌 시 게임 종료
    for i in range(len(ghost_list)):
        g = ghost_list[i]
        if crash(g, jet):
            GAME_OVER = True
            SB = False

    # 4-4. 그리기
    screen.fill(black)
    jet.show()
    for b in bomb_list:
        b.show()
    for g in ghost_list:
        g.show()

    # 텍스트 게임 화면에 표시하기
    font = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.ttf', 20)
    text_kill = font.render(f'killed: {kill} loss: {loss}', True, (255, 255, 0))
    screen.blit(text_kill, (10, 5))

    text_time = font.render(f'time: {delta_time}', True, (255, 255, 255))
    screen.blit(text_time, (size[0] - 110, 5))
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
while GAME_OVER:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_OVER = False

    font = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.ttf', 40)
    text_start = font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(text_start, (125, round(size[1] / 2 - 50)))
    pygame.display.flip()

pygame.quit()

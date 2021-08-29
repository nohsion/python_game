import pygame
import random

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [500, 700]
screen = pygame.display.set_mode(size)

title = "My Game"
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

# 4. 메인 이벤트
SB = True
while SB:
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
    d_list.reverse()
    for d in d_list:
        del ghost_list[d]

    db_list = []
    dg_list = []
    for i in range(len(bomb_list)):
        for j in range(len(ghost_list)):
            b = bomb_list[i]
            g = ghost_list[j]
            if crash(b, g):
                db_list.append(i)
                dg_list.append(j)
    db_list = list(set(db_list))
    dg_list = list(set(dg_list))
    db_list.reverse()
    dg_list.reverse()
    for db in db_list:
        del bomb_list[db]
    for dg in dg_list:
        del ghost_list[dg]



    # 4-4. 그리기
    screen.fill(black)
    jet.show()
    for b in bomb_list:
        b.show()
    for g in ghost_list:
        g.show()

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()

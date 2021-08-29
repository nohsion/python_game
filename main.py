import pygame

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


jet = obj()
jet.put_img("./image/jet.png")
jet.change_size(50, 50)
jet.x = round((size[0] - jet.sx) / 2)
jet.y = size[1] - 5 - jet.sy

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

    # 4-3. 입력, 시간에 따른 변화

    # 4-4. 그리기
    screen.fill(black)
    jet.show()

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()

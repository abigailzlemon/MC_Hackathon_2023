import pygame
import random
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SCALE_IMAGE_MONSTER = (50, 50)
SCALE_IMAGE_PLATFORM = (200, 50)

TICK_TIME = 60

basePath = os.path.dirname(__file__)
monsterPath = os.path.join(basePath, "monster dude.png")
monsterImg = pygame.image.load(monsterPath)
monsterImg = pygame.transform.scale(monsterImg, SCALE_IMAGE_MONSTER)
platformPath = os.path.join(basePath, "platform5.png")
platformImg = pygame.image.load(platformPath)
platformImg = pygame.transform.scale(platformImg, SCALE_IMAGE_PLATFORM)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = monsterImg

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platformImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30]).convert()
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx * (1/TICK_TIME)
        self.rect.y += self.dy * (1/TICK_TIME)

        print(f'{self.dx}, {self.dy}')

pygame.init()

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("MOCO Hackathon 2023")

player = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
spritesList = pygame.sprite.Group()
spritesList.add(player)

for i in range(5):
    xpos = random.randint(0, 1000)
    ypos = random.randint(0, 500)
    m = Monster(xpos, ypos)
    p = Platform(xpos-100, ypos+30)
    spritesList.add(m, p)

clock = pygame.time.Clock()

play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            play = False

        if keys[pygame.K_UP]:
            player.dy = -100
        else:
            player.dy = 0

        if keys[pygame.K_LEFT]:
            player.dx = -100
        elif keys[pygame.K_RIGHT]:
            player.dx = 100
        else:
            player.dx = 0

    player.update()
    #screen.blit(monsterImg, (200, 200))
    spritesList.draw(screen)

    clock.tick(TICK_TIME)

    pygame.display.flip()
pygame.quit()
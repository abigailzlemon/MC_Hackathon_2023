import pygame
import random
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SCALE_IMAGE = (50, 50)

basePath = os.path.dirname(__file__)
monsterPath = os.path.join(basePath, "monster dude.png")
monsterImg = pygame.image.load(monsterPath)
monsterImg = pygame.transform.scale(monsterImg, SCALE_IMAGE)
platformPath = os.path.join(basePath, "platform.jpg")
platformImg = pygame.image.load(playformPath)
platformImg = pygame.transform.scale(platformImg, SCALE_IMAGE)
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
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super.__init__()

pygame.init()

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("MOCO Hackathon 2023")

spritesList = pygame.sprite.Group()
for i in range(5):
    m = Monster(random.randint(0, 1000), random.randint(0, 500))
    spritesList.add(m)
clock = pygame.time.Clock()

play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        play = False
    #screen.blit(monsterImg, (200, 200))
    spritesList.draw(screen)
    pygame.display.flip()
pygame.quit()
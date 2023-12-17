import pygame
import random
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SCALE_IMAGE_MONSTER = (50, 50)
SCALE_IMAGE_PLATFORM = (200, 50)
SCALE_IMAGE_CHIHIRO = (50,50)
SCALE_IMAGE_BALL = (50,50)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# frame rate
TICK_TIME = 60

basePath = os.path.dirname(__file__)
monsterPath = os.path.join(basePath, "monster dude.png")
monsterImg = pygame.image.load(monsterPath)
monsterImg = pygame.transform.scale(monsterImg, SCALE_IMAGE_MONSTER)
platformPath = os.path.join(basePath, "platform5.png")
platformImg = pygame.image.load(platformPath)
platformImg = pygame.transform.scale(platformImg, SCALE_IMAGE_PLATFORM)
playerPath = os.path.join(basePath, "chihiroright.png")
playerImg = pygame.image.load(playerPath)
playerImg = pygame.transform.scale(playerImg, SCALE_IMAGE_CHIHIRO)
magicBallPath = os.path.join(basePath, "magicBall.png")
magicBallImg = pygame.image.load(magicBallPath)
magicBallImg = pygame.transform.scale(magicBallImg, SCALE_IMAGE_BALL)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = monsterImg

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def collision(self, ball):
        if ball.og == 0:
            if self.rect.x > ball.rect.x + ball.width or self.rect.x + self.width < ball.rect.x:
                return False
            if self.rect.y > ball.rect.y + ball.height or self.rect.y + self.height < ball.rect.y:
                return False
            return True
        return False

class MagicBall(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, origin):
        super().__init__()
        self.speed = speed
        self.image = 0
        if self.speed > 0:
            self.image = pygame.transform.flip(magicBallImg, True, False)
        else:
            self.image = magicBallImg

        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.og = origin #1 means from monster, 0 means from player
    def update(self):
        self.rect.x += self.speed * (1/TICK_TIME)

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
        self.image = playerImg
        #self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.dy = 0
        self.direction = 1 #1 is right, -1 is left
        self.health = 5

    def update(self):
        self.rect.x += self.dx * (1/TICK_TIME)
        self.rect.y += self.dy * (1/TICK_TIME)


        #print(f'{self.dx}, {self.dy}')
    def collision(self, ball):
        if ball.og == 1:
            if self.rect.x > ball.rect.x + ball.width or self.rect.x + self.width < ball.rect.x:
                return False
            if self.rect.y > ball.rect.y + ball.height or self.rect.y + self.height < ball.rect.y:
                return False
            return True
        return False

pygame.init()

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("MOCO Hackathon 2023")

player = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
spritesList = pygame.sprite.Group()
spritesList.add(player)
bulletsList = []
monstersList = []
for i in range(5):
    xpos = random.randint(100*i, 1000)
    ypos = random.randint(50*i, 500)
    m = Monster(xpos, ypos)
    p = Platform(xpos-100 + random.randint(10, 30), ypos+30)
    spritesList.add(m, p)
    monstersList.append(m)


clock = pygame.time.Clock()

play = True

cooldown = 120

while play:
    cooldown += 1
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            play = False

        if keys[pygame.K_UP]:
            player.dy = -100
        elif keys[pygame.K_DOWN]:
            player.dy = 100
        else:
            player.dy = 0

        if keys[pygame.K_LEFT]:
            player.dx = -100
            player.direction = -1
            player.image = pygame.transform.flip(playerImg, True, False)
        elif keys[pygame.K_RIGHT]:
            player.dx = 100
            player.direction = 1
            player.image = playerImg
        else:
            player.dx = 0
        if keys[pygame.K_SPACE]:
            if cooldown >= 120:
                cooldown = 0
                b1 = MagicBall(player.rect.x, player.rect.y, 500 * player.direction, 0)
                bulletsList.append(b1)
                spritesList.add(b1)
    
    #pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect((player.rect.x, player.rect.y, 50, 50)))
    player.update()
    for bullet in bulletsList:
        flag = False
        # for i in range(len(monstersList)):
        #     mons = monstersList[i]
        #     if mons.collision(bullet):
        #         mons.kill()
        #         monstersList.pop(i)
        for mons in monstersList:
            if mons.collision(bullet):
                
                flag = True
                mons.kill()
                bullet.kill()
                mons.rect.y = -10000
                #monstersList.remove(mons)
                #bulletsList.remove(bullet)
            
        print(bullet.rect.x)
        if not flag:
            bullet.update()
        else:
            bulletsList.remove(bullet)
    #screen.blit(monsterImg, (200, 200))
    spritesList.draw(screen)

    clock.tick(TICK_TIME)

    pygame.display.flip()
pygame.quit()
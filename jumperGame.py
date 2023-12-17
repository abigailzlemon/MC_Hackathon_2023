import pygame
import random
import os

# window size
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# for scaling
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
SKY_BLUE = (12, 156, 180)

# frame rate
TICK_TIME = 60
global score
score = 0
basePath = os.path.dirname(__file__)

# sprite images
monsterPath = os.path.join(basePath, "witchleft.png")
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
# redBallPath = os.path.join(basePath, "blueBoltPNG.png")
# redBallImg = pygame.image.load(redBallPath)
# redBallImg = pygame.transform.scale(redBallImg, SCALE_IMAGE_BALL)
bgPath = os.path.join(basePath,"bg.png")
bg = pygame.image.load(bgPath)
sootPath = os.path.join(basePath, "soot.png")
sootImg = pygame.image.load(sootPath)
sootImg = pygame.transform.scale(sootImg, SCALE_IMAGE_CHIHIRO)
cloud1Path = os.path.join(basePath, "cloud1.png")
cloud1Img = pygame.image.load(cloud1Path)
cloud1Img = pygame.transform.scale(cloud1Img, SCALE_IMAGE_PLATFORM)
cloud2Path = os.path.join(basePath, "cloud2.png")
cloud2Img = pygame.image.load(cloud2Path)
cloud2Img = pygame.transform.scale(cloud2Img, SCALE_IMAGE_PLATFORM)

monsterImgs = ["witchleft.png", "soot.png", "goblin.png"]
cloudImgs = ["cloud1.png", "cloud2.png"]



class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, frameCoolDown, imgPath):
        super().__init__()
        global score
        self.image = pygame.transform.scale(pygame.image.load(imgPath), SCALE_IMAGE_CHIHIRO)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.isAlive = True

        # shooting cooldown
        self.cooldown = frameCoolDown
    def collision(self, ball):
        global score
        # if the origin of the ball is from the player (0)
        if ball.og == 0:
            # collision detection algorithm
            if self.rect.x > ball.rect.x + ball.width or self.rect.x + self.width < ball.rect.x:
                return False
            if self.rect.y > ball.rect.y + ball.height or self.rect.y + self.height < ball.rect.y:
                return False
            score +=25
            return True
        return False
    

class MagicBall(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, origin):
        super().__init__()
        self.speed = speed
        self.image = 0
        self.og = origin #1 means from monster, 0 means from player
        blueBoltImg = pygame.image.load(os.path.join(basePath, "blueBoltPNG.png"))
        blueBoltImg = pygame.transform.scale(blueBoltImg, SCALE_IMAGE_CHIHIRO)

        # different image for player and monster
        if self.og == 0:
            if self.speed > 0:
                self.image = pygame.transform.flip(magicBallImg, True, False)
            else:
                self.image = magicBallImg
        else:
            if self.speed > 0:
                self.image = pygame.transform.flip(blueBoltImg, True, False)
            else:
                self.image = blueBoltImg
        self.speed = speed

        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.og = origin #1 means from monster, 0 means from player
    def update(self):
        self.rect.x += self.speed * (1/TICK_TIME)

class Platform(pygame.sprite.Sprite): # platforms
    def __init__(self, x, y, imgPath):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imgPath), SCALE_IMAGE_PLATFORM)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite): # player
    def __init__(self, x, y):
        super().__init__()
        self.image = playerImg
        

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.dy = 0
        self.direction = 1 #1 is right, -1 is left
        self.health = 5
        self.kills = 0
        self.score = 0

    def update(self):
        self.rect.x += self.dx * (1/TICK_TIME)
        self.rect.y += self.dy * (1/TICK_TIME)


    
    def collision(self, ball):
        if ball.og == 1:
            if self.rect.x > ball.rect.x + ball.width or self.rect.x + self.width < ball.rect.x:
                return False
            if self.rect.y > ball.rect.y + ball.height or self.rect.y + self.height < ball.rect.y:
                return False
            return True
        return False

pygame.init()

# sounds
gunFirePath = os.path.join(basePath, "gunFire.mp3")
jumpSoundPath = os.path.join(basePath, "jumpSound.mp3")
gunFire = pygame.mixer.Sound(gunFirePath)


# background music
backgroundMusicPath = os.path.join(basePath, "backgroundMusic.mp3")
pygame.mixer.music.load(backgroundMusicPath)
pygame.mixer.music.set_volume(.3)
pygame.mixer.music.play()

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("MOCO Hackathon 2023")

player = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
spritesList = pygame.sprite.Group()
spritesList.add(player)
bulletsList = []
monstersList = []

# generating the monsters and platforms
for i in range(5):
    xpos = random.randint(100*i, 1000)
    ypos = random.randint(50*i, 500)
    m = Monster(xpos, ypos, random.randint(70, 150), os.path.join(basePath, random.choice(monsterImgs)))
    p = Platform(xpos-100 + random.randint(10, 30), ypos+30, os.path.join(basePath, random.choice(cloudImgs)))
    spritesList.add(m, p)
    monstersList.append(m)

    p = Platform(xpos-100 + random.randint(10, 30), ypos+30, os.path.join(basePath, random.choice(cloudImgs)))
    spritesList.add(m, p)
    monstersList.append(m)


clock = pygame.time.Clock()

play = True
gameTime = 0
cooldown = 120

# font we are using
font = pygame.font.Font('freesansbold.ttf', 32)

while play:
    gameTime += 1
    cooldown += 1
    if player.kills != 5: # if 5 kills, game is over
        if gameTime % 120 == 0:
            player.score -= 1

    
    screen.blit(bg, (0, 0)) #paints over after every frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            play = False

        # movement
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
            if cooldown >= 120: # 60 frames in a second, 2 second cool down
                cooldown = 0
                b1 = MagicBall(player.rect.x, player.rect.y, 500 * player.direction, 0) # ball in player direction, originating from player
                bulletsList.append(b1)
                spritesList.add(b1)
                gunFire.play()
                if player.kills != 5: #at 5 kills game is over
                    player.score -= 5
    
    
    player.update()

    for mons in monstersList:
            if mons.isAlive:
                if gameTime % mons.cooldown == 0: # shoots at time intervals
                    # random if shoot left or right
                    if random.randint(0, 1) == 1:
                        b1 = MagicBall(mons.rect.x, mons.rect.y, random.randint(400, 500) * -.5, 1)
                        bulletsList.append(b1)
                        spritesList.add(b1)
                        
                    else:
                        b1 = MagicBall(mons.rect.x, mons.rect.y, random.randint(400, 500) * .5, 1)
                        bulletsList.append(b1)
                        spritesList.add(b1)
                        
    for bullet in bulletsList:
        # checks if there has been a collision
        flag = False
        if player.collision(bullet):
            player.health -= 1
            player.score -= 5
            flag = True
            bullet.kill()
    

        for mons in monstersList:
            if mons.collision(bullet):
                
                flag = True
                player.kills += 1
                player.score += 25
                # removes both monster and bullet from all sprites list
                mons.kill()
                bullet.kill()
                # makes sure does not interfere with future game mechanics
                mons.rect.y = -10000
               
            
        # if collision, render, else, remove from list
        if not flag:
            bullet.update()
        else:
            bulletsList.remove(bullet)
    
    
    spritesList.draw(screen)
    if player.kills == 5:
        text = font.render("Game Finished! Score: " + str(player.score), True, WHITE, SKY_BLUE)
        textRect = text.get_rect()
        textRect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        screen.blit(text, textRect)
    else:
        text = font.render("SCORE: " + str(player.score), True, WHITE, SKY_BLUE)
        textRect = text.get_rect()
        screen.blit(text, textRect)
    clock.tick(TICK_TIME)

    pygame.display.flip()
pygame.quit()
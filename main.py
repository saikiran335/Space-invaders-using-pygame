
import math
import pygame


import random
from pygame import mixer

from pygame.locals import *




pygame.init()



screen = pygame.display.set_mode((800, 600), RESIZABLE)

# set the pygame window name
pygame.display.set_caption("Raa Ra Choosukundham")





background = pygame.image.load("background.jpg")


mixer.music.load('music.mpeg')
mixer.music.play(-1)



icon = pygame.image.load('1.png')
pygame.display.set_icon(icon)

playerImage =pygame.image.load('space.png')
playerX = 370
playerY = 480
playerX_change = 0


enemyImage=[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enimies = 3

for i in range(num_of_enimies):
    enemyImage.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


bulletImage =pygame.image.load('bullet.png')
bulletX = 0
bulletY = 420
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


over_font = pygame.font.Font('freesansbold.ttf', 45)
over_font1 = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value),True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font1.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (330, 400))

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enimies):

        if enemyY[i] >400:
            for j in range(num_of_enimies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionImage = pygame.image.load('explosion.png')
            screen.blit(explosionImage, (enemyX[i], enemyY[i], bulletX, bulletY))

            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 420
            bullet_state = "ready"
            score_value += 10
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)




    if bulletY <= 0:
        bulletY = 420
        bullet_state = "ready"


    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

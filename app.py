import pygame
import random
import math
from pygame import mixer


# initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.jpg')

#sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space War")
icon = pygame.image.load('title.png')
pygame.display.set_icon(icon)
running = True

#player
playerImg = pygame.image.load('playerimg.png')
playerX = 370
playerY = 480
playerX_change = 0

#score

score_value = 0
font = pygame.font.SysFont('Arial.ttf',40)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score : "+ str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

#Game over
over_font = pygame.font.SysFont('Arial.ttf',60)

def game_over_text():
    over_text = over_font.render("GAME OVER", True,(255,255,255))
    screen.blit(over_text, (200,250))

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 8


for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    p = i * 70
    enemyX.append(p)
    enemyY.append(random.randint(15,150))
    enemyX_change.append(0.2)
    enemyY_change.append(30)

#bullet
#ready you can`t see the bullet
#fire the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16 , y + 10))


def player(playerX,playerY):
    screen.blit(playerImg, (playerX,playerY))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def destroy(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)+ (math.pow(enemyY - bulletY, 2))) 
    if distance < 27:
        return True
    else:
        return False

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if key is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    
    # RGB Red,Green,Blue
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    #enemy movement
    for i in range(num_of_enemy):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = - 0.2
            enemyY[i] += enemyY_change[i]

        #destroy
        enemy_destroy = destroy(enemyX[i],enemyY[i],bulletX,bulletY)
        if enemy_destroy:
            destroy_sound = mixer.Sound("explosion.wav")
            destroy_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)   
    
    #bullet movement
    if bulletY <= 50:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()


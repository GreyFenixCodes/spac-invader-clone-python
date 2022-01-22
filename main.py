
#importing pygame
import pygame

from pygame import mixer

#importing random generator
import random

#importing math operators
import math

#initializing pygame
pygame.init()


#creating the game screen - width and height are arguments
screen = pygame.display.set_mode((1000,1000))

#creating trhe background
background = pygame.image.load ('space.png')

#creating background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#changing title and icon
pygame.display.set_caption("Space Invaders .. ish") #sets the caption
icon = pygame.image.load('ufo.png')                 #loads icon image to icon variable
pygame.display.set_icon(icon)                       #sets programs icon to icon variable

#creating the player icon and x,y coordinate variables
playerImg = pygame.image.load('spaceship.png')
playerX = 468
playerY = 900

playerX_change = 0

#creating enemy icon and x,y coordinate variables
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append (pygame.image.load('enemy.png'))
    enemyX.append (random.randint(0,936))
    enemyY.append (random.randint(25, 350))

    enemyX_change.append (1)
    enemyY_change.append (64)

#creating the bullets
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 900

bulletX_change = 0
bulletY_change = 1

#creating "states" of the bullet. ready = hidden, fire = visible and moving
bullet_state = "ready"

#creating score variable
score_value = 0
font = pygame.font.SysFont('Arial', 32)

textX = 10
textY = 10

#creating game over text
game_over_font = pygame.font.SysFont('Arial', 128)


#defining the player function
def player(x,y):
    #blit draws the image at the coordinates
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow (enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render('Score: ' + str(score_value), True, (200,100,150))
    screen.blit(score, (x,y))

def game_over_text(x,y):
    game_over_text = game_over_font.render('GAME OVER!!', True, (255,50,50))
    screen.blit(game_over_text, (100,450))

#start of the game loop
running = True
while running:

    #filling the background with RGB colors
    screen.fill((0,200,255))
    screen.blit(background, (0,0))

    for event in pygame.event.get():    #gets all info on events in the game
        if event.type == pygame.QUIT:   #when the event is the quit function (x)
            running = False             #it changes running to false and closes the window

        #if key is pressed, check it and do actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            elif event.key == pygame.K_RIGHT:
                playerX_change = +1
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0




    #changes playerX based on keystrokes above
    playerX += playerX_change
    #creating left/right boundaries so player stays in screen
    if playerX <=0:
        playerX = 0
    elif playerX >=936:
        playerX = 936

    for i in range (num_of_enemies):

        #setting Game Over
        if enemyY[i] > 840:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(400,475)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
             enemyX_change[i] = -1
             enemyY[i] += enemyY_change[i]

        # collision incidences
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 900
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 936)
            enemyY[i] = random.randint(25, 350)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movemement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <=0:
        bulletY = 900
        bullet_state = "ready"



    #calling the player and enemy functions
    player(playerX, playerY)

    show_score(textX,textY)

    #updates the display, to show game changes and movement, etc.
    pygame.display.update()


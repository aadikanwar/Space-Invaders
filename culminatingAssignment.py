"""
Aadi Kanwar
March 22, 2020 - Space Invaders
This program is my culminating assignment for course ICS2O
"""

# importing the math library
import math
# importing the pygame library
import pygame
# importing the random library
import random
# importing music library
from pygame import mixer

# initializing pygame
pygame.init()

# screen coordinates/size
size = (800, 600)

# creating the actual screen
screen = pygame.display.set_mode(size)

# adding a name for my screen
pygame.display.set_caption("ICS2O Culminating")

# creating a FPS variable
clock = pygame.time.Clock()

# Colour pallet
RED = (225, 0, 0)
BLUE = (0, 0, 128)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

# creating the setting
setting = pygame.image.load("unnamed.png")
settingRE = pygame.transform.scale(setting, (800, 600))

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # the '-1' plays the music on a loop (indefinitely)


# defining a function for the setting
def settingIMG():
    screen.blit(settingRE, (0, 0))


# information for the main player
mainIMG = pygame.image.load("spaceship.png")
mainX = 368
mainY = 500
mainMoving = 0

# information for the enemy spaceship(s)

# creating a list -- used to create multiple enemies
enemyIMG = []
enemyX = []
enemyY = []
enemyMoving = []
enemyMovingY = []
enemyNum = 5

for i in range(enemyNum):
    enemyIMG.append(pygame.image.load("rock.png"))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(30, 150))
    enemyMoving.append(2.5)
    enemyMovingY.append(20)

# information for the user bullets
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500
bulletMoving = 4
bulletState = "ready"  # makes the laser invisible until you fire


# defining a function for the main player image
def mainPlayer(x, y):
    screen.blit(mainIMG, (x, y))


# defining a function for the main enemy image
def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


# defining a function for the bullet image
def bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))  # making it appear as though the bullet shoots from within the user IMG


def collision(enemyX, enemyY, bulletX, bulletY):
    coordDist = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(enemyY - bulletY, 2)))  # FORMULA FOR DISTANCE
    # BETWEEN TWO COORDINATES
    if coordDist < 20:
        return True
    else:
        return False


def paused():  # pause function
    global event  # makes the name event in scope

    pygame.mixer.music.stop()
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mixer.music.load("background.wav")
                    mixer.music.play(-1)
                    pause = False

                elif event.key == pygame.K_d:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        pauseText = pausedText.render("PAUSED", True, BLACK)
        screen.blit(pauseText, (210, 215))
        playText = playingText.render("Press 'a' to continue", True, BLACK)
        screen.blit(playText, (120, 400))
        quittingText = quitText.render("Press 'd' to quit", True, BLACK)
        screen.blit(quittingText, (530, 400))
        pygame.display.update()


# score variable
scoreVal = 0
text = pygame.font.SysFont("Times New Roman", 40)
textX = 555
textY = 550

# game over text
gameoverText = pygame.font.SysFont("Impact", 100)

# you win text
youwinText = pygame.font.SysFont("Impact", 100)

# paused text
pausedText = pygame.font.SysFont("Times New Roman", 100)
playingText = pygame.font.SysFont("Times New Roman", 20)
quitText = pygame.font.SysFont("Times New Roman", 20)


# defining a function to print score
def displayScore(x, y):
    score = text.render("Your Score: " + str(scoreVal), True, WHITE)
    screen.blit(score, (x, y))


# defining a function for the game over screen
def gameOver():
    lossText = gameoverText.render("GAME OVER ", True, WHITE)
    screen.blit(lossText, (185, 250))


# defining a function for the winner screen
def winner():
    winText = youwinText.render("YOU'RE A WINNER! ", True, WHITE)
    screen.blit(winText, (50, 230))


# creating the game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking if any arrow key has been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mainMoving = -5
            elif event.key == pygame.K_RIGHT:
                mainMoving = 5
            elif event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    soundForBullet = mixer.Sound("laser.wav")
                    soundForBullet.play()
                    bulletX = mainX
                    bullet(bulletX, bulletY)  # mainX is the coordinate of the user
            elif event.key == pygame.K_p:  # if the player presses 'p' the game will call the pause function
                paused()

        # checking for if the key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                mainMoving = 0

    # RGB
    screen.fill(BLACK)

    # calling in my setting image
    settingIMG()

    for i in range(enemyNum):

        if scoreVal == 15:  # if the score hits 13 the user wins
            for j in range(enemyNum):
                enemyY[j] = 4800  # makes the rocks disappear
                mainY = 40000  # makes the user spaceship disappear
            winner()
            pygame.mixer.music.stop()  # stops the music when the user wins
            break  # ends the code

        # game over screen code
        if enemyY[i] > 430:
            for j in range(enemyNum):
                enemyY[j] = 4800  # this y coordinate is way higher than the actual screen -- makes the rocks disappear
            gameOver()
            pygame.mixer.music.stop()  # stops the music once the game is over
            break

        # enemy movement method
        enemyX[i] += enemyMoving[i]  # [i] referencing the enemy x coord within the list

        # adding boundaries for the enemy// also the starting speed of the asteroids
        if enemyX[i] <= 0:
            enemyMoving[i] = 2.5
            enemyY[i] += enemyMovingY[i]
        elif enemyX[i] >= 736:
            enemyMoving[i] = -2.5
            enemyY[i] += enemyMovingY[i]

        if scoreVal == 5:  # if the user hits a score of 5 the asteroids start moving faster for a bit
            if enemyX[i] <= 0:
                enemyMoving[i] = 8
                enemyY[i] += enemyMovingY[i]
            elif enemyX[i] >= 736:
                enemyMoving[i] = -8
                enemyY[i] += enemyMovingY[i]

        if scoreVal == 10:  # if the user hits a score of 10 the asteroids start moving faster again
            if enemyX[i] <= 0:
                enemyMoving[i] = 10
                enemyY[i] += enemyMovingY[i]
            elif enemyX[i] >= 736:
                enemyMoving[i] = -10
                enemyY[i] += enemyMovingY[i]

        # collision detection
        collisionDetect = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisionDetect:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.play()
            bulletY = 500
            bulletState = "ready"
            scoreVal += 1
            enemyX[i] = random.randint(0, 730)  # respawning the enemy coordinates to another random coordinate(s)
            enemyY[i] = random.randint(30, 150)

        # calling in my enemy image
        enemy(enemyX[i], enemyY[i], i)

    # user movement method
    mainX += mainMoving

    # adding boundaries for the main player
    if mainX <= 0:
        mainX = 0
    elif mainX >= 736:
        mainX = 736

    # movement of bullet
    if bulletState is "fire":  # this exact line states that when the space bar is pressed the bulletstate changes from
        # "ready"
        bullet(bulletX, bulletY)
        bulletY -= bulletMoving

    if bulletY <= 0:
        bulletY = 500  # making the bullet come back to the head of the user spaceship
        bulletState = "ready"  # making sure that when the bullet reaches top of screen, the bulletstate stables and we
        # can shoot more bullets afterwards

    # calling in my image
    mainPlayer(mainX, mainY)

    # showing the score
    displayScore(textX, textY)

    # FPS
    clock.tick(100)

    # update code line
    pygame.display.flip()

# exit code command
pygame.quit()

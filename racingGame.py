#import the libraries
import pygame, random, sys, os, time
from pygame.locals import *

#initialize the variables
window_width = 800
window_height = 600
text_color = (255, 54, 124)
background_color = (0, 0, 225)
FPS = 40
car_min_speed = 10
car_max_speed = 20
car_min_size = 5
car_max_size = 20
new_car_add = 6
player_speedrate = 5
count = 3

#function to exit the game
def terminate():
    pygame.quit()
    sys.exit()

#function to start the game by taking player input
def PressKeyToStart():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return

#function to know if player has failed
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

#function to display text, score, etc.
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, text_color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/formula_1.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')

# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car7.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3, car4, baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')
truba = pygame.image.load('image/TRUBA.png')
# "Start" screen
#drawText('TRUBA', font, windowSurface, (window_width / 3) - 30, (window_height / 7))
windowSurface.blit(truba, (0,0))
drawText('Welcome to Car racing game', font, windowSurface, (window_width / 3) - 30, (window_height / 7))
drawText('Press any key to start the game.', font, windowSurface, (window_width / 3) - 30, (window_height / 3))
drawText('And Enjoy', font, windowSurface, (window_width / 3), (window_height / 3) + 30)
drawText('A game developed by:', font, windowSurface, (window_width / 3) - 30, 400)
drawText('Mohd Noman', font, windowSurface, (window_width / 3) - 30, 450)
pygame.display.update()
PressKeyToStart()
zero = 0
if not os.path.exists("data/save.dat"):
    f = open("data/save.dat", 'w')
    f.write(str(zero))
    f.close()
v = open("data/save.dat", 'r')
topScore = int(v.readline())
v.close()
while (count > 0):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (window_width / 2, window_height - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    # the game loop
    while True:
        # increase score
        score += 1

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == new_car_add:
            baddieAddCounter = 0
            baddieSize = 20
            newBaddie = {'rect': pygame.Rect(random.randint(120, 430), 0 - baddieSize, 23, 47),
                         'speed': random.randint(car_min_speed, car_max_speed),  #random.choice(sample)
                         'surface': pygame.transform.scale(random.choice(sample), (20, 60)),
                         }
            baddies.append(newBaddie)
            sideLeft = {'rect': pygame.Rect(0, 0, 126, 600),
                        'speed': random.randint(car_min_speed, car_max_speed),
                        'surface': pygame.transform.scale(wallLeft, (126, 599)),
                        }
            baddies.append(sideLeft)
            sideRight = {'rect': pygame.Rect(497, 0, 303, 600),
                         'speed': random.randint(car_min_speed, car_max_speed),
                         'surface': pygame.transform.scale(wallRight, (303, 599)),
                         }
            baddies.append(sideRight)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * player_speedrate, 0)
        if moveRight and playerRect.right < window_width:
            playerRect.move_ip(player_speedrate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * player_speedrate)
        if moveDown and playerRect.bottom < window_height:
            playerRect.move_ip(0, player_speedrate)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > window_height:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(background_color)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 40)

        windowSurface.blit(playerImage, playerRect)

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g = open("data/save.dat", 'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick(FPS)


    # "Game Over" screen.
    pygame.mixer.music.stop()
    count = count - 1
    gameOverSound.play()
    time.sleep(1)
    if (count == 0):
        laugh.play()
        drawText('Game over', font, windowSurface, (window_width / 3), (window_height / 3))
        drawText('Press any key to play again.', font, windowSurface, (window_width / 3) - 80, (window_height / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        PressKeyToStart()
        count = 3
        gameOverSound.stop()
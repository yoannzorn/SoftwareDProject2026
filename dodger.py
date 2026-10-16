import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIESIZE = 40
BADDIEMINSPEED = 3
BADDIEMAXSPEED = 6
ADDNEWBADDIERATE = 30
PLAYERMOVERATE = 5

class Player:
    def __init__(self):
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, WINDOWHEIGHT / 2)
        self.moveDown = self.moveUp = self.moveLeft = self.moveRight = False
    def keyboardMove(self):
        if self.moveLeft and self.rect.left > 0:
            self.rect.move_ip(-1 * PLAYERMOVERATE, 0)
        if self.moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.move_ip(PLAYERMOVERATE, 0)
        if self.moveUp and self.rect.top > 0:
            self.rect.move_ip(0, -1 * PLAYERMOVERATE)
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.move_ip(0, PLAYERMOVERATE)
    def KEYDOWN(self, event):
        if event.key == K_LEFT or event.key == K_a:
            self.moveRight = False
            self.moveLeft = True
        if event.key == K_RIGHT or event.key == K_d:
            self.moveLeft = False
            self.moveRight = True
        if event.key == K_UP or event.key == K_w:
            self.moveDown = False
            self.moveUp = True
        if event.key == K_DOWN or event.key == K_s:
            self.moveUp = False
            self.moveDown = True
    def KEYUP(self, event):
        if event.key == K_LEFT or event.key == K_a:
            self.moveLeft = False
        if event.key == K_RIGHT or event.key == K_d:
            self.moveRight = False
        if event.key == K_UP or event.key == K_w:
            self.moveUp = False
        if event.key == K_DOWN or event.key == K_s:
            self.moveDown = False
    def mouseMove(self, event):
        self.rect.centerx = event.pos[0]
        self.rect.centery = event.pos[1]

def terminate():
    pygame.quit() #ferme pygame
    sys.exit()    #ferme le programme python

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:       #quitter le jeu avec la croix
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # quitter le jeu avec la touche echap
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies): #la hitbox du joueur et des ennemis
    for b in baddies:
        if playerRect.colliderect(b['rect']): #si le joueur touche un ennemi, return True
            return True                       #collision    
    return False                              #pas collision   

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #taille de la fenêtre du jeu
pygame.display.set_caption('Dodger')  #titre du jeu
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)  #police d'écriture et taille de la police

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
baddieImage = pygame.image.load('baddie.png') #skin des ennemis

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    player = Player()
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)  #faire tourner la musique en boucle

    while True: # The game loop runs while the game part is playing.
        score += (1/60) # Increase score / 1 point par seconde

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:  #touches qui font bouger le joueur si activées
                if event.key == K_LEFT or event.key == K_a:
                    player.KEYDOWN(event)
                if event.key == K_RIGHT or event.key == K_d:
                    player.KEYDOWN(event)
                if event.key == K_UP or event.key == K_w:
                    player.KEYDOWN(event)
                if event.key == K_DOWN or event.key == K_s:
                    player.KEYDOWN(event)

            if event.type == KEYUP: #dès qiue la touche est relachée, le joueur ne bouge plus
                if event.key == K_ESCAPE:
                        terminate()
                if event.key == K_LEFT or event.key == K_a:
                    player.KEYUP(event)
                if event.key == K_RIGHT or event.key == K_d:
                    player.KEYUP(event)
                if event.key == K_UP or event.key == K_w:
                    player.KEYUP(event)
                if event.key == K_DOWN or event.key == K_s:
                    player.KEYUP(event)

            if event.type == MOUSEMOTION: # If the mouse moves, move the player where to the cursor.
                player.mouseMove(event)
        # Add new baddies at the top of the screen, if needed.
        baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = BADDIESIZE
            newBaddie = {'rect': pygame.Rect(WINDOWWIDTH + baddieSize, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around. et faire en sorte que le joueur ne sorte pas de l'écran
        player.keyboardMove()

        # Move the baddies down.
        for b in baddies:      #vitesse des ennemis
            b['rect'].move_ip(-b['speed'], 0) #vitesse des ennemis

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].right < 0:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score. (arrondi à l'entier le plus proche)
        drawText('Score: %s' % (int(score)), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (int(topScore)), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(player.image, player.rect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(player.rect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()

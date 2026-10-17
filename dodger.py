import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
PLAYERWIDTH = 40
PLAYERHEIGHT = 40
BADDIE1WIDTH = 40
BADDIE1HEIGHT = 40
BADDIE1MINSPEED = 3
BADDIE1MAXSPEED = 6
ADDNEWBADDIE1RATE = 30
BADDIE2WIDTH = 60
BADDIE2HEIGHT = 60
BADDIE2SPEED = 2
ADDNEWBADDIE2RATE = 400
BANANEWIDTH = 25                 
BANANEHEIGHT = 15
BANANESPEED = 7
BANANERATE = 250
MURSPEED = 5
MURWIDTH = 10
MURHEIGHT = 200
ADDNEWMURRATE = 300
BONUSSPEED = 8
BONUSWIDTH = 20
BONUSHEIGHT = 20
ADDNEWBONUSRATE = 200

class Player:
    def __init__(self):
        self.image = pygame.image.load('heros_plage.png')
        self.image = pygame.transform.scale(self.image, (PLAYERWIDTH, PLAYERHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, WINDOWHEIGHT / 2)
        self.moveDown = self.moveUp = self.moveLeft = self.moveRight = False
        self.moveRate = 5
    def keyboardMove(self):
        if self.moveLeft and self.rect.left > 0:
            self.rect.move_ip(-1 * self.moveRate, 0)
        if self.moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.move_ip(self.moveRate, 0)
        if self.moveUp and self.rect.top > 0:
            self.rect.move_ip(0, -1 * self.moveRate)
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.move_ip(0, self.moveRate)
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
    def isHit(self, objects):                          
        for o in objects:                              
            if self.rect.colliderect(o.rect):          
                return True
        return False
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Baddie:
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
    def move(self):
        self.rect.move_ip(-self.speed, 0)
    def tryToShoot(self, missileImage):  
        return None
    def isOffScreen(self):
        return self.rect.right < 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Baddie1(Baddie):
    def __init__(self,image):
        super().__init__(image)
        self.rect.topleft = (WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - BADDIE1HEIGHT))
        self.speed = random.randint(BADDIE1MINSPEED, BADDIE1MAXSPEED)
        self.shootCounter = random.randint(0, BANANERATE - 1)
    def tryToShoot(self, bananeImage):                        
            self.shootCounter += 1
            if self.shootCounter >= BANANERATE:
                self.shootCounter = 0
                return Banane(bananeImage, self.rect.left, self.rect.centery)
            return None

class Baddie2(Baddie):
    def __init__(self,image):
            super().__init__(image)
            self.rect.topleft = (WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - BADDIE2HEIGHT))
            self.speed = BADDIE2SPEED

class Banane:
    def __init__(self,image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speed = BANANESPEED
    def move(self):
        self.rect.move_ip(-self.speed, 0)
    def isOffScreen(self):
        return self.rect.right < 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)
class Mur:
    def __init__(self,image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - MURHEIGHT))
            self.speed = MURSPEED
    def move(self):
            self.rect.move_ip(-self.speed, 0)
    def isOffScreen(self):
            return self.rect.right < 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bonus:
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - BONUSHEIGHT))
        self.speed = BONUSSPEED
    def move(self):
                self.rect.move_ip(-self.speed, 0)
    def isOffScreen(self):
                return self.rect.right < 0
    def draw(self, surface):
            surface.blit(self.image, self.rect)
    

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
gameOverSound = pygame.mixer.Sound('son_perdu.wav') 
pygame.mixer.music.load('musique_plage.mid')

# Set up images.                                                          
baddie1Image = pygame.image.load('monkey.png')                             
baddie1Image = pygame.transform.scale(baddie1Image, (BADDIE1WIDTH, BADDIE1HEIGHT))
baddie2Image = pygame.image.load('gorille_512.png')                             
baddie2Image = pygame.transform.scale(baddie2Image, (BADDIE2WIDTH, BADDIE2HEIGHT))
bananeImage = pygame.image.load('banana_bunch.png')                             
bananeImage = pygame.transform.scale(bananeImage, (BANANEWIDTH, BANANEHEIGHT))
murImage = pygame.image.load('mur_pierre.png')                             
murImage = pygame.transform.scale(murImage, (MURWIDTH, MURHEIGHT))
bonusImage = pygame.image.load('spray_solaire.png')                             
bonusImage = pygame.transform.scale(bonusImage, (BONUSWIDTH, BONUSHEIGHT))

# Show the "Start" screen.
fondsecran = pygame.image.load('menu_attente.png')                             
fondsecran = pygame.transform.scale(fondsecran, (WINDOWWIDTH, WINDOWHEIGHT))
fondsecranjeu = pygame.image.load('decor_plage_coucher.png')                             
fondsecranjeu = pygame.transform.scale(fondsecranjeu, (WINDOWWIDTH, WINDOWHEIGHT))
windowSurface.blit(fondsecran, (0, 0))
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies1 = []
    baddies2 = []
    bananas = []
    murs = []
    bonuses = []
    score = 0
    player = Player()
    baddie1AddCounter = 0
    baddie2AddCounter = 0
    murAddCounter = 0
    bonusAddCounter = 0
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
        baddie1AddCounter += 1
        if baddie1AddCounter == ADDNEWBADDIE1RATE:
            baddie1AddCounter = 0
            baddies1.append(Baddie1(baddie1Image))

        # Add new baddies at the top of the screen, if needed.
        baddie2AddCounter += 1
        if baddie2AddCounter == ADDNEWBADDIE2RATE:
            baddie2AddCounter = 0
            baddies2.append(Baddie2(baddie2Image))

        # Add new murs at the top of the screen, if needed.
        murAddCounter += 1
        if murAddCounter == ADDNEWMURRATE:
            murAddCounter = 0
            murs.append(Mur(murImage))

        # Add new bonuses at the top of the screen, if needed.
        bonusAddCounter += 1
        if bonusAddCounter == ADDNEWBONUSRATE:
            bonusAddCounter = 0
            bonuses.append(Bonus(bonusImage))

        # Move the player around. et faire en sorte que le joueur ne sorte pas de l'écran
        player.keyboardMove()

        # Move the baddies down.
        for b in baddies1:      #vitesse des ennemis
            b.move() #vitesse des ennemis
            banane = b.tryToShoot(bananeImage)    
            if banane is not None:                
                bananas.append(banane)

        # Move the baddies down.
        for b in baddies2:      #vitesse des bananas
            b.move() #vitesse des bananas

        # Move the bananas down.
        for m in bananas:      #vitesse des bananas
            m.move() #vitesse des bananas

        # Move the murs down.
        for o in murs:      #vitesse des murs
             o.move() #vitesse des murs
        
        # Move the bonuses down.
        for p in bonuses:      #vitesse des bonuses
             p.move() #vitesse des bonuses

        # Delete baddies that have fallen past the bottom.
        for b in baddies1[:]:
            if b.isOffScreen():
                baddies1.remove(b)
                
        for b in baddies2[:]:
            if b.isOffScreen():
                baddies2.remove(b)

        # Delete bananas that have fallen past the bottom.
        for m in bananas[:]:
            if m.isOffScreen():
                bananas.remove(m)

        # Delete murs that have fallen past the bottom.
        for o in murs[:]:
            if o.isOffScreen():
                murs.remove(o)

        # Delete bonuses that have fallen past the bottom.
        for p in bonuses[:]:
            if p.isOffScreen():
                bonuses.remove(p)
            if player.rect.colliderect(p.rect):
                score += 10
                bonuses.remove(p)

        # Draw the game world on the window.
        windowSurface.blit(fondsecranjeu, (0, 0))

        # Draw the score and top score. (arrondi à l'entier le plus proche)
        drawText('Score: %s' % (int(score)), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (int(topScore)), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        player.draw(windowSurface)

        # Draw each baddie.
        for b in baddies1:
            b.draw(windowSurface)
        
        for b in baddies2:
            b.draw(windowSurface)

        # Draw each banane.
        for m in bananas:
            m.draw(windowSurface)

        # Draw each mur.
        for o in murs:
            o.draw(windowSurface)
        
        # Draw each bonus.
        for p in bonuses:
            p.draw(windowSurface)

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if player.isHit(baddies1) or player.isHit(baddies2) or player.isHit(bananas) or player.isHit(murs):
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

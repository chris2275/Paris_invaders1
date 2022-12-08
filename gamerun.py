import random
import pygame
import tutorial as t
import menu as men
from background import Background
import time
import time
import save as s
import settings as set

pygame.init()

#NEW_ALIENS = pygame.USEREVENT + 1
#pygame.time.set_timer(NEW_ALIENS, 2000)
#new_aliens = False

lasersound = pygame.mixer.Sound('data/laser.wav')
hitsound = pygame.mixer.Sound('data/hit.wav')

seccount = 0
totaltestseconds = 0

screen_w = set.screen_w
screen_h = set.screen_h
shootloop = 0
alienkills = 0
level = 1
spaceshipkills = 0
colorcounter = 0
timee = ''
ru = True
pausebutton = False
show1 = True
spawnaliens = True
addalien = False
moving_up = False
moving_down = False

clock = pygame.time.Clock()


powerups = [['double shooting ability', False, False, 'allows you to have twice as much lasers as normal on screen'],
          ['half alien velocity', False, False, 'slows down the aliens or the spaceship'],
          ['double laser damage', False, False, 'your lasers do twice as much damage as normal'],
          ['double cannons', False, False, 'allows you to have two cannons on your spaceship'],
          ['Health Boost', False, False, 'replenishes your health by 1/5']]
          # double shooting ability : vous permet d'avoir deux fois plus de lasers que la normale à l'écran
          #half alien velocity : ralentit les aliens ou le vaisseau spatial
          #double laser damage : vos lasers font deux fois plus de dégâts que la normale
          #double cannons : vous permet d'avoir deux canons sur votre vaisseau spatial
          #health boost : reconstitue votre santé de 1/5

holdingpowerup=False
usepowerup=False
poweruploop=0

aliennumber=0
spaceships_number = 0
alienhealth=0
alienlaserdamage=1

yellow=(255,255,0)
black=(0,0,0)
white=(255,255,255)
grey=(150,150,150)
red=(255,0,0)
green=(0,222,0)

color=green


####################################################################################################
#########################  SPACESHIP  ##############################################################
####################################################################################################

class spaceship:
    def __init__(self, x, y):
        self.image = pygame.image.load('data/player_avion2.png')
        self.image = pygame.transform.scale(self.image, (300, 170))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 6
        self.health = set.health_hero
        self.visible = True
        self.hitbox = (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())

    def draw(self, win):
        global powerups
        global usepowerup

        if powerups[4][2]:
            self.health += 40
            if self.health > set.health_hero:
                self.health = set.health_hero
            powerups[4][2] = False
            usepowerup = False

        win.blit(self.image, (self.rect.x, self.rect.y))
        self.hitbox = (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        
    def fire(self):
        global powerups
        if powerups[0][2]:
            le = 10
        else:
            le = 5
        if len(lasers) < le + 10:
            if men.soundchoose.get_tof():
                lasersound.set_volume(men.soundbar.get_Volume())
                lasersound.play()

            if powerups[3][2]:  #permet 2 canons
                lasers.append(laser(self.rect.x + 300, self.rect.y + round(self.image.get_height()/2), yellow))
                lasers.append(laser(self.rect.x + 300, self.rect.y + round(self.image.get_height()/2) + 10, yellow))
            else:
                lasers.append(laser(self.rect.x + 300, self.rect.y + round(self.image.get_height()/2), yellow))


    def drawHealthBar(self,win): # barre de vie spaceship
        font1 = pygame.font.SysFont('comicsans', 30)
        text = font1.render('Health:', 1, red)
        win.blit(text, (5, 5))
        textb = font1.render(str(self.health), 1, red)
        win.blit(textb, (210, 5))
        if self.health > 0:
            pygame.draw.rect(win, red, (15 + text.get_width(), round(text.get_height() / 2), round(self.health/2), 10))

    def hit(self):
        global alienlaserdamage
        self.health -= alienlaserdamage
        hitsound.play()


#########################################################################################################
####################   ENEMYALIEN #######################################################################
#########################################################################################################

class enemyAlien: #personnage alien

    def __init__(self, health, vel):
        self.image = pygame.image.load('data/ennemi.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1800, 10000)
        self.rect.y = random.randrange(0, 1000)
        self.health = health
        self.hitbox = (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()) #largeur et hauteur du futur vaisseau
        self.vel = vel
        self.visible = True
        self.lasercount = 0


    def move(self):
        global powerups
        if powerups[1][2]: #ralenti aliens ou vaisseau
            e = self.vel / 2
        else:
            e = self.vel

        if self.hitbox[0] + self.hitbox[2] - self.vel > 0 - self.hitbox[2]: #(self.x + self.hitbox[0]) - self.vel > 0:
             self.rect.x -= e
            

    def draw(self, win):
        self.move()
        if self.visible:
            self.drawHealthBar(win)
            self.fire()
            win.blit(self.image, (self.rect.x, self.rect.y))

    def drawHealthBar(self, win):
        y = self.hitbox[1] - 10
        healthfont = pygame.font.SysFont('arial', 20)
        text = healthfont.render(str(self.health), 1, red)
        win.blit(text, (self.hitbox[0] + (self.hitbox[2] / 2), y))
            
        

    def fire(self):
        if self.rect.x < set.screen_w:
            if self.lasercount == 0:
                if men.soundchoose.get_tof():# si clique dans la bonne zone
                    lasersound.set_volume(men.soundbar.get_Volume()) #soundbar:instance volumebar
                    #get_Volume:retourne le niveau du son
                    lasersound.play()
                enemylasers.append(laser(self.rect.x, self.rect.y + 50, green))
                self.lasercount = 1

            else:
                self.lasercount += 1
                if self.lasercount > 500:
                    self.lasercount = 0


    def hit(self):
        hitsound.play()

        global powerups
        if powerups[2][2]:
            self.health -= 2
        else:
            self.health -= 1

########################################################################################################
###################    LASER    ########################################################################
########################################################################################################

class laser:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 3
        self.color = color
        self.vel = set.vel_laser
        self.visible = True

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

#######################################################################################################
##########################   ENEMYSPACESHIP   #########################################################
#######################################################################################################

class enemyspaceship:
    def __init__(self):
        self.image = pygame.image.load('data/ennemi.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 1800
        self.rect.y = 500
        self.hitbox = (self.rect.x, self.rect.y, self.image.get_width(),self.image.get_height())  # largeur et hauteur du futur vaisseau
        self.vel = 4
        self.health = 20
        self.lasercount = 0
        self.direc = 'up'


    def draw(self, win):
        self.hitbox = (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        win.blit(self.image, (self.rect.x, self.rect.y))
        self.drawHealthBar(win)
        self.move()
        self.fire()

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.x > 1100:
            self.rect.x -= self.vel
        if self.rect.x == 1100:
            if self.direc == 'up':
                if self.rect.y > 0:
                    self.rect.y -= 4
                    if self.rect.y == 0:
                        self.direc = 'down'
            if self.direc == 'down':
                self.rect.y += 4
                if self.rect.y == set.screen_h - self.image.get_height():
                    self.direc = 'up'

            if self.direc == 'up' and keys[pygame.K_DOWN]:
                self.direc == 'down'
                self.rect.y += 4
                if self.rect.y == set.screen_h - self.image.get_height():
                    self.direc = 'up'
            if self.direc == 'down' and keys[pygame.K_UP]:
                self.direc == 'up '
                if self.rect.y > 0:
                    self.rect.y -= 4
                    if self.rect.y == 0:
                        self.direc = 'down'


    def fire(self):
        if self.rect.x < set.screen_w:
            if self.lasercount == 0:
                if men.soundchoose.get_tof():# si clique dans la bonne zone
                    lasersound.set_volume(men.soundbar.get_Volume()) #soundbar:instance volumebar
                    #get_Volume:retourne le niveau du son
                    lasersound.play()
                enemylasers.append(laser(self.rect.x, self.rect.y + 50, green))
                self.lasercount = 1

            else:
                self.lasercount += 1
                if self.lasercount > 500:
                    self.lasercount = 0



        if self.health > 10:
            seq = 66
        else:
            seq = 33
        if self.lasercount == 0:
            if men.soundchoose.get_tof():
                lasersound.set_volume(men.soundbar.get_Volume())
                lasersound.play()
            enemylasers.append(laser(self.rect.x, self.rect.y, green))
            self.lasercount = 1

        else:
            self.lasercount += 1
            if self.lasercount > seq:
                self.lasercount = 0

    def hit(self):
        hitsound.play()
        self.health -= 1

    def drawHealthBar(self, win):
        y = self.hitbox[1] - 10
        healthfont = pygame.font.SysFont('arial', 20)
        text = healthfont.render(str(self.health), 1, red)
        win.blit(text, (round((self.hitbox[0] + (self.hitbox[2]/2)) - round(text.get_width()/2)), y - 10))

###########################################################################################
###########################################################################################
###########################################################################################

def showLevel(win,level,msg):
    lvlfont=pygame.font.SysFont('comicsans',50)
    text=lvlfont.render('Level: '+str(level),1,white)
    win.blit(text,(350-round(text.get_width()/2),275))

    msgfont=pygame.font.SysFont('comicsans',30)
    text=msgfont.render(msg,1,white)
    win.blit(text,(350-round(text.get_width()/2),315))

    pygame.display.update()
    time.sleep(3) #La méthode de temps Python sleep() suspend l'exécution pendant le nombre de secondes donné

def generateLevel(win,number):
    global powerups
    global addalien
    global level
    global aliennumber
    global spaceships_number
    global alienhealth
    global alienlaserdamage
    global alienvelocity
    global spawnaliens #initialisé a True en début de fichier
    global seccount
    global totaltestseconds
    global levelcounter

    if number == 1:
        global level
        level = 0
        alienkills = 0
        spaceshipkills = 0
        levelcounter = 1
        global battleship
        global show1
        show1 = True
        #battleship = spaceship(50, 250)
        global addalien  #initialisé a False en début de fichier
        #addalien = False
        aliennumber = 15 #nombre d'alien
        spaceships_number = 4
        alienhealth = 2
        alienlaserdamage = 2
        alienvelocity = 3

    if levelcounter == 2:
        alienhealth += 1
        showLevel(win, level+1, 'Alien health +2')
    elif levelcounter == 3:
        alienlaserdamage += 2
        showLevel(win, level+1, 'Alien laser damage +2')
    elif levelcounter == 4:
        alienvelocity += 4
        showLevel(win, level+1, 'Alien velocity +4')
    elif levelcounter == 5:
        showLevel(win, level+1, 'Enemy spaceship attacks')
        levelcounter = 0
        spawnaliens = False
    elif levelcounter == 1 and number != 1:
        for p in powerups:
            if p[1]: #si une des lignes est True , elle deviendra False
                p[1] = False
        a = random.randint(0, len(powerups)-1)
        powerups[a][1] = True #une des lignes au hasard va devenir True

        newpfont = pygame.font.SysFont('comicsans', 50)
        newtext = newpfont.render('New Powerup: ' + powerups[a][0], 1, white)
        win.blit(newtext, (350-round(newtext.get_width()/2), 225))

        exfont = pygame.font.SysFont('comicsans', 30)
        textex = exfont.render(powerups[a][3], 1, white)
        win.blit(textex, (350-round(textex.get_width()/2), 295))

        pygame.display.update()
        time.sleep(2)
        redrawGameWindow(win)

    if spawnaliens:
        for e in range(aliennumber):
            aliens.append(enemyAlien(alienhealth, set.alienvelocity))

    else:
        enemyspaceships.append(enemyspaceship())
        spawnaliens = True


    levelcounter += 1
    level += 1

###########################################################################################

def gameover(win):
    global alienkills
    global spaceshipkills
    global totaltestseconds
    global level
    global aliens
    global lasers
    global enemylasers
    global timee
    pygame.mixer.music.stop()
    helplevel = level
    battleship.health = set.health_hero
    
    ptime = calculateTime()
    if int(ptime[1]) < 10:
        timee=ptime[0] + ':0' + ptime[1]
    else:
        timee=ptime[0] + ':' + ptime[1]
        
    generateLevel(win, 1)
    print(str(helplevel))
    print(str(s.readlevel()))
    if helplevel > s.readlevel():
        s.save(helplevel, alienkills, spaceshipkills, timee, totaltestseconds)
        highscoreloop = True
        hslo = 0
        ybutton = 370
    elif helplevel == s.readlevel() and totaltestseconds > s.readseconds():
        s.save(helplevel, alienkills, spaceshipkills, timee, totaltestseconds)
        highscoreloop = True
        hslo = 0
        ybutton = 370
    else:
        highscoreloop = False
        ybutton = 350
    
    f = True
    g = True
    h = True
    while f:
        try:
            aliens.pop()
        except:
            f = False
    while g:
        try:
            lasers.pop()
        except:
            g = False
    while h:
        try:
            enemylasers.pop()
        except:
            h = False
            
    gaov = True
    while gaov:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ptime = calculateTime()
                if int(ptime[1]) < 10:
                    timee = ptime[0] + ':0' + ptime[1]
                else:
                    timee = ptime[0] + ':' + ptime[1]
                return 0
        pygame.draw.rect(win, yellow, (50, 75, 600, 400)) #cadre resultat final
        pygame.draw.rect(win, black, (60, 85, 580, 380))
        
        gameoverfont = pygame.font.SysFont('comicsansms', 50)
        text = gameoverfont.render('Game Over!', 1, yellow)
        win.blit(text, (350-round(text.get_width()/2), 80))

        statfont = pygame.font.SysFont('comicsans', 30)
        text = statfont.render('Level: '+str(helplevel), 1, white)
        win.blit(text, (350-round(text.get_width()/2), 160))
        
        text=statfont.render('Aliens killed: '+str(alienkills), 1, white)
        win.blit(text, (350-round(text.get_width()/2), 190))

        text=statfont.render('Enemy spaceships destroyed: '+str(spaceshipkills), 1, white)
        win.blit(text, (350-round(text.get_width()/2),220))

        if highscoreloop: # si True : nouveau score
            hslo += 1 # la boucle hslo va permettre l'affichage par intermitence de
            # 'New Highscore!'
            if hslo < 15:
                highfont = pygame.font.SysFont('comicsansms', 40)
                text = highfont.render('New Highscore!', 1, yellow)
                win.blit(text, (350-round(text.get_width()/2), 290))
            elif hslo == 30:
                hslo = 0
                
        text = statfont.render('Survived time: '+timee, 1, white)
        win.blit(text, (350-round(text.get_width()/2), 250))

        exbutton = t.button(win, 'Main Menu', 250, ybutton, 200, 50, yellow, black, yellow)
        if exbutton:
            return 1
        
        pygame.display.update()

def calculateTime():
    global totaltestseconds  #initialisé a 0 en debut de fichier
    minutes = totaltestseconds//60
    seconds = totaltestseconds%60

    return [str(minutes), str(seconds)]

def pause(win):
    global timee
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ptime = calculateTime()
            if int(ptime[1]) < 10:
                timee = ptime[0] + ':0'+ptime[1]
            else:
                timee = ptime[0] + ':'+ptime[1]
            return 0
    
    pygame.draw.rect(win, yellow, (150, 115, 400, 320))
    pygame.draw.rect(win, black, (160, 125, 380, 300))

    paufont = pygame.font.SysFont('comicsansms', 50)
    text = paufont.render('Paused', 1, yellow)
    win.blit(text, (350-round(text.get_width()/2), 120))

    notefont = pygame.font.SysFont('comicsansms', 15)
    text = notefont.render('NOTE: if you quit, you can go back to the current', 1, yellow)
    win.blit(text, (170, 320))
    text = notefont.render('save by just starting the game via the main menu.', 1, yellow)
    win.blit(text, (170, 340))
    text = notefont.render('If you close the whole game with an unfinished save,', 1, yellow)
    win.blit(text, (170,360))
    text = notefont.render('it will be saved regularly but you wont be able to',1,yellow)
    win.blit(text, (170, 380))
    text = notefont.render('finish it.', 1 , yellow)
    win.blit(text, (170, 400))

    resumebutton = t.button(win, 'Resume', 250, 200, 200, 50, yellow, black, yellow)
    if resumebutton: # si clique sur resumebutton
        return 1

    quitbutton = t.button(win, 'Quit', 250, 260, 200, 50, yellow, black, yellow)
    if quitbutton: # si clique sur quitbutton
        ptime = calculateTime()
        if int(ptime[1]) < 10:
            timee=ptime[0] + ':0' + ptime[1]
        else:
            timee=ptime[0] + ':' + ptime[1]
        return 0

    pygame.display.update()

###########################################################################################
        
def redrawGameWindow(win):
    global powerups
    global battleship
    global alienkills
    global spaceshipkills
    global pausebutton
    global holdingpowerup
    global usepowerup
    global poweruploop
    
    #win.blit(gamebg, (0, 0))
    background.update_background(win)

    lvlfont = pygame.font.SysFont('comicsans', 30)
    text = lvlfont.render('Level: '+str(level), 1, white) #texte en haut
    win.blit(text, (350-round(text.get_width()/2), 5))

    text = lvlfont.render('Powerups: ', 1, (0, 0, 255)) #texte Powerups seul en haut ecran
    win.blit(text, (5, 25))

    for powerup in powerups:
        if powerup[1] == True:
            textp = lvlfont.render(powerup[0], 1, white)
            win.blit(textp, (text.get_width()+5, 25))
            holdingpowerup = True

    if holdingpowerup: # holdingpowerup : maintien du pouvoir
        usebutton = t.button(win, 'Use', 5+text.get_width() + textp.get_width()+20, 25, 45, 20, yellow, black, yellow)
        if usebutton:
            holdingpowerup = False
            usepowerup = True #utilisation du pouvoir

    if usepowerup: #utiliser la pouvoir
        for powerup in powerups: #powerup : pouvoir utilisé
            if powerup[1] == True: #remise de powerup a False
                powerup[1] = False
                powerup[2] = True # 2eme booleen passe a True

    for powerup in powerups:
        if powerup[2]:
            textp = lvlfont.render(powerup[0], 1, white)
            win.blit(textp, (text.get_width()+5, 25))
            poweruploop += 1
            if poweruploop == 720:
                poweruploop = 0
                powerup[2] = False
                usepowerup = False

    if not holdingpowerup and not usepowerup:
        textp = lvlfont.render('none', 1, white)
        win.blit(textp, (text.get_width()+5, 25))
        
    
    pausebutton = t.button(win, 'Pause', 625, 10, 65, 30, yellow, black, yellow)
    
    keys = pygame.key.get_pressed()
    if pausebutton or keys[pygame.K_ESCAPE]: #if pausebutton = si clique sur pause
        pause(win)

    for laser in lasers:
        laser.draw(win)

    for laser in enemylasers:
        laser.draw(win)

    for alien in aliens:
        if alien.health >= 1:
            alien.draw(win)
        else:
            aliens.pop(aliens.index(alien))
            alienkills += 1
        if alien.rect.x + alien.hitbox[2] < 0:
            aliens.pop(aliens.index(alien))

    for v in enemyspaceships:
        if v.health >= 1:
            v.draw(win)
        else:
            enemyspaceships.pop()
            spaceshipkills += 1
            

    if battleship.visible:   #battleship : instance héro
        battleship.draw(win)
    battleship.drawHealthBar(win)# barre de vie

    pygame.display.update()


battleship = spaceship(50, 350) #instance héro
background = Background()
background.load_images()
clock = pygame.time.Clock()
lasers = []
enemylasers = []
aliens = []
enemyspaceships = []

def run(win):
    global alienkills
    global spaceshipkills
    global battleship
    global ru
    global seccount
    global pausebutton
    global totaltestseconds
    global timee
    global new_aliens

    clock.tick(60)

    seccount += 1
    if seccount == 60:
        totaltestseconds += 1
        seccount = 0

    redrawGameWindow(win)
    
    global show1  #variable initialisé a True en debut de fichier
    if show1:
        alienkills = 0
        spaceshipkills = 0
        generateLevel(win, 1) #on appelle une seule fois generateLevel dans run
        showLevel(win, level, '')
        totaltestseconds = 0
        seccount = 1
        show1 = False
        
    global shootloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ptime = calculateTime() #retourne le temps en minute et secondes
            if int(ptime[1]) < 10: #ptime[1] = secondes
                timee = ptime[0] + ':0' + ptime[1]
            else:
                timee = ptime[0] + ':' + ptime[1]
            return 0

    if battleship.visible:
        global moving_up
        global moving_down

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if battleship.rect.x > battleship.vel: #permet de ne pas sortir sur la gauche
                battleship.rect.x -= battleship.vel

        if keys[pygame.K_RIGHT]:
            if battleship.rect.x < screen_w - battleship.hitbox[2] - battleship.vel: #breite : largeur
                battleship.rect.x += battleship.vel

        if keys[pygame.K_UP]:
            if battleship.rect.y > 0:
                battleship.rect.y -= battleship.vel
                moving_up = True
        else:
            moving_up = False

        if keys[pygame.K_DOWN]:
            if battleship.rect.y < screen_h - battleship.hitbox[3] - battleship.vel:
                battleship.rect.y += battleship.vel
                moving_down = True
        else:
            moving_down = False

        if keys[pygame.K_SPACE]:
            if shootloop == 0:
                battleship.fire()
                shootloop = 1

    if shootloop > 0:  #boucle d'attente entre 2 tirs héro
        shootloop += 1
    if shootloop > set.interval_fire:
        shootloop = 0

    for laser in lasers: #deplacement par le haut du laser du vaisseau héros jusqu'a 10 pixels
        if laser.x < screen_w:
            laser.x += laser.vel
           
        else:
            lasers.pop(lasers.index(laser)) #supression laser héros si sortie par la gauche

        for e in enemylasers:#on inbrique ce for car permet de recuperer de laser.x et laser.y
            xx = e.x - laser.x #distance x entre le laser enemie et le laser héro
            yy = e.y - laser.y #distance y entre le laser enemie et le laser héro

            if xx < 10 and yy < 10 and yy > -10 and xx > -10 : #permet de gerer la collision entre les lasers du héros et les lasers aliens si elle est comprise entre 5 et -5 ,c'est qu'il y a collision et on le supprime
                enemylasers.pop(enemylasers.index(e)) #suppression laser enemies si collision
                #enemylasers regroupe les lasers de tous les groupes d'aliens
                lasers.pop(lasers.index(laser)) #supression laser héros si collision

            
    for alien in aliens: #aliens = 1 er groupe d'aliens
    #gestion collision du laser héros avec chaque aliens
        if alien.visible: #if alien.visible = True
            for laser in lasers: #lasers:liste lasers héros
               if laser.x + laser.width > alien.rect.x and laser.x + laser.width < alien.rect.x + alien.hitbox[2]:
                    if laser.y + laser.height > alien.rect.y and laser.y + laser.height < alien.rect.y  + alien.hitbox[3]:
                        alien.hit()
                        lasers.pop(lasers.index(laser))


    for v in enemyspaceships: #gestion collision laser héro avec second groupe aliens
        for laser in lasers:
            if laser.y < v.hitbox[1] + v.hitbox[3] and laser.y > v.hitbox[1]:#c'est a dire s'ilest en plein dans le corps de l'enemi  en y 
               if laser.x > v.hitbox[0] and laser.x < v.hitbox[0] + v.hitbox[2]:
                        v.hit()
                        lasers.pop(lasers.index(laser))
            elif laser.y + laser.height < v.hitbox[1] + v.hitbox[3] and laser.y + laser.height > v.hitbox[1]:
                    if laser.x > v.hitbox[0] and laser.x < v.hitbox[0] + v.hitbox[2]:
                        v.hit()
                        lasers.pop(lasers.index(laser))

    for laser in enemylasers:#gestion de la collision des lasers de tous les enemi vers le vaisseau héro
        #if laser.y + laser.height > battleship.hitbox[1] + 5 and laser.y < battleship.hitbox[1] + battleship.hitbox[3]:
        if laser.x < battleship.hitbox[0] + battleship.hitbox[2] and laser.x > battleship.hitbox[0]:
            if laser.y + laser.height > battleship.hitbox[1] and laser.y < battleship.hitbox[1] + battleship.hitbox[3]:
                battleship.hit()
                enemylasers.pop(enemylasers.index(laser))

    for laser in enemylasers: #gestion sortie de tous les lasers enemies
        if laser.x > 0:
            laser.x -= laser.vel
        else:
            enemylasers.pop(enemylasers.index(laser))

    if battleship.health <= 0:
        if not ru: # ru : boucle qui permet de laisser le menu gameover affiché tant que
        # pas clique sur quit ou main menu ?
            go = gameover(win)
            if go == 0 or go == 1: # si cliqué sur quit ou main menu
                ru = True
                return go # go valeur de retour fonction gameover,soit 0, soit 1
        ru = False

    if len(aliens) == 0 and len(enemyspaceships) == 0:
    # si plus d'enemis , on supprime tous les lasers héros et enemis
        l = True
        while l:
            try:
                lasers.pop() #lasers du héro
            except:
                l = False
        e = True
        while e:
            try:
                enemylasers.pop()
            except:
                e = False
        redrawGameWindow(win)
        generateLevel(win, 0)

    keys = pygame.key.get_pressed()
    if pausebutton or keys[pygame.K_ESCAPE]:
        pausebutton = False
        pau = True
        while pau:
            g = pause(win)
            if g == 1:
                pau = False
            elif g == 0:
                pau = False
                return 1

import pygame
import tutorial as t
import save as s
import settings as set
pygame.init()
clock = pygame.time.Clock()

yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
green = (0, 222, 0)

screen_w = set.screen_w
screen_h = set.screen_h

mushelp = False
soundhelp = False
laser = pygame.mixer.Sound('data/laser.wav')

soundvol = 0.5
musicvol = 0.5

class volumebar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vollevel = 50
        self.volume = 0.5
        self.maxvol = 100
        self.minvol = 0
        self.soundplay = False

    def calcvolume(self):
        return self.vollevel / 100
    
    def drawchest(self, win, x, msg, fill, col):#fonction qui sert a dessiner chacune des 4 boites de son
    	#couleur de fond ,couleur du texte et texte
        pygame.draw.rect(win, yellow, (x, self.y, 35, 35), fill)
        font2 = pygame.font.SysFont('comicsansms', 30)
        text = font2.render(msg, 1, col)
        win.blit(text, (round(x + (35/2 - text.get_width()/2)), round(self.y + (35 / 2 - text.get_height()/2))))
        
    def checkchest(self, win): #chest signifie boite
    #du 1er if au 1 er else:si seulement survol des 2 boites volume de gauche,changement
    #de couleur des signes  
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + 35 and self.y < mouse[1] < self.y + 35:
            self.drawchest(win, self.x, '-', 0, black)
            if click[0] == 1 and self.minvol < self.vollevel <= self.maxvol:
             #si en plus clic dans la zone, emission d'un son + augmentation du son de 5
                self.soundplay = True
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                self.vollevel -= 5
                self.volume = self.calcvolume()

        else:
        #si pas survol des 2 boites de gauche , vola la couleur affichée
            self.drawchest(win, self.x, '-', 1, yellow)

	#meme chose pour les 2 boites de droite
        if self.x + 255 < mouse[0] < self.x + 290 and self.y < mouse[1] < self.y + 35:
            self.drawchest(win, self.x + 255, '+', 0, black)
            if click[0] == 1 and self.minvol <= self.vollevel < self.maxvol:
                self.soundplay = True
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                self.vollevel += 5
                self.volume = self.calcvolume()
        else:
            self.drawchest(win, self.x + 255, '+', 1, yellow)
            
    
    def draw(self, win):
        if self.vollevel != 0: #si volume est superieur a zero , apparition de la barre dont la largeur augmente a chaque clique est volume augmente aussi
            pygame.draw.rect(win, yellow, (self.x + 45, self.y + 17, 2 * self.vollevel, 5))
        self.checkchest(win)

    def get_Volume(self):
        return self.volume
        

class choosebutton:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tof=True

    def check(self):#permet de savoir si le joueur clique et s'il clique dans la bonne zone(boutton)
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + 120 and self.y < mouse[1] < self.y + 30:
            if self.tof == False and click[0] == 1:
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                    self.tof = True

        if self.x + 170 < mouse[0] < self.x + 270 and self.y < mouse[1] < self.y + 30:
            if self.tof == True and click[0] == 1:
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                    self.tof = False

    def draw(self,win):
        
        if self.tof: # si pas clique
            colortext1=black
            colortext2=yellow
            c1=0
            c2=1
        else:
            colortext1=yellow
            colortext2=black
            c1=1
            c2=0

        pygame.draw.rect(win,yellow,(self.x,self.y,120,30),c1)# c1:parametre utilisé pour dessiner un rectangle aux coins arrondis
        font1=pygame.font.SysFont('comicsansms',20)
        text=font1.render('ON',1,colortext1)
        win.blit(text, (round(self.x + (120/2 - text.get_width()/2)),round( self.y + (30/2 - text.get_height()/2))))

        pygame.draw.rect(win,yellow,(self.x+170,self.y,120,30),c2)
        font1=pygame.font.SysFont('comicsansms',20)
        text=font1.render('OFF',1,colortext2)
        win.blit(text, (round(self.x+170 + (120/2 - text.get_width()/2)),round( self.y + (30/2 - text.get_height()/2))))

        self.check()#permet de savoir si le joueur clique et s'il clique dans la bonne zone(boutton)
        
    def get_tof(self):# permet de savoir la couleur du boutton ,soit jaune,soit black suivant que ca retourne 
        # true ou false
        if self.tof:
            return True
        return False

def drawMenuLayout(win):
    win.fill((0,0,0))
    font1=pygame.font.SysFont('comicsansms',80)
    text=font1.render('PARIS INVADERS',1,yellow)
    win.blit(text,(20,10))
    font2=pygame.font.SysFont('comicsansms',15)
    text2=font2.render('v.1.0.0',1,white)
    win.blit(text2,(screen_w-text2.get_width()-20,screen_h-text2.get_height()-5))

    #t.drawtutorialship(win,50,400)#representation du vaisseau bas page acceuil
    #representation vaisseau haut page d'acceuil
    #pygame.draw.rect(win,grey,(90,150,70,50))
    #pygame.draw.rect(win,green,(160,150,20,35))
    #pygame.draw.rect(win,green,(70,150,20,35))
    #pygame.draw.rect(win,white,(120,200,10,20))
    #pygame.draw.rect(win,green,(122,260,3,30))
    

def drawChooseTutorial(win):#boutton tutorial , gestion du yes , no ou back
    drawMenuLayout(win)#inscription yellow spaceship,v.1.0.0
    font1=pygame.font.SysFont('comicsansms',30)
    text=font1.render('Do you want to do the tutorial?',1,white)
    win.blit(text,(230,170))

    global yesbutton
    global nobutton
    global backbutton
    
    #fonction button :gestion taille boutons (largeur + taille caracteres(size) en fonction du message) et gestion du cliquage sur le boutton ou non 
    yesbutton=t.button(win,'Yes',270,280,150,50,yellow,black,yellow)
    nobutton=t.button(win,'No',470,280,150,50,yellow,black,yellow)
    backbutton=t.button(win,'Back',470,470,150,50,yellow,black,yellow)

    pygame.display.update()

def redrawMenuWindow(win):# affichage tous les boutons sauf vaisseaux page acceuil
    drawMenuLayout(win)#affichage yellow spaceship,v.1.0.0
    
    global button1
    global button2
    global button3
    global button4
    global button5
    button1=t.button(win,'Play!',470,150,150,50,yellow,black,yellow)
    #fonction button creer le boutton et dit si clique dessus ou pas
    button2=t.button(win,'Settings',470,220,150,50,yellow,black,yellow)
    button3=t.button(win,'Score',470,290,150,50,yellow,black,yellow)
    button4=t.button(win,'Credits',470,360,150,50,yellow,black,yellow)
    button5=t.button(win,'Quit',470,430,150,50,yellow,black,yellow)

    pygame.display.update()

def drawSettings(win):
    # affichage vaisseau haut et bas a gauche ecran + laser
    #affichage "Volume"x 2, "Sounds", 
    #affichage boutton (on off)x2 + insription "ON"x2, "OFF"x2,
    #affichage boutton back + inscription 'Back'
    #affichage en gros caractere " Yellow Spaceship"
    drawMenuLayout(win)#affichage yellow spaceship,v.1.0.0
    global backbutton
    backbutton=t.button(win,'Back',470,470,150,50,yellow,black,yellow)
    
    font1=pygame.font.SysFont('comicsansms',20)
    text=font1.render('Music:',1,white)
    win.blit(text,(300,140))
    text=font1.render('Sounds:',1,white)
    win.blit(text,(290,300))
    global mushelp
    global soundhelp
    musicchoose.draw(win)#musicchose est une instance de la classe choosebutton , la fonction draw de la classe choosebutton check s'il y a 'clique' du boutton ON et OFF , auquel cas , la couleur noire passera au jaune 
    # puis musique coupé egalement
    
    if musicchoose.get_tof() and mushelp: # si get_off est true( c'est a dire si pas clique ,texte en noire ,et si la variable mushelp est True(variable a False en haut de ce fichier)
        mushelp=False
        pygame.mixer.music.play(-1)
    elif not(musicchoose.get_tof()):
        pygame.mixer.music.stop()
        mushelp=True  # la var "mushelp" permet de savoir si la musique est coupé ou pas , si mushelp est a 
        #True , la musique est coupée

    if musicchoose.tof:#musicchose instance de la classe choosebutton permet d'atteindre la variable 
    #self.tof quii est initialement a True
        
        text=font1.render('Volume:',1,white)
        win.blit(text,(round(370+290/2-text.get_width()/2),180))
        musicbar.draw(win) #musicbar est une instance de Volumebar et fonction draw affiche la barre dont la taille progresse en fonction de l'augmentation du volume
        
        pygame.mixer.music.set_volume(musicbar.get_Volume()) #la fonction get_volume de l'instance musicbar retourne le volume et pygame.mixer.music.set_volume permet de changer le volume
        
    soundchoose.draw(win) #soundchoose est une instance de choosebutton 
    if soundchoose.get_tof() and soundhelp: #si get_off est true( c'est a dire si pas clique ,texte en jaune ,et si la variable mushelp est True(variable a False en haut de ce fichier)
        soundhelp=False
        laser.play()
    elif not(soundchoose.get_tof()):
        soundhelp=True
        
    if soundchoose.tof: #tof = si cliqué sur on , le texte volume ne blanc apparait
        text=font1.render('Volume:',1,white)
        win.blit(text,(round(370+290/2-text.get_width()/2),340))
        soundbar.draw(win) #soundbar est instance de volumebar et fonction draw : si volume est superieur a zero , apparition de la barre dont la largeur augmente a chaque clique est volume augmente aussi
        laser.set_volume(soundbar.get_Volume())
        if soundbar.soundplay:
            laser.play()
            soundbar.soundplay=False
            
    pygame.display.update()

def drawscorewin(win):
    drawMenuLayout(win)#inscription yellow spaceship,v.1.0.0
    global backbutton
    backbutton=t.button(win,'Back',470,470,150,50,yellow,black,yellow)

    try:
        scorearray=s.read()

        datefont=pygame.font.SysFont('comicsansms',30)
        text=datefont.render('Best save with this game file:',1,white)
        win.blit(text,(250,130))
        text=datefont.render('Date: '+scorearray[0],1,white)
        win.blit(text,(250,210))
        text=datefont.render('Reached Level: '+str(scorearray[1]),1,white)
        win.blit(text,(250,250))
        text=datefont.render('Aliens killed: '+scorearray[2],1,white)
        win.blit(text,(250,290))
        text=datefont.render('Spaceships destroyed: '+scorearray[3],1,white)
        win.blit(text,(250,330))
        text=datefont.render('Survived time: '+scorearray[4],1,white)
        win.blit(text,(250,370))

    except:
        datefont=pygame.font.SysFont('comicsansms',20)
        text=datefont.render('You haven´t played a game with this game',1,white)
        win.blit(text,(250,130))
        text=datefont.render('file so far.',1,white)
        win.blit(text,(250,160))
        text=datefont.render("Just begin your first game by clicking 'Play!'",1,white)
        win.blit(text,(250,220))
        text=datefont.render("on the main menu. You can do the tutorial first",1,white)
        win.blit(text,(250,250))
        text=datefont.render("if you want to.",1,white)
        win.blit(text,(250,280))
        text=datefont.render("Good luck! You´re gonna need it :P",1,white)
        win.blit(text,(250,330))

    pygame.display.update()

def drawCredits(win):
    drawMenuLayout(win)#inscription yellow spaceship,v.1.0.0
    crefont=pygame.font.SysFont('comicsansms',30)
    text=crefont.render('Credits:',1,white)
    win.blit(text,(250,130))
    cfont=pygame.font.SysFont('comicsansms',20)
    text=cfont.render('Menu music: "Epic" from Bensound.com',1,white)
    win.blit(text,(250,170))
    text=cfont.render('Game music: "Evolution" from Bensound.com',1,white)
    win.blit(text,(250,200))
    text=cfont.render('Space picture: "Milchstraße" by Felix',1,white)
    win.blit(text,(250,230))
    text=cfont.render('Mittermeier on pixabay.com',1,white)
    win.blit(text,(250,260))
    text=cfont.render('Version: 1.0.0',1,white)
    win.blit(text,(250,320))
    text=cfont.render('made with IDLE 3.8.3 and pygame 1.9.6',1,white)
    win.blit(text,(250,350))
    text=cfont.render('.exe-version converted with cx_Freeze 6.1',1,white)
    win.blit(text,(250,380))
    global nextbutton
    nextbutton=t.button(win,'Next',470,470,150,50,yellow,black,yellow)

    pygame.display.update()

def drawCredits2(win):
    drawMenuLayout(win)#inscription yellow spaceship,v.1.0.0
    crefont=pygame.font.SysFont('comicsansms',30)
    text=crefont.render('Credits:',1,white)
    win.blit(text,(250,130))

    cfont=pygame.font.SysFont('comicsansms',20)
    text=cfont.render('Alien pictures, ingame sounds: Tech with Tims',1,white)
    win.blit(text,(250,170))
    text=cfont.render('pygame tutorial (I highy recommend checking',1,white)
    win.blit(text,(250,200))
    text=cfont.render('him out he makes awesome tutorials/videos).',1,white)
    win.blit(text,(250,230))
    text=cfont.render('If you find any bugs or have suggestions or',1,white)
    win.blit(text,(250,290))
    text=cfont.render('ideas feel free to contact me (GitHub:',1,white)
    win.blit(text,(250,320))
    text=cfont.render('@ph3nix-cpu or just use the comment section',1,white)
    win.blit(text,(250,350))
    text=cfont.render('on pygame.org.',1,white)
    win.blit(text,(250,380))
    text=cfont.render('Thank you for playing, I hope you enjoy it!',1,white)
    win.blit(text,(250,425))
    
    global backbutton
    backbutton=t.button(win,'Back',470,470,150,50,yellow,black,yellow)

    pygame.display.update()

def drawquit(win):
    drawMenuLayout(win)#inscription yellow spaceship,v.1.0.0
    font1=pygame.font.SysFont('comicsansms',30)
    text=font1.render('Are you sure you want to quit?',1,white)
    win.blit(text,(250,150))

    font2=pygame.font.SysFont('comicsansms',30)
    text=font1.render('Your highscore will be saved!',1,white)
    win.blit(text,(250,200))
    
    global yesbutton
    global nobutton
    yesbutton=t.button(win,'Yes',250,280,150,50,yellow,black,yellow)
    nobutton=t.button(win,'No',450,280,150,50,yellow,black,yellow)

    pygame.display.update()


musicchoose=choosebutton(370,140)
musicbar=volumebar(370,205)
soundchoose=choosebutton(370,300)
soundbar=volumebar(370,365)

def menu(win):
    clock.tick(30)   
    redrawMenuWindow(win)# affichage tous les boutons sauf vaisseaux page acceuil et retourne si
    #appuyer sur soit play soit settings etc...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
    if button1: #bouton play du menu , si clique sur play on passe dabord a la page tutorial
        # a savoir soit oui ou non tutorial ou back vers le premier menu
        choosetut = True   #choosetut = choix tutorial
        while choosetut:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0 #si le retour est 0 ,menu=False et game=False ( dans fichier main)
                    	     #si le retour est 1 , run=True et menu=False (dans fichier main)
            drawChooseTutorial(win)#boutton tutorial , gestion du yes , no ou back
            if yesbutton:# appelle la fonction button dans fichier tutorial retourne si le bouton est True ou False et la fonction button gere le cliquage sur le boutton ou non (boutton yes)
                tutorial = True
                while tutorial:
                    clock.tick(30)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return 0
                    drawMenuLayout(win)# affichage yellow spaceship + vaisseau haut et bas sur page acceuil
                    num = t.doTutorial(win) #affichage des differentes pages du tutorial
                    #retourne soi 0 , 1 ou 2
                    if num == 1:
                        return 1
                    elif num == 2:
                        tutorial = False
                        choosetut = False
            if nobutton:# boutton no
                return 1 # la boucle run du fichier main est True
            if backbutton:  #boutton back
                choosetut = False
    if button2: # boutton settings du menu
        settings = True
        while settings:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawSettings(win) #1 ere page credit
            if backbutton:
                settings = False
    if button3:  #score
        scorewin = True
        while scorewin:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawscorewin(win)
            if backbutton:
                scorewin = False

    if button4:  #boutton credits du menu
        credit = True
        while credit:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawCredits(win)# page settings avec reglages divers
            if nextbutton:
                credit2 = True
                credit = False
        while credit2:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawCredits2(win)
            if backbutton:
                credit2 = False
        
    if button5:  #boutton quit du menu
        quitt = True
        while quitt:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawquit(win)
            if yesbutton:
                return 0
            if nobutton:
                quitt = False

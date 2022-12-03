def start():
    import gamerun
    import pygame
    import menu as men
    import save as s
    import settings as set

    pygame.init()

    screen_w = set.screen_w
    screen_h = set.screen_h
    win = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption('Paris_invaders')
    clock = pygame.time.Clock()

    game = True
    menu = True
    run = False

    yellow = (255, 255,  0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (150, 150, 150)

    while game:
        pygame.mixer.music.load('data/bensound-epic.mp3')
        #musicbar est une instance de Volumebar dans fichier menu et la fonction get_volume retourne le volume
        pygame.mixer.music.set_volume(men.musicbar.get_Volume())
        pygame.mixer.music.play(-1)
    
        while menu:
            number=men.menu(win)
            if number==0:
                menu=False
                game=False
            elif number==1:
                run=True
                menu=False
    
        pygame.mixer.music.stop()  # si pas menu la musique est arreté     
        if men.musicchoose.get_tof():#get_tof retourne si le boutton permettant la musique a été enfoncé
            #musicchoose est une instance de Choosebutton dans fichier menu
            pygame.mixer.music.load('data/bensound-evolution.mp3')
            pygame.mixer.music.set_volume(men.musicbar.get_Volume())
            pygame.mixer.music.play(-1)

        while run:
            num=gamerun.run(win)#retourne 0 ou 1
            if num==0:
                run=False
                game=False
            if num==1:
                run=False
                menu=True
                
    if gamerun.level > s.readlevel():#fonction dans save qui retourne le level incrit dans un fichier .txt
    	#fonction save() dans save sauvegarde level,alienkills,shipkills,etc...enregisre aussi date et heure
        s.save(gamerun.level,gamerun.alienkills,gamerun.spaceshipkills,gamerun.timee,gamerun.totaltestseconds)
    elif gamerun.totaltestseconds > s.readseconds() and gamerun.level == s.readlevel():
        s.save(gamerun.level,gamerun.alienkills,gamerun.spaceshipkills,gamerun.timee,gamerun.totaltestseconds)
    pygame.quit()

if __name__=='__main__':
    start()

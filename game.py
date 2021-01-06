import pygame
from pygame import locals as pgvar
from sys import exit
from cowboy import Cowboy
from train import Train
from card import Card
from network import Network
import json


class Game():

    def __init__(self,single):
        with open("PlayerConf.json","r") as infile:
            settings = json.load(infile)
        for param,val in settings.items():
            try:
                exec("self."+param+"="+str(val))
            except NameError:
                exec("self."+param+"='"+str(val)+"'")
        # Assertoins for the game to run
        if (not single):
            self.net = Network(self.serverip,self.port)
            self.id = self.net.id
            self.nPlayers = self.net.nPlayers
        else:
            self.nPlayers = 5
            self.id = 1
        assert self.width >= self.height, "Screen not wide enough! Change width in settins.json"
        assert self.nPlayers > 0, "Need at least 1 Player"
        assert self.nPlayers < 7, "Too many players, I can't count that many"


        # Variable declarations
        self.players = [] # List of cowboy objects, representing the players
        self.cards = [] # List of card objects, that you can choose from
        self.train = Train(nWagons=self.nPlayers+1,screenW = self.width,screenH = self.height)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE)
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface,(self.width,self.height))
        self.msCount = 0
        self.nextAction = None
        pygame.init()
        self.alive = 1
        self.chooseState = 1
        self.playerinit()
        self.cardsinit()
        self.actionQ = [("2","Turn")]
        #[("1","Move"),("3","Turn"),("3","Move"),("4","Turn"),("4","move"),("4","move"),("5","Turn"),("5","move"),("5","move"),("5","move"),("2","Jump"),("2","Jump")]
        self.wait = 0

        # Init for displaying text
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS",40)

        print("INIT FINSHED")
    

    def cardsinit(self):
        setattr(Card,'_gameP',self)
        setattr(Card,"screenW",self.width)
        setattr(Card,"screenH",self.height)
        for action in ["Jump","Move","Shoot","Turn"]:
            self.cards.append(Card(action))

    def playerinit(self):
        # Sets some instance variables, unfortunately not class variables
        setattr(Cowboy,'_gameP',self)
        setattr(Cowboy,"_trainP",self.train)
        setattr(Cowboy,"screenW",self.width)
        setattr(Cowboy,"screenH",self.height)

        for i in range(1,self.nPlayers+1):
            CB = Cowboy(wagonI = i,flip=False)
            self.players.append(CB)
        self.placeCowboys()

    def killPlayer(self,player : Cowboy):
        obj = self.players.pop(self.players.index(player))
        del obj
        self.alive = 0
        self.nPlayers -=1

    def placeCowboys(self):
        for i in range(len(self.train.wagons)):
            self.train.wagons[i].placeCB(True)
            self.train.wagons[i].placeCB(False)

    def createText(self,text):
        self.textsurface = self.myfont.render(text,False,(0,0,0))
    
    def deleteText(self):
        del self.textsurface

    def playerAction(self,nextAction):
        """
        nextAction : tuple[string,string]
        - Cotains at index=0 the playerID, and at index=1 the action to be performed
        """
        player = int(nextAction[0])
        action = nextAction[1].lower()
        exec(f"self.players[player-1].{action}()")
        print("executed",player,action)

    def NextAction(self):
        while(len(self.actionQ) > 0):
            # Loads next action to be done
            nextAction = self.actionQ.pop(0)
            # Displays what the next action is and who does it
            # Displays for 180 ticks (3s)
            text = f"Player {nextAction[0]} {nextAction[1]}s"
            self.createText(text = text)
            self.waitLoop(180)
            self.deleteText()
            # Performs the action and waits 120 ticks (2s)
            self.playerAction(nextAction = nextAction)
            self.waitLoop(120)
        self.chooseState = 1
    
    def baseDrawWindow(self):
        self.screen.blit(self.bg_surface,(0,0))
        self.train.animate(self.screen)
        for i in range(len(self.players)):
            self.players[i].animate(self.screen,self.msCount)
    
        try:
            #If variabel exists
            X = self.width//2 - self.textsurface.get_width()//2
            Y = self.height//2 - self.textsurface.get_height()//2
            self.screen.blit(self.textsurface,(X,Y))
        except AttributeError:
            pass

    def drawWindow(self,wait = False):
        """
        wait : bool
        - True if only base should be drawed
        """
        self.baseDrawWindow()
        if(wait):
            pygame.display.update()
            return
        #if we are in the option state
        if(self.chooseState and self.alive):
            for i in range(4):
                self.cards[i].animate(self.screen,self.msCount)
        else:
            #Action state
            if(self.msCount % 180 == 0):
                self.NextAction()
                
        pygame.display.update()

    def resizeWindow(self):
        print("Resized Window",self.width,self.height)
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface , (self.width,self.height))
        self.train.resize(self.width,self.height)
        for i in range(self.nPlayers):
            print("Resized player",i+1)
            self.players[i].resize(self.width,self.height)
        
        self.placeCowboys()

        if(self.chooseState):
            for i in range(len(self.cards)):
                self.cards[i].resize(self.width,self.height)
        

    def gameInteraction(self,event):
        x,y = pygame.mouse.get_pos()
        if(self.chooseState):
            for i in range(4):
                self.cards[i].checkmousePos(x,y)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.chooseState = abs(self.chooseState-1)

            if event.key == pgvar.K_ESCAPE:
                run = False

            if event.key == pgvar.K_j:
                self.players[self.id-1].jump()

            if event.key == pgvar.K_m:
                self.players[self.id-1].move()

            if event.key == pgvar.K_t:
                self.players[self.id-1].turn()

            if event.key == pgvar.K_s:
                self.players[self.id-1].shoot()
    
    def eventChecker(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pgvar.K_ESCAPE):
                run = False
            if event.type == pygame.VIDEORESIZE:
                self.width = event.dict['size'][0]
                self.height = event.dict['size'][1]
                self.resizeWindow()
            if (self.alive):
                self.gameInteraction(event)
            
        return run
    
    def waitLoop(self,waitTicks):
        self.wait = waitTicks
        while(self.wait != 0):
            self.drawWindow(wait=True)
            self.msCount +=1
            self.msCount %= 10000
            self.clock.tick(60)
            self.wait -= 1
        return


    def gameloop(self):
        run = True
        while(run):
            run = self.eventChecker()

            
            self.drawWindow()

            self.train.assertions(self.nPlayers)
            
            self.msCount +=1
            self.msCount %= 10000
            self.clock.tick(60)
        
        pygame.quit()

    def close(self):
        with open("PlayerConf.json","r") as infile:
            settings = json.load(infile)
        settings["height"] = self.height
        settings["width"] = self.width
        with open("PlayerConf.json","w") as outfile:
            json.dump(settings,outfile,indent=2)

    def run(self):
        self.gameloop()





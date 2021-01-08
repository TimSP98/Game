import pygame
from pygame import locals as pgvar
from sys import exit
from cowboy import Cowboy
from train import Train
from card import Card
from button import Button
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
        self.single = single
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
        self.buttoninit()

        self.chosenCardCount = 0
        self.actionQ = [("2","Turn")]
        #[("1","Move"),("3","Turn"),("3","Move"),("4","Turn"),("4","move"),("4","move"),("5","Turn"),("5","move"),("5","move"),("5","move"),("2","Jump"),("2","Jump")]
        self.wait = 0
        self.drag = False

        # Init for displaying text
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS",100)
        self.resizeWindow()
        print("INIT FINSHED")
    
    def buttoninit(self):
        setattr(Button,"_gameP",self)
        setattr(Button,"screenW",self.width)
        setattr(Button,"screenH",self.height)
        self.submitButton = Button(action = "Submit")

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
        if(self.id == obj.playerID):
            self.alive = 0
        del obj
        self.nPlayers -=1

    def placeCowboys(self):
        for i in range(len(self.train.wagons)):
            self.train.wagons[i].placeCB(True)
            self.train.wagons[i].placeCB(False)

    def displayGameText(self,text,time):
        """
        text : string
        - The string to be displayed on the screen

        time : int
        - Amount of game ticks that the text should be displayed
        """
        self.textsurface = self.myfont.render(text,False,(0,0,0))
        self.waitLoop(time)
        del self.textsurface

    def playerAction(self,nextAction):
        """
        nextAction : tuple[string,string]
        - Cotains at index=0 the playerID, and at index=1 the action to be performed
        """
        player = int(nextAction[0])
        action = nextAction[1].lower()
        pi = -1
        for i in range(len(self.players)):
            if(self.players[i].playerID == player):
                pi = i
                break
        if(pi != -1):
            exec(f"self.players[{pi}].{action}()")
        else:
            text = f"Player {player} is unfortunately dead"
            self.displayGameText(text = text,time = 120)

    def actionExec(self):
        while(len(self.actionQ) > 0):
            # Loads next action to be done
            nextAction = self.actionQ.pop(0)
            # Displays what the next action is and who does it
            # Displays for 180 ticks (3s)
            text = f"Player {nextAction[0]} {nextAction[1]}s"
            self.displayGameText(text = text,time = 180)
            # Performs the action and waits 120 ticks (2s)
            self.playerAction(nextAction = nextAction)
            self.waitLoop(120)
        self.chooseState = 1

    def submit(self):
        actions = []
        for i in range(len(self.cards)):
            if(self.cards[i].chosen):
                actions.append((self.cards[i].num,(self.id,self.cards[i].action)))
        if(len(actions) != 3):
            print("Choose more you dumb fuck")
            return
        
        actions.sort()
        actions = [tup for _ , tup in actions]
        if(not self.single):
            self.net.send(data = actions, dataType = 1)
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
            self.submitButton.animate(self.screen)
        elif(not self.chooseState):
            #Action state
            if(self.msCount % 180 == 0):
                self.actionExec()
                
        pygame.display.update()

    def chooseCard(self,card):
        if(card.chosen):
            #unChoose
            for i in range(4):
                if(self.cards[i] != card and self.cards[i].chosen and self.cards[i].num > card.num):
                    self.cards[i].select(num = self.cards[i].num-1)
            
            card.unselect()
            self.chosenCardCount -= 1
        else:
            # Choose
            if(self.chosenCardCount == 3):
                return
            self.chosenCardCount += 1
            card.select(num = self.chosenCardCount)

    def moveScreen(self):
        x,y = pygame.mouse.get_pos()
        diff = x-self.lastMouseX
        self.lastMouseX = x
        self.train.moveX(change = diff)
        self.placeCowboys()
        
    def resizeWindow(self):
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface , (self.width,self.height))
        self.train.resize(self.width,self.height,scale = self.scale)
        for i in range(self.nPlayers):
            self.players[i].resize(self.width,self.height,self.scale)
        
        self.placeCowboys()

        if(self.chooseState):
            for i in range(len(self.cards)):
                self.cards[i].resize(self.width,self.height)
            self.submitButton.resize(self.width,self.height)
        
    def gameInteraction(self,event):
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
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pgvar.K_ESCAPE):
                run = False
            if event.type == pygame.VIDEORESIZE:
                self.width = event.dict['size'][0]
                self.height = event.dict['size'][1]
                self.resizeWindow()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 4):
                    #scroll up
                    self.scale = self.scale + self.scale/10
                    self.resizeWindow()
                if(event.button == 5):
                    #scroll down
                    self.scale = self.scale - self.scale/10
                    self.resizeWindow()
                if(y>= self.height//2 and event.button == 1):
                    self.drag = True
                    self.lastMouseX = x
                if(self.submitButton.ishovering(x,y) and event.button == 1):
                    self.submitButton.press()
            if (event.type == pygame.MOUSEBUTTONUP):
                if(self.drag and event.button == 1):
                    self.drag = False
                elif(self.chooseState and event.button == 1):
                    # We are in chooseState, left button is released
                    # and self.drag == False
                    # Checks whether a card was clicked
                    for i in range(4):
                        chosenCard = None
                        if(self.cards[i].ishovering(x,y)):
                            chosenCard = self.cards[i]
                            break
                    if(chosenCard != None):
                        self.chooseCard(card = chosenCard)
                    elif(self.submitButton.unpress(x,y)):
                        #True if submit button was pressed
                        self.submit()
            if(self.chooseState and self.alive):
                for i in range(4):
                    self.cards[i].checkmousePos(x,y)

            if (self.alive and self.wait == 0):
                self.gameInteraction(event)
            
        return run
    
    def waitLoop(self,waitTicks):
        self.wait = waitTicks
        while(self.wait != 0 and self.run):
            self.run = self.eventChecker()

            if(self.drag):
                self.moveScreen()

            self.train.assertions(self.nPlayers)
            self.drawWindow(wait=True)

            self.msCount +=1
            self.msCount %= 10000
            self.clock.tick(60)
            self.wait -= 1
        return

    def gameloop(self):
        self.run = True
        while(self.run):
            self.run = self.eventChecker()

            if(self.drag):
                self.moveScreen()
            
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
        settings["scale"] = self.scale
        with open("PlayerConf.json","w") as outfile:
            json.dump(settings,outfile,indent=2)

    def run(self):
        self.gameloop()





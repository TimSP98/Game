import pygame
from pygame import locals as pgvar
import sys
from cowboy import Cowboy
from train import Train
from card import Card
from button import Button
from network import Network
import json
import random

class Game():

    def __init__(self,single):
        with open("PlayerConf.json","r") as infile:
            settings = json.load(infile)
        for param,val in settings.items():
            try:
                exec(f"self.{param}={val}")
            except:
                exec(f"self.{param}='{val}'")
        # Assertoins for the game to run
        self.single = single
        if (not single):
            self.netinit()

        else:
            self.nPlayers = 7
            self.id = 1
        assert self.width >= self.height, "Screen not wide enough! Change width in settins.json"
        assert self.nPlayers > 0, "Need at least 1 Player"
        #assert self.nPlayers < 7, "Too many players, I can't count that many"


        # Variable declarations
        self.run = True
        self.players = [] # List of cowboy objects, representing the players
        self.cards = [] # List of card objects, that you can choose from
        self.train = Train(nWagons=self.nPlayers+2,screenW = self.width,screenH = self.height)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE)
        self.msCount = 0
        self.nextAction = None
        pygame.init()
        self.alive = 1
        self.chooseState = 0
        self.points = [0]*self.nPlayers
        self.recieved = False

        self.playerinit()
        self.cardsinit()
        self.buttoninit()

        self.chosenCardCount = 0
        self.actionQ = []
        #[("1","Move"),("3","Turn"),("3","Move"),("4","Turn"),("4","move"),("4","move"),("5","Turn"),("5","move"),("5","move"),("5","move"),("2","Jump"),("2","Jump")]
        self.wait = 0
        self.drag = False

        # Init for displaying text
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS",100)
        self.resizeWindow()
        self.seed = None
        if(not single):
            self.connectinit()
        random.seed(self.seed)
        print("INIT FINSHED")
        self.gameloop()

    def netinit(self):
        setattr(Network,"_gameP",self)
        self.net = Network(self.serverip,self.port)
        self.id = self.net.id
        self.nPlayers = self.net.nPlayers

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
        flip = False
        for i in range(1,self.nPlayers+1):
            if i > (self.nPlayers)//2:
                flip = True
            CB = Cowboy(wagonI = i,flip=flip)
            self.players.append(CB)
        self.placeCowboys()

    def deadLoop(self):
        print("deadloop entered")
        self.net.send(data = str(self.id),dataType=2)
        while(True):
            self.waitRecieve()
            self.chooseState = 0


    def killPlayer(self,player : Cowboy):
        obj = self.players.pop(self.players.index(player))
        self.nPlayers -=1
        if(self.id == obj.playerID):
            # You died
            self.alive = 0
        del obj

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
        self.textsurface = pygame.transform.scale(self.textsurface,(self.width//2,self.width//8))
        self.waitLoop(time)
        del self.textsurface

    def distPoints(self):
        points = random.randint(200,800)
        points = int((points//10)*10)
        i = len(self.train.wagons)-1
        while i >= 0:
            if(len(self.train.wagons[i].amountTop) > 0):
                pointer = self.train.wagons[i].amountTop
                break
            elif(len(self.train.wagons[i].amountBot) > 0):
                pointer = self.train.wagons[i].amountBot
                break
            i -= 1
        playerID = pointer[-1].playerID
        self.points[playerID] += points
        text = f"Player {playerID} recieves {points} points"
        self.displayGameText(text = text,time = 180)      


    def removeWagon(self):
        while(len(self.train.wagons[-1].amountTop) > 0):
            CB = self.train.wagons[-1].amountTop[0]
            CB.die()
        while(len(self.train.wagons[-1].amountBot) > 0):
            CB = self.train.wagons[-1].amountBot[0]
            CB.die()
        wag = self.train.wagons.pop()
        del wag       
        #Assert if only 1 is left afterwards then terminate game then
        # both 1 wagon or 1 player
        if(len(self.train.wagons) == 1 or self.nPlayers < 2):
            print("Wagons Left:",len(self.train.wagons),"Players left:",self.nPlayers)
            #We (might) have a winner
            self.findWinner()

    def findWinner(self):
        if(self.nPlayers == 0):
            winners = []
        elif(self.nPlayers == 1):
            winners = [self.players[0].playerID]
        else:
            self.distPoints()
            winners = [ID for ID, val in enumerate(self.points) if val == max(self.points)]
        self.finish(winners)


    def finish(self,winners):
        #Display winner on the screen forever
        if(len(winners) == 0):
            text = "Everybody died, everybody lost"
        elif (len(winners) == 1):
            text = f"Player {winners[0]} wins the game"
        else:
            text = "We have a tie between: "
            for ID in winners[:-1]:
                text += f"Player {ID}, "
            text += f"and Player {winners[-1]}"
        while True:
            self.displayGameText(text = text,time=1000)

    def playerAction(self,player,action):
        """
        player : int

        action : string
        """
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
        print("actionExec:",len(self.actionQ),self.recieved)
        while(len(self.actionQ) > 0):
            # Loads next action to be done
            nextAction = self.actionQ.pop(0)
            # Displays what the next action is and who does it
            # Displays for 180 ticks (3s)
            player,action = nextAction.split("-")
            player = int(player)
            action = action.lower()
            text = f"Player {player} {action}s"
            self.displayGameText(text = text,time = 180)
            # Performs the action and waits 120 ticks (2s)
            self.playerAction(player = player, action = action)
            self.waitLoop(120)
        #Remove most left wagon
        self.removeWagon()
        # Distribute points to the player most to the left
        self.distPoints()
        self.chooseState = 1

    def submit(self):
        actions = []
        for i in range(len(self.cards)):
            if(self.cards[i].chosen):
                actions.append((self.cards[i].num,f"{self.id}-{self.cards[i].action}"))
        if(len(actions) != 3):
            return
        # Unselect all cards
        for i in range(len(self.cards)):
            if(self.cards[i].chosen):
                self.cards[i].unselect()
        self.chosenCardCount = 0
        
        self.chooseState = 0
        actions.sort()
        actions = [string for _ , string in actions]
        if(not self.single):
            self.net.send(data = actions, dataType = 1)
            self.waitRecieve()

    def connectinit(self):
        while(not self.recieved):
            self.net.recieve()
            self.displayGameText(text = "Waiting for other Players to connect",time = 60)
        self.displayGameText(text = "All players have connected",time = 180)
        self.displayGameText(text = f"You are player {self.id}",time = 180)
        self.nameText = self.myfont.render(f"You are player {self.id}",False,(0,0,0))
        self.nameText = pygame.transform.scale(self.nameText,(self.width//12,self.height//20))
        self.chooseState = 1
        self.recieved = False

    def waitRecieve(self):
        #Wait until answer is recieved
        while(not self.recieved):
            self.net.recieve()
            self.displayGameText(text = "Waiting for other Players",time = 60)
        self.actionExec()
        self.recieved = False
        self.chooseState = 1

    def baseDrawWindow(self):
        self.screen.blit(self.bg_surface,(0,0))
        self.train.animate(self.screen,self.msCount)
        for i in range(len(self.players)):
            self.players[i].animate(self.screen,self.msCount)
    
        try:
            #If variabel exists
            X = self.width//2 - self.textsurface.get_width()//2
            Y = self.height//2 - self.textsurface.get_height()//2
            self.screen.blit(self.textsurface,(X,Y))
        except AttributeError:
            pass
        try:
            X = self.width - int(self.nameText.get_width()*1.05)
            Y = 0
            self.screen.blit(self.nameText,(X,Y))
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
        print("RESIZE CALLED")
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface , (self.width,self.height))
        self.train._resize(self.width,self.height,self.scale)

        for i in range(self.nPlayers):
            self.players[i]._resize(self.width,self.height,self.scale)
        
        self.placeCowboys()
        try:
            c = self.nameText
            self.nameText = self.myfont.render(f"You are player {self.id}",False,(0,0,0))
            self.nameText = pygame.transform.scale(self.nameText,(self.width//12,self.height//20))
        except:
            pass
        if(self.chooseState):
            for i in range(len(self.cards)):
                self.cards[i].resize(self.width,self.height)
            self.submitButton.resize(self.width,self.height)

    
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
        if(not self.run):
            pygame.quit()
            self.close()
        return

    def gameloop(self):
        while(self.run):
            if(not self.alive):
                self.deadLoop()
            self.run = self.eventChecker()

            if(self.drag):
                self.moveScreen()
            
            self.drawWindow()

            self.train.assertions(self.nPlayers)
            
            self.msCount +=1
            self.msCount %= 10000
            self.clock.tick(60)
        
        pygame.quit()
        self.close()

    def close(self):
        with open("PlayerConf.json","r") as infile:
            settings = json.load(infile)
        settings["height"] = self.height
        settings["width"] = self.width
        settings["scale"] = self.scale
        with open("PlayerConf.json","w") as outfile:
            json.dump(settings,outfile,indent=2)
        sys.exit()




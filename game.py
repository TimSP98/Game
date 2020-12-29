import pygame
from pygame import locals as pgvar
from sys import exit
from cowboy import Cowboy
from train import Train
from card import Card
from network import Network
import json


class Game():

    def __init__(self):
        with open("PlayerConf.json","r") as infile:
            settings = json.load(infile)
        for param,val in settings.items():
            try:
                exec("self."+param+"="+str(val))
            except NameError:
                exec("self."+param+"='"+str(val)+"'")
        # Assertoins for the game to run
        self.net = Network(self.serverip,self.port)
        self.id = self.net.id
        self.nPlayers = self.net.nPlayers

        assert self.width >= self.height, "Screen not wide enough! Change width in settins.json"
        assert self.nPlayers > 0, "Need at least 1 Player"
        assert self.nPlayers < 7, "Too many players, I can't count that many"


        self.players = [] # List of cowboy objects, representing the players
        self.cards = [] # List of card objects, that you can choose from
        self.train = Train(nWagons=self.nPlayers+1,screenW = self.width,screenH = self.height)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE)
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface,(self.width,self.height))
        self.msCount = 0
        pygame.init()
        self.alive = 1
        self.playerinit()
        self.cardsinit()


    def cardsinit(self):
        setattr(Card,'_gameP',self)
        setattr(Card,"screenW",self.width)
        setattr(Card,"screenH",self.height)
        for i in range(4):
            self.cards.append(Card("jump"))

    def playerinit(self):
        # Sets some instance variables, unfortunately not class variables
        setattr(Cowboy,'_gameP',self)
        setattr(Cowboy,"_trainP",self.train)
        setattr(Cowboy,"screenW",self.width)
        setattr(Cowboy,"screenH",self.height)

        for i in range(1,self.nPlayers+1):
            CB = Cowboy(wagonI = i,flip=False)
            self.train.wagons[i].amountBot.append(CB)
            self.players.append(CB)

    def killPlayer(self,player : Cowboy):
        obj = self.players.pop(self.players.index(player))
        del obj
        self.alive = 0
        self.nPlayers -=1

    def drawWindow(self):
        self.screen.blit(self.bg_surface,(0,0))
        self.train.idle_animate(self.screen)
        for i in range(len(self.players)):
            self.players[i].idle_animate(self.screen,self.msCount)
        pygame.display.update()

    def resizeWindow(self):
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface , (self.width,self.height))
        self.train.resize(self.width,self.height)
        for i in range(self.nPlayers):
            self.players[i].resize(self.width,self.height)

    def gameInteraction(self,event):
        if event.type == pygame.KEYUP:
            if event.key == pgvar.K_ESCAPE:
                run = False

            if event.key == pgvar.K_j:
                self.players[self.id-1].jump()

            if event.key == pgvar.K_m:
                self.players[self.id-1].move()

            if event.key == pgvar.K_t:
                self.players[self.id-1].turn()
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





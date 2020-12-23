import pygame
from sys import exit
from cowboy import Cowboy
from train import Train
import json


class Game():

    def __init__(self):
        with open("settings.json","r") as infile:
            settings = json.load(infile)
        for param,val in settings.items():
            exec("self."+param+"="+str(val))
        # Assertoins for the game to run
        assert self.width >= self.height, "Screen not wide enough! Change width in settins.json"
        assert self.nPlayers > 0, "Need at least 1 Player"
        assert self.nPlayers < 6, "Too many players, I can't count that many"
        self.players = []
        self.train = Train(nWagons=self.nPlayers,screenW = self.width,screenH = self.height)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.bg_surface = pygame.image.load("./Assets/desert.png").convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface,(self.width,self.height))
        self.msCount = 0
        pygame.init()

        self.playerinit()
        

    def playerinit(self):
        for i in range(self.nPlayers):
            CB = Cowboy(place = self.train.wagons[i].bottom,screenW = self.width,screenH = self.height,flip=False)
            CB.placeRect()
            
            self.players.append(CB)


    def drawWindow(self):
        self.screen.blit(self.bg_surface,(0,0))
        self.train.idle_animate(self.screen)
        for i in range(len(self.players)):
            self.players[i].idle_animate(self.screen,self.msCount)
        pygame.display.update()


    def gameloop(self):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.drawWindow()
            
            self.msCount +=1
            self.msCount %= 10000
            self.clock.tick(60)



    def run(self):
        self.gameloop()



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
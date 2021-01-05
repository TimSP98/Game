import pygame
from wagon import Wagon

class Train():
    assetP = "./Assets/Train/"

    def __init__(self,nWagons,screenW,screenH):
        self.headX = 0
        self.headY = 0
        self.size = 0
        self.head = pygame.image.load(self.assetP+"train.png")
        self.nWagons = nWagons
        self.wagons = [Wagon(col=i%5) for i in range(nWagons)]

        self.resize(screenW,screenH)


    def assertions(self,playersLeft):
        tot = 0
        for i in range(self.nWagons):
            tot += len(self.wagons[i].amountTop)
            tot += len(self.wagons[i].amountBot)
        assert tot == playersLeft, f"There are supposed to be {playersLeft} but I counted {tot} players"
    

    def idle_animate(self,screen):
        #Draws the train head
        screen.blit(self.head,(self.headX,self.headY),(0,0,self.size,int(self.size-self.size*0.3)))
        # Draws all the wagons
        for i in range(len(self.wagons)):
            self.wagons[i].animate(screen)


    def resize(self,screenW,screenH):
        self.head = pygame.image.load(self.assetP+"train.png")
        # Wagon Head
        self.size = screenH//3
        self.head = pygame.transform.scale(self.head,(self.size,self.size))
        self.headY = 2*screenH//3

        # First wagon
        X = int(self.headX+self.size*0.85)
        Y = int(self.headY-self.headY*0.05)
        h = int(self.size-self.size*0.08)
        w = int(self.size + self.size*0.5)
        self.wagons[0].resize(X,Y,w,h)


        #The rest of the wagons
        for i in range(1,self.nWagons):
            X += w*0.82
            self.wagons[i].resize(X,Y,w,h)
        
import pygame
from wagon import Wagon

class Train():
    assetP = "./Assets/Train/"

    def __init__(self,X=0,Y=475,nWagons = 4):
        self.headX = X
        self.headY = Y
        self.head = pygame.image.load(self.assetP+"train.png")
        self.head = pygame.transform.scale(self.head,(125,125))
        self.nWagons = nWagons
        self.wagons = []
        
        # initialize wagons with positions and color
        xd,yd = 100,-10
        for i in range(nWagons):
            X+= xd
            Y += yd
            self.wagons.append(Wagon(X,Y,col=i))
            xd,yd = 160,0

    def idle_animate(self,screen):
        #Draws the train head
        screen.blit(self.head,(self.headX,self.headY),(0,0,125,115))
        # Draws all the wagons
        for i in range(len(self.wagons)):
            self.wagons[i].animate(screen)
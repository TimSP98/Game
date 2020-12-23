import pygame
from wagon import Wagon

class Train():
    assetP = "./Assets/Train/"

    def __init__(self,nWagons,screenW,screenH):
        self.screenW = screenW
        self.screenH = screenH
        self.headX = 0
        self.headY = self.screenH//4
        
        self.head = pygame.image.load(self.assetP+"train.png")
        self.size = self.screenH//2
        self.head = pygame.transform.scale(self.head,(self.size,self.size))
        
        self.nWagons = nWagons
        self.wagons = []
        
        self.wagoninit()



    def wagoninit(self):
        # initialize wagons with positions, color adn size
        X = int(self.headX+self.size*0.85)
        Y = int(self.headY-self.headY*0.05)
        h = int(self.size-self.size*0.08)
        w = int(self.size + self.size*0.5)
        self.wagons.append(Wagon(X,Y,col=0,wWidth=w,wHeight=h))
        for i in range(1,self.nWagons):
            X += w*0.82
            self.wagons.append(Wagon(X,Y,col=i,wWidth=w,wHeight=h))

    

    def idle_animate(self,screen):
        #Draws the train head
        screen.blit(self.head,(self.headX,self.headY),(0,0,self.size,int(self.size-self.size*0.3)))
        # Draws all the wagons
        for i in range(len(self.wagons)):
            self.wagons[i].animate(screen)
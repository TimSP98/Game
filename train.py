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
        self.wagons = [Wagon(col=i) for i in range(nWagons)]

        print(screenW,screenH)
        self.resize(screenW,screenH)
        print("si",self.size)



    

    def idle_animate(self,screen):
        #Draws the train head
        screen.blit(self.head,(self.headX,self.headY),(0,0,self.size,int(self.size-self.size*0.3)))
        # Draws all the wagons
        for i in range(len(self.wagons)):
            self.wagons[i].animate(screen)


    def resize(self,width,height):
        self.head = pygame.image.load(self.assetP+"train.png")
        # Wagon Head
        print(width,height)
        self.size = height//2
        print(self.size)
        self.head = pygame.transform.scale(self.head,(self.size,self.size))
        self.headY = height//2

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
        
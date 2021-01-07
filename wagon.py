import pygame

class Wagon():
    assetP = "./Assets/Train/"
    def __init__(self,col):
        self.X = 0
        self.Y = 0
        self.width = 0
        self.height = 0
        self.col = col
        self.amountBot = [] # list of cowboy objects
        self.amountTop = [] # list of cowboy objects
        self.asset = pygame.image.load(self.assetP+f"sprite_traincars{col}.png")
        self.bottom = self.asset.get_rect()
        self.top = self.asset.get_rect()


    def animate(self,screen):
        screen.blit(self.asset,(self.X,self.Y))
       # pygame.draw.rect(screen,(255,0,0),self.bottom)
        #spygame.draw.rect(screen,(0,255,0),self.top)
        

    def placeCB(self,top):
        """
        top : bool
        - indicates whether the top/bot should be replaced

        returns : None
        """
        
        if(top):
            numCB = len(self.amountTop)
            if(numCB == 0):
                return
            stepSize = self.top.width*1//(numCB+1)
            baseX = self.top.left
            for i in range(numCB):
                self.amountTop[i].place(x=baseX+(i+1)*stepSize,y=self.top.top)
        else:
            numCB = len(self.amountBot)
            if(numCB == 0):
                return
            stepSize = self.bottom.width*1//(numCB+1)
            baseX = self.bottom.left
            for i in range(numCB):
                self.amountBot[i].place(x=baseX+(i+1)*stepSize,y=self.bottom.top)
        
    def moveX(self,change):
        self.X += change
        self.bottom = pygame.Rect.move(self.bottom,change,0)
        self.top = pygame.Rect.move(self.top,change,0)


    def resize(self,X,Y,wagonW,wagonH):
        self.asset = pygame.image.load(self.assetP+f"sprite_traincars{self.col}.png")
        self.X = X
        self.Y = Y
        self.width = wagonW
        self.height =wagonH
        self.asset = pygame.transform.scale(self.asset,(self.width,self.height))

        left , top = self.X+self.width//5 , self.Y + 3.9*self.height//6
        boxW , boxH = self.width-(1.15*self.width//3) , self.height-9*self.height//10
        
        pygame.Rect.update(self.bottom,(left,top) , (boxW,boxH))

        left , top = self.X+self.width//5 , self.Y+int(1.1*self.height//8)
        pygame.Rect.update(self.top,(left,top) , (boxW,boxH))


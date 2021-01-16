import pygame
from baseObject import GameObject 
class Wagon(GameObject):
    assetP = "./Assets/Train/"
    def __init__(self,index):
        self.X = 0
        self.Y = 0
        self.width = 0
        self.height = 0
        self.index = index
        self.amountBot = [] # list of cowboy objects
        self.amountTop = [] # list of cowboy objects
        self.assets = []
        self.assetPaths = [f"./Assets/Train/sprite_traincars{index%5}.png"]



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
            stepSize = self.top.width//(numCB+1)
            baseX = self.top.left
            for i in range(numCB):
                self.amountTop[i].place(x=baseX+(i+1)*stepSize,y=self.top.top)
        else:
            numCB = len(self.amountBot)
            if(numCB == 0):
                return
            stepSize = self.bottom.width//(numCB+1)
            baseX = self.bottom.left
            for i in range(numCB):
                self.amountBot[i].place(x=baseX+(i+1)*stepSize,y=self.bottom.top)
        
    def moveX(self,change):
        self.X += change
        self.bottom = pygame.Rect.move(self.bottom,change,0)
        self.top = pygame.Rect.move(self.top,change,0)

    def _calcSize(self,scale):
        self.height =int(self.screenH*0.25*scale)
        self.width = int(self.screenW*0.22*scale)
        self.X = int(self._trainP.X) + (self.index+1)*self.width
        self.Y = self.screenH-self.height
        self.boxW = self.width-(1.15*self.width//3)
        self.boxH = self.height-9*self.height//10
        
        self.boxLeft = self.X+self.width//5
        self.bottomTop = self.Y + 3.9*self.height//6

        self.topTop = self.Y+int(1.1*self.height//8)

    def animate2(self,screen,msCount):
        #pygame.draw.rect(screen,(255,0,0),self.bottom)
        #pygame.draw.rect(screen,(255,0,0),self.top)
        pass

    def _resize2(self,screenW,screenH,scale=1.0):
        self.top = pygame.Rect((self.boxLeft,self.topTop) , (self.boxW,self.boxH))
        self.bottom = pygame.Rect((self.boxLeft,self.bottomTop) , (self.boxW,self.boxH))
        
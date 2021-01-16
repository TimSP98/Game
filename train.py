import pygame
from wagon import Wagon
from baseObject import GameObject
class Train(GameObject):
    assetP = "./Assets/Train/"

    def __init__(self,nWagons,screenW,screenH):
        setattr(Wagon,"_trainP",self)
        self.headX = 0
        self.headY = 0
        self.size = 0
        self.assetPaths = ["./Assets/Train/train.png"]
        self.assets = []
        self.wagons = [Wagon(index=i) for i in range(nWagons)]

        self._resize(screenW,screenH)


    def assertions(self,playersLeft):
        tot = 0
        for i in range(len(self.wagons)):
            tot += len(self.wagons[i].amountTop)
            tot += len(self.wagons[i].amountBot)
        assert tot == playersLeft, f"There are supposed to be {playersLeft} but I counted {tot} players"
    
    def moveX(self,change):
        """
        change : int
        - Specifies how far to change and direction (+ or -)
        """
        self.headX += change
        for i in range(len(self.wagons)):
            self.wagons[i].moveX(change = change)

    def animate2(self,screen,msCount):
        # Draws all the wagons
        for i in range(len(self.wagons)):
            self.wagons[i].animate(screen,msCount = msCount)

    def _calcSize(self,scale):
        self.width = int(self.screenW*0.2*scale)
        self.height = self.width
        self.X = 0
        self.Y = self.screenH-self.height
    

    def _resize2(self,screenW,screenH,scale = 1.0):
        for i in range(len(self.wagons)):
            self.wagons[i]._resize(self.screenW,screenH,scale = scale)
              
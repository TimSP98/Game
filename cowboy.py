import pygame


class Cowboy():
    assetP = "./Assets/Cowboy/"
    def __init__(self,wagonI: int,flip : bool):
        self.X = 0
        self.Y = 0
        self.wagonI = wagonI
        self.height = 0
        self.width = 0
        self.top = 0
        
        
        self.resize(self.screenW,self.screenH)

        self.right = 1
        if flip:
            self.flip()
            self.right = 0

            
    def idle_animate(self,screen,msCount):
        msCount %= 40
        i = msCount//10
        screen.blit(self.idleNG[i],(self.X,self.Y))


    def flip(self):
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.flip(self.idleNG[i],True,False)
        self.right = abs(self.right-1)
        self.X += 15 if self.right else -15
    
        
    def place(self,x,y):
        """
        x : int
        y : int
        - Coordinate of center of feet
        """
        self.X = x-self.width//2
        self.Y = y-self.height

    def resize(self,screenW,screenH):
        self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_idle_without_gun_{i}.png") for i in range(4)]
        self.height = screenH//8
        self.width = self.height
        
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.scale(self.idleNG[i],(self.width,self.height))
        
        for i in range(len(self._trainP.wagons)):
            self._trainP.wagons[i].placeCB(True)
            self._trainP.wagons[i].placeCB(False)

    def getlsP(self,I = None):
        # Create the correct list pointers depending on which level
        # of the wagon the CB is on
        if (I == None):
            I = self.wagonI
        if(self.top):
            lsP = self._trainP.wagons[I].amountTop
        else:
            lsP = self._trainP.wagons[I].amountBot
        return lsP

    def jump(self):
        # Insert a pointer to self (cowboy object) into the correct list in wagon object
        lsBot = self._trainP.wagons[self.wagonI].amountBot
        lsTop = self._trainP.wagons[self.wagonI].amountTop
        if (self.top):
            lsTop.pop(lsTop.index(self))
            if (self.right):
                lsBot.insert(0,self)
            else:
                lsBot.append(self)
        else:
            lsBot.pop(lsBot.index(self))
            if (self.right):
                lsTop.insert(0,self)
            else:
                lsTop.append(self)
        
        self._trainP.wagons[self.wagonI].placeCB(True)
        self._trainP.wagons[self.wagonI].placeCB(False)

        self.top = abs(self.top - 1)


    def move(self,shot= False,right = True):
        # Checks if shot, to get correct direction of movement
        if(not shot):
            right = self.right
        #gets index of the wagon moving to
        if (right):
            newI = self.wagonI+1
        else:
            newI = self.wagonI-1

        # Checks if you are out of bounds
        if (newI >= len(self._trainP.wagons) or newI < 0):
            self.die() # Dies
            return
        
        # Retrieves ls pointers
        lsCurrent = self.getlsP()
        lsNext = self.getlsP(newI)
        
        # Removes from current
        lsCurrent.pop(lsCurrent.index(self))
        self._trainP.wagons[self.wagonI].placeCB(self.top)

        # Adds to new place
        if(right):
            lsNext.insert(0,self)
        else:
            lsNext.append(self)
        self.wagonI = newI
        self._trainP.wagons[self.wagonI].placeCB(self.top)    

        
    def turn(self):
        self.flip()

    def die(self):
        lsCurrent = self.getlsP()
        lsCurrent.pop(lsCurrent.index(self))
        self._gameP.killPlayer(self)
        

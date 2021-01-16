import pygame
from baseObject import GameObject

class Cowboy(GameObject):
    def __init__(self,wagonI: int,flip : bool):
        self.X = 0
        self.Y = 0
        self.wagonI = wagonI
        self.playerID = wagonI-1
        self.height = 0
        self.width = 0
        self.top = 0
        self.prone = 0
        self.angle = 0
        
        #init for assets
        self.assets = []
        self._resetAP()
        self.scale = 1.0
        self.name = f"Player {self.playerID}"

        # Makes a pointer to self at the place
        # where self is located (initial at the bottom layer)
        self._trainP.wagons[wagonI].amountBot.append(self)
        self.right = 0 if flip else 1 

        self.myfont = pygame.font.SysFont("UBUNTU",100)
        
        self._resize(self.screenW,self.screenH)
 

    def animate2(self,screen,msCount):
        screen.blit(self.assetName,(self.assetNameX,self.assetNameY))
        
    def flip(self):
        for i in range(len(self.assets)):
            self.assets[i] = pygame.transform.flip(self.assets[i],True,False)
        
        self.X += self.width//8 if self.right else -self.width//8
        
    def place(self,x,y):
        """
        x : int
        y : int
        - Coordinate of center of feet
        """
        self.X = x - int(self.width*0.5)
        self.Y = y - self.height
        if(self.prone):
            if((self.right and self.angle == -90) or (not self.right and self.angle == 90) ):
                self.Y += self.height//2
            else:
                self.Y += self.height//10

        self.assetNameX = self.X + int(self.width*0.5) - int(self.assetNameW*0.5)
        self.assetNameY = self.Y -  int(self.assetNameH*0.5)


    def _calcSize(self,scale):
        """
        Calculates the size of the object,
        and stores in class variables
        """
        self.height = int((self.screenH//8)*scale)
        self.width = self.height
        self.assetNameW = int(self.width*1.5)
        self.assetNameH = int(self.height*0.5)  


    def _resize2(self,screenW,screenH,scale = 1.0):
        """
        Extra resizing

        fixes if person if flipped or prone

        Creates the surface for the nameTag
        """
        if(not self.right): self.flip()
        if(self.prone):
            #Flips the surface, to visualize prone
            self.assets = [pygame.transform.rotate(self.assets[0],self.angle)]
        
        assetName = self.myfont.render(self.name,False,(255,0,0))
        self.assetName = pygame.transform.scale(assetName,(self.assetNameW,self.assetNameH))

    def _resetAP(self):
        self.assetPaths = [f"./Assets/Cowboy/Cowboy4_idle_without_gun_{i}.png" for i in range(4)]

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

    def changeProne(self,goProne,right = True):
        """
        goProne : bool
        - Indicates whether self should be prone or not after function call
        right : bool
        -indicates which direction to tilt if goProne = True
        """
        if(goProne):
            # Goes prone
            self.prone = 1
            self.angle = -90 if right else 90
            self.assetPaths = [f"./Assets/Cowboy/Cowboy4_shoot_0.png"]
            self._resize(self.screenW,self.screenH)
            
            self._trainP.wagons[self.wagonI].placeCB(self.top)

        else: 
            # Person straightens up
            self.prone = 0
            self._resetAP()
            self._resize(self.screenW,self.screenH)

            text = f"Player {self.playerID} straightenen up instead"
            self._gameP.displayGameText(text = text, time = 120)

            self._trainP.wagons[self.wagonI].placeCB(self.top)  

    def jump(self):
        # Checks if prone, and straightens if self is prone
        if(self.prone):
            self.changeProne(goProne = False)
            return
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
        # Checks if prone, and straightens if self is prone
        if(self.prone and not shot):
            self.changeProne(goProne = False)
            return
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

        if(shot):
            self.changeProne(goProne=True,right = right)

        # Adds to new place
        if(right):
            lsNext.insert(0,self)
        else:
            lsNext.append(self)
        self.wagonI

        self.wagonI = newI
        self._trainP.wagons[self.wagonI].placeCB(self.top)

    def shoot(self):
        # Checks if prone, and straightens if self is prone
        if(self.prone):
            self.changeProne(goProne = False)
            return
        # Shoot animation
        self.assetPaths = [f"./Assets/Cowboy/Cowboy4_shoot_{i}" for i in range(4)]
        self._gameP.waitLoop(80)
        self.resetAP()

        hit = False # To indicate whether someone was hit
        delta = -1
        if(self.right):
            delta = 1
        # See if someone else at the same place in front of self
        lsCurrent = self.getlsP()
        nextI = lsCurrent.index(self)+delta
        if(nextI >= 0 and nextI < len(lsCurrent)):
                shotPlayer = lsCurrent[nextI]
                hit = True
        if(not hit):
            if(self.top):
                # look for next wagon
                crntWagon = self.wagonI+delta
                while(crntWagon >= 0 and crntWagon < len(self._trainP.wagons)):
                    if(self._trainP.wagons[crntWagon].amountTop):
                        indexToShoot = 0 if self.right else -1
                        shotPlayer = self._trainP.wagons[crntWagon].amountTop[indexToShoot]
                        hit = True
                        break
                    crntWagon += delta
            else: #self.top = False (at bottom) can only shoot 1 wagon away
                crntWagon = self.wagonI+delta
                if(crntWagon >= 0 and crntWagon < len(self._trainP.wagons) and self._trainP.wagons[crntWagon].amountBot):
                    indexToShoot = 0 if self.right else -1
                    shotPlayer = self._trainP.wagons[crntWagon].amountBot[indexToShoot]
                    hit = True
            
        if(not hit):
            #Noone got hit
            text = f"Player {self.playerID} missed (get gud scrub)"
            self._gameP.displayGameText(text = text, time = 180)
        else: # shotPlayer references player that got hit
            shotPlayer.move(shot=True,right = self.right) # Shoots player
        self._gameP.resizeWindow()
        
    def turn(self):
        if(self.prone):
            self.changeProne(goProne = False)
            return
        self.right = abs(self.right-1)
        self.flip()

    def die(self):
        lsCurrent = self.getlsP()
        lsCurrent.pop(lsCurrent.index(self))
        self._gameP.killPlayer(self)
        

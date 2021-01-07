import pygame


class Cowboy():
    assetP = "./Assets/Cowboy/"
    def __init__(self,wagonI: int,flip : bool):
        self.X = 0
        self.Y = 0
        self.wagonI = wagonI
        self.playerID = wagonI
        self.height = 0
        self.width = 0
        self.top = 0
        self.prone = 0
        self.angle = 0
        self.scale = 1.0

        # Makes a pointer to self at the place
        # where self is located (initial at the bottom layer)
        self._trainP.wagons[wagonI].amountBot.append(self)
        self.right = 1

        self.myfont = pygame.font.SysFont("UBUNTU",100)
        

        self.resize(self.screenW,self.screenH,scale = self.scale)
        self.crntAsset = self.idleNG
          
    def animate(self,screen,msCount):
        msCount %= len(self.crntAsset)*20
        i = msCount//20
        screen.blit(self.crntAsset[i],(self.X,self.Y))
        screen.blit(self.nameTag,(self.nameTagX,self.nameTagY))

    def flip(self):
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.flip(self.idleNG[i],True,False)
        for i in range(len(self.shootAsset)):
            self.shootAsset[i] = pygame.transform.flip(self.shootAsset[i],True,False)
        self.X += self.width//8 if self.right else -self.width//8
        
    def place(self,x,y):
        """
        x : int
        y : int
        - Coordinate of center of feet
        """
        self.X = x-self.width//2
        self.Y = y-self.height
        if(self.prone):
            if((self.right and self.angle == -90) or (not self.right and self.angle == 90) ):
                self.Y += self.height//2
            else:
                self.Y += self.height//10

        self.nameTagX = (self.X + self.width//2) - self.nameTag.get_width()//2 
        self.nameTagY = self.Y -  (self.nameTag.get_height()//2)

    def resize(self,screenW,screenH,scale = 1.0):
        self.scale = scale
        if(self.prone):
            self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_shoot_0.png")]
        else:
            self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_idle_without_gun_{i}.png") for i in range(4)]
        self.shootAsset = [pygame.image.load(self.assetP+f"Cowboy4_shoot_{i}.png") for i in range(4)]
        self.height = int((screenH//8)*scale)
        self.width = int(self.height)
        
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.scale(self.idleNG[i],(self.width,self.height))

        if(not self.right):
            self.flip()
        if(self.prone):
            self.idleNG = [pygame.transform.rotate(self.idleNG[0],self.angle)] 
        for i in range(len(self.shootAsset)):
            self.shootAsset[i] = pygame.transform.scale(self.shootAsset[i],(self.width,self.height))

        self.nameTag = self.myfont.render(f"Player {self.playerID}",False,(255,0,0))
        self.nameTag = pygame.transform.scale(self.nameTag,(int(self.width+self.width*0.5),self.height//2))

        self.crntAsset = self.idleNG
    
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
        # Straightens self (upright)
        if(goProne):
            self.prone = 1
            self.angle = -90 if right else 90
            self.resize(self.screenW,self.screenH,scale = self.scale)
            
        else: #person Straightenen up
            self.prone = 0
            self.resize(self.screenW,self.screenH,scale = self.scale)
            self._trainP.wagons[self.wagonI].placeCB(self.top)
            text = f"Player {self.playerID} straightenen themselves up instead"
            self._gameP.displayGameText(text = text, time = 120)

        self.crntAsset = self.idleNG
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
        self.crntAsset = self.shootAsset
        self._gameP.waitLoop(80)
        self.crntAsset = self.idleNG

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
                if(self._trainP.wagons[crntWagon].amountBot):
                    indexToShoot = 0 if self.right else -1
                    shotPlayer = self._trainP.wagons[crntWagon].amountBot[indexToShoot]
                    hit = True
            
        if(not hit):
            #Noone got hit
            text = f"Player {self.playerID} shot but didn't hit anyone (get gud scrub)"
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
        

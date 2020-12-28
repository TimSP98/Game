import pygame


class Cowboy():
    assetP = "./Assets/Cowboy/"
    def __init__(self,wagonI: int,screenW,screenH,flip,trainP):
        self.X = 0
        self.Y = 0
        self.wagonI = wagonI
        self.trainP = trainP
        self.height = 0
        self.width = 0
        self.top = 0
        self.place = self.trainP.wagons[wagonI]
        
        
        self.resize(screenW,screenH)

        self.right = 1
        if flip:
            self.flip()
            self.right = 0

        print(self.right)
            
    def idle_animate(self,screen,msCount):
        msCount %= 40
        i = msCount//10
        screen.blit(self.idleNG[i],(self.X,self.Y))


    def flip(self):
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.flip(self.idleNG[i],True,False)
        self.right = abs(self.right-1)
        self.X += 15 if self.right else -15
    
    def placeRect(self):
        if (self.top):
            self.Y = self.place.top.top
            self.Y -= self.height

            self.X = (self.place.top.left + self.place.top.right)//2
            self.X -= (self.width)//3

        else:
            self.Y = self.place.bottom.top
            self.Y -= self.height

            self.X = (self.place.bottom.left + self.place.bottom.right)//2
            self.X -= (self.width)//3

    def resize(self,screenW,screenH):
        self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_idle_without_gun_{i}.png") for i in range(4)]
        self.height = screenH//6
        self.width = self.height

        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.scale(self.idleNG[i],(self.width,self.height))
        
        self.placeRect()


    def jump(self):
        self.top = abs(self.top - 1)
        self.placeRect()
    
    def decreaseWagonCount(self):
        if self.top:
            self.trainP.wagons[self.wagonI].amountTop -=1
        else:
            self.trainP.wagons[self.wagonI].amountBot -=1
    
    def increaseWagonCount(self):
        if self.top:
            self.trainP.wagons[self.wagonI].amountTop +=1
        else:
            self.trainP.wagons[self.wagonI].amountBot +=1


    def move(self):
        enforceWagonCount()
        if(self.right):
            self.wagonI +=1
        else:
            self.wagonI -= 1
        
        self.place = self.trainP.wagons[self.wagonI]

        self.placeRect()
        
    def turn(self):
        self.flip()
        

        

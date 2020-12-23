import pygame


class Cowboy():
    assetP = "./Assets/Cowboy/"
    def __init__(self,place: pygame.rect,screenW,screenH,flip):
        self.X = 0
        self.Y = 0 
        self.place = place
        self.height = screenH//6
        self.width = int(self.height*0.75)
        self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_idle_without_gun_{i}.png") for i in range(4)]
        
        for i in range(len(self.idleNG)):
            self.idleNG[i] = pygame.transform.scale(self.idleNG[i],(self.width,self.height))

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
    
    def placeRect(self):
        self.Y = self.place.top
        self.Y -= self.height

        self.X = (self.place.left + self.place.right)//2
        self.X -= (self.width)//3


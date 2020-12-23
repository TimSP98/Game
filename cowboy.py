import pygame


class Cowboy():
    assetP = "./Assets/Cowboy/"
    def __init__(self,X,Y,flip):
        self.X = X #180
        self.Y = Y #490
        self.idleNG = [pygame.image.load(self.assetP+f"Cowboy4_idle_without_gun_{i}.png") for i in range(4)]
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


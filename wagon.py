import pygame

class Wagon():
    assetP = "./Assets/Train/"
    def __init__(self,col):
        self.X = 0
        self.Y = 0
        self.width = 0
        self.height = 0
        self.col = col
        self.asset = pygame.image.load(self.assetP+f"sprite_traincars{col}.png")
        self.bottom = self.asset.get_rect()
        


    def animate(self,screen):
        screen.blit(self.asset,(self.X,self.Y))
        pygame.draw.rect(screen,(255,0,0),self.bottom)


    def resize(self,X,Y,wagonW,wagonH):
        self.asset = pygame.image.load(self.assetP+f"sprite_traincars{self.col}.png")
        self.X = X
        self.Y = Y
        self.width = wagonW
        self.height =wagonH
        self.asset = pygame.transform.scale(self.asset,(self.width,self.height))

        top , left = self.X+self.width//5 , self.Y + 3.9*self.height//6
        bottomW , bottomH = self.width-(1.15*self.width//3) , self.height-5*self.height//6

        pygame.Rect.update(self.bottom,(top,left) , (bottomW,bottomH))

        pass
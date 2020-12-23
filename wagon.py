import pygame

class Wagon():
    assetP = "./Assets/Train/"
    def __init__(self,X,Y,col):
        self.X = X
        self.Y = Y
        self.asset = pygame.image.load(self.assetP+f"sprite_traincars{col}.png")
        self.bottom = self.asset.get_rect()
        pygame.Rect.inflate_ip(self.bottom,-self.bottom.size[0]//3,-5*self.bottom.size[1]//6)
        newX = self.X+self.asset.get_size()[0]//6
        newY = self.Y+3.9*self.asset.get_size()[1]//6   
        
        pygame.Rect.move_ip(self.bottom,newX-self.bottom.left,newY-self.bottom.top)


    def animate(self,screen):
        screen.blit(self.asset,(self.X,self.Y))
        pygame.draw.rect(screen,(255,0,0),self.bottom)

import pygame

class Button:

    def __init__(self,action):
        self.action = action
        self.X = 0
        self.Y = 0
        self.myfont = pygame.font.SysFont("Comic Sans MS",100)

        self.resize(self.screenW,self.screenH)

    def resize(self,screenW,screenH):
        self.screenW = screenW
        self.screenH = screenH

        self.width = self.screenH//15
        self.height = self.width//2
        

        self.buttonText = self.myfont.render(self.action,False,(0,0,0))
        self.buttonText = pygame.transform.scale(self.buttonText,(screenH//5,screenH//10))

        self.Rect = self.buttonText.get_rect()
        W = self.Rect.width
        H = self.Rect.height

        self.X = screenW - (W+W*0.5)
        self.Y = H*4
        pygame.Rect.update(self.Rect,(self.X,self.Y),(W,H))

    def animate(self,screen):
        pygame.draw.rect(screen,(178,190,181),self.Rect)
        screen.blit(self.buttonText,(self.X,self.Y))

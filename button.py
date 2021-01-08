import pygame

class Button:
    
    assetP = "./Assets/Buttons/"

    def __init__(self,action):
        self.action = action
        self.X = 0
        self.Y = 0
        self.pressed = False
        self.myfont = pygame.font.SysFont("Comic Sans MS",100)

        self.resize(self.screenW,self.screenH)

    def resize(self,screenW,screenH):
        self.screenW = screenW
        self.screenH = screenH

        self.width = self.screenH//3
        self.height = int(self.width//2.5)
        self.X = 26*screenW//32 #screenW - (self.width+self.width*0.5)
        self.Y = screenH//4

        if(self.pressed):
            self.buttonAsset = pygame.image.load(self.assetP + "submit_down.png")
        else:
            self.buttonAsset = pygame.image.load(self.assetP + "submit_up.png")
        self.buttonAsset = pygame.transform.scale(self.buttonAsset,(self.width,self.height))

    def animate(self,screen):
        screen.blit(self.buttonAsset,(self.X,self.Y))

    def ishovering(self,x,y):
        return (x > self.X and  y > self.Y and x < self.X+self.width and y < self.Y+self.height)

    def press(self):
        if(not self.pressed):
            self.pressed = True
            self.resize(self.screenW,self.screenH)
    
    def unpress(self,x,y):
        if(self.ishovering(x,y) and self.pressed):
            return_val = True
        else:
            return_val = False

        self.pressed = False
        self.resize(self.screenW,self.screenH)
        return return_val
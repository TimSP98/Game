import pygame


class Card:
    cardPath = "./Assets/Card/"
    cowboyPath = "./Assets/Cowboy/"
    def __init__(self,action):
        """ action  : string
            options : Jump, Move, Shoot, Turn """
        self.action = action
        self.X = 0
        self.Y = 0
        self.resize(self.screenW,self.screenH)

    def resize(self,screenW,screenH,scale = 1.0):
        """
        screenW : int
        screenH : int
        scale : int/float

        Resizes the Card to correct size given, screen size and can be scaled up/down
        with the scale parameter.
        """


        self.screenW = screenW
        self.screenH = screenH
        self.cardAsset = pygame.image.load(self.cardPath+"Card2.PNG")
        centerY = screenH//4

        if(self.action == "Jump"):
            self.cowboyAsset =  [pygame.image.load(self.cowboyPath+f"Cowboy4_idle_without_gun_{i}.png") for i in range(1,4)] + \
                                [pygame.image.load(self.cowboyPath+"Cowboy4_jump_without_gun_0.png")]*2 
            centerX = 5*screenW//32
        elif(self.action == "Move"):
            self.cowboyAsset = [pygame.image.load(self.cowboyPath+f"Cowboy4_walk_without_gun_{i}.png") for i in range(0,4)]
            centerX = 11*screenW//32
        elif(self.action == "Shoot"):
            self.cowboyAsset = [pygame.image.load(self.cowboyPath+f"Cowboy4_shoot_{i}.png") for i in range(0,4)]
            centerX = 17*screenW//32
        elif(self.action == "Turn"):
            self.cowboyAsset =  [pygame.image.load(self.cowboyPath+f"Cowboy4_idle_without_gun_{i}.png") for i in range(0,4)] *2
            for i in range(4,8):
                self.cowboyAsset[i] = pygame.transform.flip(self.cowboyAsset[i],True,False)
            centerX = 23*screenW//32

        self.cardW = int((screenW//8)*scale)
        self.cardH = int((self.cardW*1.5)*scale)
        self.cowboyW = int((self.cardW//2.25)*scale)
        self.cowboyH = self.cowboyW
        self.placeCard((centerX,centerY))

        self.cardAsset = pygame.transform.scale(self.cardAsset,(self.cardW,self.cardH))
        for i in range(len(self.cowboyAsset)):
            self.cowboyAsset[i] = pygame.transform.scale(self.cowboyAsset[i],(self.cowboyW,self.cowboyH))


    def placeCard(self,center):
        """
        Center : tuple[int,int]

        returns : None
        """
        x,y = center
        self.X = x-self.cardW//2
        self.Y = y-self.cardH//2


    def checkmousePos(self,x,y):
        """ x and y position of mouse
            if mouse is hovering over card then highlight it"""
        if(x > self.X and  y > self.Y and x < self.X+self.cardW and y < self.Y+self.cardH ):
            #Increases card size by 2%, when mouse is hovering the card
            self.resize(self.screenW,self.screenH,scale = 1.2)
        else:
            self.resize(self.screenW,self.screenH)



    def animate(self,screen,msCount):
        screen.blit(self.cardAsset,(self.X,self.Y))
        msCount %= int(len(self.cowboyAsset)*10)*2
        i = msCount//20
        diffY = 0
        diffX = 0
        if(self.action == "Jump"):
            diffX += self.cardW//20
            #Lifts from the air when jumping
            if(i < 3):
                diffY += self.cowboyH//10
            
        elif(self.action == "Shoot"):
            diffX += self.cardW//20
        elif(self.action == "Turn"):
            diffX -= self.cardW//30
            if(i > 3):
                diffX -= self.cardW//25

            
        cowboyX = self.X + int(self.cardW//2.95)+ diffX
        cowboyY = self.Y + 3*self.cardH//8      + diffY
        
        
        screen.blit(self.cowboyAsset[i],(cowboyX,cowboyY))

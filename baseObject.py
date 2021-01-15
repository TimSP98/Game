import pygame

class GameObject:
    """
    resize()
    """



    def _resize(self,screenW,screenH,scale = 1.0):
        """
        Parameters
        ----------

        assetPath : string
        -   Path to where the assets should be loaded from

        screenW : int
        screenH : int
        -   The dimensions of the screen

        scale : float
        -   Can be changed to increse/decrease overall size of the object


        Returns
        -------
        None
        -   Changes object variables in place 
        """
        #Calculate the size of the object. Is defined in each independent class
        self.screenW = screenW
        self.screenH = screenH
        self._calcSize()

        W = int(self.width*scale)
        H = int(self.height*scale)

        self.assets = []
        for i in range(len(self.assetPaths)):
            surface = pygame.image.load(self.assetPaths[i])
            self.assets.append(pygame.transform.scale(surface,(W,H)))
        
        # For object specific resizing 
        self._resize2(screenW,screenH,scale = scale)

    def _resize2(self):
        pass

        




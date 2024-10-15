import pygame
import pygameInput
pygame.font.init()

class Element():
    elements = []
    mouseRect = None


    def __init__(self,screen,pos,size,label,colour,shape = 1):
        self.pos = pos
        self.shape = shape
        self.size = size
        self.label = label
        self.isPressed = False
        self.colour = colour
        self.SCREEN = screen
        self.font  = pygame.font.SysFont("Arial", 30)
        self.fontColour = (0,0,0)
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        Element.elements.append(self)
        self.OGcolour = colour
        self.over = False


    def displayLabel(self):
        label = self.font.render(self.label, True, self.fontColour)
        xOffset = (self.size[0] - label.get_size()[0])/2
        self.SCREEN.screen.blit(label,(self.pos[0]+xOffset,self.pos[1]+self.size[1]/2-self.font.get_height()/2))
    def createBox(self):
        if self.shape == 1:
            pygame.draw.rect(self.SCREEN.screen,self.colour,self.rect)
        if self.shape == 2:
            pygame.draw.circle(self.SCREEN.screen,self.colour,(self.rect.x+self.rect.width/2,self.rect.y+self.rect.width/2),self.rect.width/2)

    def checkForHover(self):
        if Element.mouseRect.colliderect(self.rect) and not pygame.mouse.get_pressed()[0]:
            self.colour = (self.OGcolour[0]-15,self.OGcolour[1]-15,self.OGcolour[2]-15)
            self.over = True
        else:
            self.colour = self.OGcolour
            self.over = False

    def checkForClick(self):
        if pygame.mouse.get_pressed()[0]:

            if Element.mouseRect.colliderect(self.rect):
                self.colour = (self.OGcolour[0] - 30, self.OGcolour[1] - 30, self.OGcolour[2] - 30)
                self.isPressed = True
            else:
                self.colour = self.OGcolour
                self.isPressed = False


    def update(self):
        self.checkForClick()
        self.checkForHover()
        self.createBox()
        self.displayLabel()


    @staticmethod
    def updateAllElements():
        if len(Element.elements) != 0:
            mousePos = pygame.mouse.get_pos()
            Element.mouseRect = pygame.Rect(mousePos[0],mousePos[1],4,4)

            for element in Element.elements:
                element.update()

class Button(Element):
    def __init__(self, screen,pos, size, label, colour,function,shape = 1,arg = None):
        super().__init__(screen,pos, size, label, colour,shape)
        self.func = function
        self.isRan = False
        self.arg = arg


    def update(self):
        self.checkForClick()
        self.checkForHover()
        self.createBox()
        self.displayLabel()
        if self.isPressed and not self.isRan:
            if self.arg != None:
                self.func(self.arg)
            else:
                self.func()
            self.isRan = True


        if not self.isPressed:
            self.isRan = False


class TextInput(Element):
    def __init__(self,screen, pos, size, label, colour):
        super().__init__(screen,pos, size, label, colour)
        self.defaultLabel = label
        self.label = ""
        self.keyReleased = True
        self.lastKeyPressed = ""
        self.prevKey = ""
        self.keysBeingPressed  = []
        self.allowRemove = True
    def updateLabel(self) :
        if self.isPressed:
            if self.label == self.defaultLabel:self.label = ""
            self.lastKeyPressed = pygameInput.Input.keyPressed()
            if self.keyReleased and len(self.lastKeyPressed) == 1 and self.lastKeyPressed not in self.keysBeingPressed:
                self.label += self.lastKeyPressed
                self.keysBeingPressed.append(self.lastKeyPressed)

            if self.lastKeyPressed == "backspace":
                if self.allowRemove:
                    self.label = self.label[:len(self.label)-1]
                    self.allowRemove = False
                else:
                    self.allowRemove = True
            if pygameInput.Input.getKeyUp("backspace"):
                self.allowRemove = True

            for key in self.keysBeingPressed:
                if pygameInput.Input.getKeyUp(key):
                    self.keysBeingPressed.remove(key)


            self.prevKey = self.lastKeyPressed

        else:
            self.label = self.defaultLabel



    def update(self):
        self.checkForClick()
        self.checkForHover()
        self.createBox()
        self.updateLabel()
        self.displayLabel()

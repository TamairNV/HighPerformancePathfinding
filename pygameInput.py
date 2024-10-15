import pygame


class Input:
    keys = {}
    numberOfKeys = 0
    keysPressed = []
    keysPressedLastFrame = []
    screen = None

    @staticmethod
    def startListening():
        Input.numberOfKeys = len(pygame.key.get_pressed())
        Input.keysPressed = pygame.key.get_pressed()
        Input.keysPressedLastFrame = pygame.key.get_pressed()
        for key in range(Input.numberOfKeys - 1):
            Input.keys[pygame.key.name(key)] = key

    @staticmethod
    def isKeyPressed(key, pressed=None):
        if pressed == None:
            return Input.keysPressed[Input.keys[key]]
        return pressed[Input.keys[key]]

    @staticmethod
    def keyPressed():

        for key in range(Input.numberOfKeys - 1):
            if pygame.key.get_pressed()[key]:
                return pygame.key.name(key)
        return ""

    @staticmethod
    def getKeyDown(key):
        for event in Input.screen.events:
            if event.type == pygame.KEYDOWN and Input.isKeyPressed(key):
                return True
        return False

    @staticmethod
    def getKeyUp(key):
        for event in Input.screen.events:
            if event.type == pygame.KEYUP and Input.isKeyPressed(key, Input.keysPressedLastFrame):
                return True
        return False

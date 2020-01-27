import pygame
from math import atan2, degrees

class Question:
    # Stores blocks to create a question, can be saved to a file, could add cloud storage
    def __init__(self):
        self.blocks = []

    def interact(self,event):
        for i in self._blocks:
            i.interact(event)

    def save(self,file):
        pass

    def load(self,file):
        pass

class Block:
    # coords, interface with other blocks and the question as a whole
    def __init__(self,screen,position):
        self.screen = screen
        self.position = position
        self._x = position[0]
        self._y = position[1]
        self.colour = colour["BLACK"]

class Vector(Block):
    # Need arrow, input box, connection to a particle
    #pygame.transform.rotate
    # what ill do is if they click a certain button then the bottom of the arrow is locked in place
    # it tracks the mouse and takes the angle of the mouse from that point and then does a transform
    def __init__(self,position):
        super().__init__(position)
        self.active = False
        self.rotate = False
        self.rotateAngle = 0
        self.name = 'temp'
        self.text = TextInput(self.app, self.position, (50, 50),
                                       colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                       alphaHigh=100, textSize=16
                                       )

        # Sprite setup
        self.arrow = pygame.image.load('arrow.svg').convert_alpha()

    def render(self):
        self.screen.blit(self.arrow,self.position)

    def interact(self,event):
        if self.active: # Group active
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.rotate = not self.rotate
                self.root = mouse
            if self.rotate:# Nice to use my angle function from before
                self.rotateAngle = degrees(atan2(self.root[1] - mouse[1], self.root[0] - mouse[0] ))
                self.arrow = pygame.transform.rotate(self.arrow,self.rotateAngle)
            textInput = self.text.interact(event)
            if textInput != None:
                self.input = textInput
            self.render()

class Force(Vector):
    # Newtons, red colour, relates to calculations.py force object
    def __init__(self,position):
        super().__init__(position)
        self.colour = colour["RED"]

class Velocity(Vector):
    # m/s, blue colour, relates to calculations.py velocity object
    def __init__(self,position):
        super().__init__(position)
        self.colour = colour["BLUE"]

class Acceleration(Vector):
    # m/s/s, green colour, relates to calculations.py acceleration object
    def __init__(self, position):
        super().__init__(position)
        self.colour = colour["GREEN"]

class Particle(Block):
    # store and create (vectors,mass,coeff), relates to calculations.py particle object
    def __init__(self,position):
        super().__init__(position)
        self.circle = (self.position,10)# Center, radius

    def render(self,screen):
        pygame.draw.cicle(screen,self.colour,self.circle[0],self.circle[1])

class Plane(Block):
    # Incline, friction, relates to calculations.py plane object
    def __init__(self, position, rough = False, angle = 0):
        super().__init__(position)


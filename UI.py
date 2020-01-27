"""
This section of code controls the
user interface of the mechanics modeller.
"""
from pygame.locals import *
from fractions import Fraction
from sidebars import *
#from math import atan2, degrees

class App:
    """
    The App class is the backbone of the user interface
    where the pygame module is initialised and setup,
    as well as containg the main program loop.
    """

    def __init__(self):
        # Initialises pygame module
        pygame.init()
        self.programExit = False

        # Gathers system info
        systemInfo = pygame.display.Info()
        self.rect = pygame.Rect(0,0,systemInfo.current_w,systemInfo.current_h)
        self.width = self.rect.w
        self.height = self.rect.h
        self.aspectRatio = Fraction(self.width, self.height)

        # Display creation
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        pygame.display.set_caption("Mechanics Modeller")
        icon = pygame.image.load("jubble.jpg")
        pygame.display.set_icon(icon)

        # Initial image setup
        self.grid = pygame.image.load("grid.png")
        self.grid = pygame.transform.scale(self.grid, (self.width, self.width))

        # Framerate
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Objects setup
        self._objects = {}
        self.objects = (Slope(self), Toolbar(self), Walkthrough(self), ForcesOnParticle(self))

    # Main program loop that controls each frame
    def programLoop(self):
        while not self.programExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    quit()
                # Reset screen and render objects
                self.screenReset()
                self.interact(event)

            pygame.display.update()
            self.clock.tick(self.FPS)

    def interact(self, event):
        for name, obj in self.objects.items():
            obj.interact(event)

    def screenReset(self):
        self.screen.fill(colour['WHITE'])
        self.screen.blit(self.grid, (0, 0))

    @property
    def objects(self):
        return self._objects

    @objects.getter
    def objects(self, name=None):
        if name == None:
            return self._objects
        else:
            return self._objects[name]

    @objects.setter
    def objects(self, listOfObjects):
        for i in listOfObjects:
            self._objects[i.name] = i

class Slope:
    """
    Some questions require an inclined plane and this class
    draws and manages the user interaction with a slope.
    """

    def __init__(self, app):
        # Paramater initialisation
        self.app = app

        # Slope attributes
        self.name = 'slope'
        self.active = False

        # Calculations related values
        self.angle = None

        # Rendering related values
        self.thick = 10  # Thickness of the line
        self.rect = pygame.Rect(500, 300, 800, 400)  # Coords and dimensions of the object
        self.lines = ((self.rect.bottomleft, self.rect.topright),
                      (self.rect.bottomleft, self.rect.bottomright),
                      (self.rect.topright, self.rect.bottomright)
                      )
        # Object Storage
        self.angleInputBox = TextInput(self.app, (self.rect.x * 1.24, self.rect.bottomleft[1] * 0.92), (50, 50),
                                       colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                       alphaHigh=100, textSize=16
                                       )

    def render(self):
        renderLines(self.app.screen, colour['BLACK'], self.lines, self.thick)

    def interact(self, event):
        if self.active:
            self.render()
            self.angleInputBox.interact(event)

class ForcesOnParticle:
    def __init__(self,app):
        # Paramater initialisation
        self.app = app

        # Slope attributes
        self.name = 'resolve'
        self.active = False

        # Calculations related values
        self.buttons = []
        self.forces = {}

        # Rendering related values
        self.thick = 10  # Thickness of the line
        self.rect = pygame.Rect(self.app.rect.centerx, self.app.rect.centery, 100, 100)  # Coords and dimensions of the object
        # Object Storage
        self.buttons.append(TextInput(self.app, (self.rect.centerx,self.rect.y-50), (50, 50),
                                       colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                       alphaHigh=100, textSize=16
                                       ))
        self.buttons.append(TextInput(self.app, (self.rect.centerx,self.rect.bottom+50), (50, 50),
                                colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                alphaHigh=100, textSize=16
                                ))
        self.buttons.append(TextInput(self.app, (self.rect.x-50,self.rect.centery), (50, 50),
                                colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                alphaHigh=100, textSize=16
                                ))
        self.buttons.append(TextInput(self.app, (self.rect.right+50,self.rect.centery), (50, 50),
                                colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                alphaHigh=100, textSize=16
                                ))

    def interact(self, event):
        if self.active:
            f1 = Force(self.app,(800,400))
            f1.interact(event)
            for i in self.buttons:
                textInput = i.interact(event)
                if textInput != None:
                    self.forces[i] = textInput

app = App()
app.programLoop()
"""
1. Vector part
2. Force part
3. Velocity part
4. Acceleration part
5. Particle part
6. Plane part
7. Inclined plane part
8. Rough plane part
9. Group parts together
10. Presets
11. Make each class self reliant, e.g. def interact(event), def render(screen), remove self.app
"""
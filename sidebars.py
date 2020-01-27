from pygameMethods import *

class Sidebar:
    """
    The two sidebars are the toolbar tab and the walk through tab. As their rendering is very similar,
    they share a parent class.
    """

    def __init__(self, app,sidebar):
        # Paramater initialisation
        self.app = app

        # UI assembly
        if isinstance(sidebar, Toolbar):
            builder = ToolbarUIBuilder(sidebar)
            self.build = True
        else:
            builder = WalkthroughUIBuilder(sidebar)
        builder.build()
        del builder

    def render(self):
        self.app.screen.blit(self.surface, self.coords)
        pygame.draw.rect(self.app.screen, self.panelColour, self.panel)
        self.panelText.render()

class Walkthrough(Sidebar):
    """
    The walk through is used as a guide to show students each step of the calculations.
    This is necessary if the user can not work out how the program came to the answer.
    """
    def __init__(self, app):
        self.name = 'walkthrough'
        self.active = False
        super().__init__(app,self)

    def interact(self, event):
        if self.active:
            self.render()
            for i in self.buttons:
                i.interact(event)
            renderLines(self.app.screen, self.colour, self.border, 2)
        else:
            self.max.interact(event)
        self.run.interact(event)

class Toolbar(Sidebar):
    """
    The toolbar is displayed on the left hand side of the screen
    and is used to access different components of questions as well
    as to access the settings.
    The toolbar can be minimized to allow a teacher to better show
    the class the question.
    """

    def __init__(self, app):
        self.state = 0
        self.name = 'toolbar'
        self.active = True
        super().__init__(app,self)

    def interact(self, event):
        if self.active:
            self.render()

            # Creates all buttons
            for i in self.buttons:
                i.interact(event)
            for i in self.states[int(self.state)]:
                i.interact(event)

            #Border lines are rendered on top of buttons
            renderLines(self.app.screen, colour['BLACK'], self.border, 2)
        else:
            # Creates maximize button if toolbar is minimized
            self.max.interact(event)

class ToolbarUIBuilder:
    """
    Encapsulates the assembly of the toolbar class' UI elements.
    """
    text = [["Presets","Particle","Force","Plane"],["Inclined Plane","Forces on a particle"],["Force"],["Horizontal Plane","Inclined Plane","Vertical Plane"]]
    command = [["state1", "state0 ", "temp", "state3"],["slope","resolve"],["state0"],["state0","state0","state0"]]
    def __init__(self,toolbar):
        self.toolbar = toolbar
        self.app = toolbar.app
        self._amountStates = len(self.text)
        self.rect = pygame.Rect(0, 0, self.app.width * 0.25, self.app.height)
        self.toolbar.coords = self.rect.topleft
        self.colour = colour["GREY"]
        self.toolbar.panelColour = colour["WHITE"]

    def getHeight(self,buttons):
        heights = []
        self.buttonSize = 150 #(self.app.height - 100) // buttons
        for i in range (buttons):
            heights.append(52+(self.buttonSize*i))
        return heights

    def stateBuilder(self):
        _states = [list() for i in range(self._amountStates)]
        for state in range(len(_states)):
            heights = self.getHeight(len(self.text[state]))
            for i in range(len(heights)):
                _states[state].append(Button(self.app,(0,heights[i]),(self.rect.w,self.buttonSize),
                                                       self.command[state][i],self.text[state][i],25,
                                                       self.colour,0,self.colour,100,False
                                                       ))
        return _states

    def imageBuilder(self):
        self.toolbar.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.toolbar.surface.set_alpha(150)
        self.toolbar.surface.fill(self.colour)
        self.panel = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 50)
        self.toolbar.panel = self.panel
        self.toolbar.panelText = Text(self.app, self.panel.centerx, self.panel.centery, "Tools", 40)
        self.toolbar.border = (self.rect,self.panel)

    def buttonBuilder(self):
        buttons = []
        buttons.append(Button(self.app, (self.panel.w - 80, 0), (80, self.panel.h), 'toolbar',
                              "X", 25, colour["WHITE"], 0, colour["RED"], 255, False))
        buttons.append(Button(self.app, self.panel.topleft, (self.panel.h, self.panel.h), 'state0',
                              "↵",40, colour["WHITE"], highlight=colour['LIGHTGREY'], border=False))
        self.toolbar.max = Button(self.app, (0, 0), (40, 60), 'toolbar',
                                  ">>", 25, colour["GREY"], 255, colour["GREEN"])

        return buttons

    def build(self):
        self.imageBuilder()
        self.toolbar.buttons = self.buttonBuilder()
        self.toolbar.states = self.stateBuilder()

class WalkthroughUIBuilder:
    """
    Encapsulates the assembly of the Walkthrough class' UI elements
    """
    def __init__(self,walkthrough):
        self.walk = walkthrough
        self.app = self.walk.app
        self.rect = pygame.Rect(self.app.width*0.75,0,self.app.width*0.25,self.app.height)
        self.walk.coords = self.rect.topleft
        self.walk.panelColour = colour["LIGHTGREY"]
        self.walk.colour = colour["DARKGREY"]

    def imageBuilder(self):
        self.walk.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.walk.surface.fill(colour["DARKGREY"])
        self.panel = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 50)
        self.walk.panel = self.panel
        self.walk.panelText = Text(self.app, self.panel.centerx, self.panel.centery, "Walk through", 40)
        self.walk.border = (self.panel,self.rect)

    def buttonBuilder(self):
        buttons = []
        buttons.append(Button(self.app, self.panel.topleft, (80, self.panel.h), 'walkthrough',
                             "X", 25, colour["WHITE"], 0, colour["RED"], 255, False))
        self.walk.max = Button(self.app, (self.app.width - 40, 0), (40, 60), 'walkthrough',
                          "<<", 25, colour["GREY"], 255, colour["GREEN"])
        self.walk.run = Button(self.app, (self.app.rect.centerx - 100, 0), (100, 50),
                          run, 'Run', 30, colour["GREEN"], highlight=colour["GREEN2"])

        return buttons

    def build(self):
        self.imageBuilder()
        self.walk.buttons = self.buttonBuilder()
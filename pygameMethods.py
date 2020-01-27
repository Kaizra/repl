from colours import *
from GlobalFunctions import *

class Force:
    def __init__(self,app,coords,direction = 'N'):
        self.app = app
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.direction = direction
        self.active = True
        self.textInput = TextInput(self.app, coords, (50, 50),
                                colour=colour["LIGHTGREY"], alpha=50, highlight=colour["LIGHTGREY"],
                                alphaHigh=100, textSize=16
                                )
        if direction == 'N':
            self.arrow = ((self.coords,(self.x,self.y-50)),
                         ((self.x,self.y-50),(self.x+10,self.y-50+10)),
                         (((self.x,self.y-50),(self.x-10,self.y-50+10)))
                         )
    def render(self):
        renderLines(self.app.screen,colour["BLACK"],self.arrow,10)

    def interact(self,event):
        if self.active:
            self.render()
            self.textInput.interact(event)
class Text:
    """
    A simple class that can render text to the screen
    """

    def __init__(self, app, x, y, text, size=None):
        if size == None:
            self.size = 100
        else:
            self.size = size
        self.colour = colour["BLACK"]
        self._msg = text
        self.app = app
        self.font = 'segoeuiemoji'
        self.font = pygame.font.SysFont(self.font, self.size)
        self.surface = self.font.render(self._msg, True, self.colour)
        self.border = self.surface.get_rect()
        self.border.center = (x, y)

    def render(self):
        self.app.screen.blit(self.surface, self.border)

    @property
    def message(self):
        return self._msg

    @message.setter
    def message(self, msg):
        self._msg = msg
        self.surface = self.font.render(self._msg, True, colour["BLACK"])


class Button:
    """
    This class creates a button that changes colour when the cursor is
    hovered over it and on click it can run a function.
    """

    def __init__(self,
                 app,
                 coords,
                 dimensions,
                 action=None,
                 text='',
                 textSize=25,
                 colour=colour["GREY"],
                 alpha=255,
                 highlight=colour["WHITE"],
                 alphaHigh=255,
                 border=True
                 ):
        # Paramater initialisation
        self.app = app
        self.rect = pygame.Rect(coords[0], coords[1], dimensions[0], dimensions[1])
        self.action = action
        self.text = Text(self.app, self.rect.centerx, self.rect.centery, text, textSize)
        self.colour = colour
        self.alpha = alpha
        self.highlight = highlight
        self.alphaHigh = alphaHigh
        self.border = border

        # Button attributes
        self.active = False

        # Rendering related values
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.lines = ((self.rect.topleft, self.rect.topright),(self.rect.topleft, self.rect.bottomleft),
                      (self.rect.bottomleft, self.rect.bottomright),(self.rect.bottomright, self.rect.topright)
                      )

    def render(self, colour1=None, alpha=None):
        if colour1 == None:
            colour1 = self.colour
        if alpha == None:
            alpha = self.alpha
        if alpha != None:
            self.surface.set_alpha(alpha)
        if colour1 != None:
            self.surface.fill(colour1)
            self.app.screen.blit(self.surface, (self.rect.x, self.rect.y))
        self.text.render()
        if self.border:
            renderLines(self.app.screen, colour["BLACK"], self.lines, 2)

    def interact(self, event):
        self.mouse = pygame.mouse.get_pos()
        self.render(self.colour, self.alpha)
        if self.rect.collidepoint(self.mouse):
            self.render(self.highlight, self.alphaHigh)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = not self.active
                if self.action != None:
                    if isinstance(self.action, str):  # Activating object
                        if self.action[:5] == 'state':
                            self.app.objects['toolbar'].state = self.action[5::]
                        else:
                            self.app.objects[self.action].active = not self.app.objects[self.action].active
                    elif self.action != None:
                        self.action(self.app)

class TextInput(Button):
    """
    Creates a text box that when clicked the user can type inside it
    and the text is rendered to the screen.
    """

    def __init__(self,
                 app,
                 coords,
                 dimensions,
                 action=None,
                 text=None,
                 textSize=None,
                 colour=None,
                 alpha=255,
                 highlight=None,
                 alphaHigh=255,
                 border=True
                 ):
        super().__init__(app,
                         coords,
                         dimensions,
                         action,
                         text,
                         textSize,
                         colour,
                         alpha,
                         highlight,
                         alphaHigh
                         )
        # Text input attributes
        self.input = ''
        self.textInput = Text(app, self.rect.midleft[0] + 10, self.rect.midleft[1], self.input, textSize)
        self.repeat = 0

    def render(self, colour1, alpha):
        super().render(colour1, alpha)
        self.textInput.render()
        if self.border:
            renderLines(self.app.screen, colour["BLACK"], (
                (self.rect.topleft, self.rect.bottomleft),
                (self.rect.topleft, self.rect.topright),
                (self.rect.topright, self.rect.bottomright),
                (self.rect.bottomright, self.rect.bottomleft)
            ), 3)

    def interact(self, event):
        self.render(self.colour, self.alpha)
        super().interact(event)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                    self.repeat += 1
                    # backspace = True
                    # while backspace:
                    #    pygame.key.get_pressed()

                elif event.key == pygame.K_RETURN:
                    self.active = False
                    return self.input
                else:
                    self.input += event.unicode
                self.textInput.message = self.input
                self.textInput.render()

################
#class newTextBox(pygame.sprite.Sprite):
#    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
#        pygame.sprite.Sprite.__init__(self)
#        self.text = ""
#        self.width = width
#        self.initialText = text
#        self.case = case
#        self.maxLength = maxLength
#        self.boxSize = int(fontSize * 1.7)
#        self.image = pygame.Surface((width, self.boxSize))
#        self.image.fill((255, 255, 255))
#        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
#        self.rect = self.image.get_rect()
#        self.fontFace = pygame.font.match_font("Arial")
#        self.fontColour = pygame.Color("black")
#        self.initialColour = (180, 180, 180)
#        self.font = pygame.font.Font(self.fontFace, fontSize)
#        self.rect.topleft = [xpos, ypos]
#        newSurface = self.font.render(self.initialText, True, self.initialColour)
#        self.image.blit(newSurface, [10, 5])
#
#    def update(self, keyevent):
#        key = keyevent.key
#        unicode = keyevent.unicode
#        if key > 31 and key < 127 and (
#                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
#            if keyevent.mod in (1, 2) and self.case == 1 and key >= 97 and key <= 122:
#                # force lowercase letters
#                self.text += chr(key)
#            elif keyevent.mod == 0 and self.case == 2 and key >= 97 and key <= 122:
#                self.text += chr(key - 32)
#            else:
#                # use the unicode char
#                self.text += unicode
#
#        elif key == 8:
#            # backspace. repeat until clear
#            keys = pygame.key.get_pressed()
#            nexttime = pygame.time.get_ticks() + 200
#            deleting = True
#            while deleting:
#                keys = pygame.key.get_pressed()
#                if keys[pygame.K_BACKSPACE]:
#                    thistime = pygame.time.get_ticks()
#                    if thistime > nexttime:
#                        self.text = self.text[0:len(self.text) - 1]
#                        self.image.fill((255, 255, 255))
#                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
#                        newSurface = self.font.render(self.text, True, self.fontColour)
#                        self.image.blit(newSurface, [10, 5])
#                        updateDisplay()
#                        nexttime = thistime + 50
#                        pygame.event.clear()
#                else:
#                    deleting = False
#
#        self.image.fill((255, 255, 255))
#        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
#        newSurface = self.font.render(self.text, True, self.fontColour)
#        self.image.blit(newSurface, [10, 5])
#        if screenRefresh:
#            updateDisplay()
#
#    def move(self, xpos, ypos, centre=False):
#        if centre:
#            self.rect.topleft = [xpos, ypos]
#        else:
#            self.rect.center = [xpos, ypos]
#
#    def clear(self):
#        self.image.fill((255, 255, 255))
#        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
#        newSurface = self.font.render(self.initialText, True, self.initialColour)
#        self.image.blit(newSurface, [10, 5])
#        if screenRefresh:
#            updateDisplay()
#
#def textBoxInput(textbox, functionToCall=None, args=[]):
#    # starts grabbing key inputs, putting into textbox until enter pressed
#    global keydict
#    textbox.text = ""
#    returnVal = None
#    while True:
#        updateDisplay()#draws and displays everything
#        if functionToCall:
#            returnVal = functionToCall(*args)
#        for event in pygame.event.get():
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_RETURN:
#                    textbox.clear()
#                    if returnVal:
#                        return textbox.text, returnVal
#                    else:
#                        return textbox.text
#                elif event.key == pygame.K_ESCAPE:
#                    pygame.quit()
#                    sys.exit()
#                else:
#                    textbox.update(event)
#            elif event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#
#
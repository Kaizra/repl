import pygame
# Global functions
def renderLines(screen, colour, coords, thickness=None):
    if thickness == None:
        thickness = 10
    if isinstance(coords,pygame.Rect):
        lines = ((coords.topleft, coords.topright),
                (coords.topleft, coords.bottomleft),
                (coords.topright, coords.bottomright),
                (coords.bottomright, coords.bottomleft)
                )
        renderLines(screen,colour,lines,thickness)
    elif isinstance(coords[0],pygame.Rect):
        for i in coords:
            lines = ((i.topleft, i.topright),
                     (i.topleft, i.bottomleft),
                     (i.topright, i.bottomright),
                     (i.bottomright, i.bottomleft)
                     )
            renderLines(screen, colour, lines, thickness)
    else:
        for i in coords:
            pygame.draw.line(screen, colour, i[0], i[1], thickness)

def run(app):
    app.objects["walkthrough"].active = True

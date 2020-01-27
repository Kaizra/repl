"""
Global colour definitions, I have implemented a dark and light mode just for fun.
"""
colourScheme = True
if colourScheme:
    colour = {'WHITE': (255, 255, 255),
              'BLACK': (0, 0, 0),
              'GREY': (211, 211, 211),
              'LIGHTGREY': (230, 230, 230),
              'DARKGREY': (111,111,111),
              'RED': (255, 0, 0),
              'GREEN': (0, 255, 0),
              'GREEN2': (15, 200, 15),
              'BLUE': (0, 0, 255)
              }
else:
    colour = {'WHITE': (0, 0, 0),
              'BLACK': (255, 255, 255),
              'GREY': (111, 111, 111),
              'LIGHTGREY': (100, 100, 100),
              'DARKGREY': (200, 200, 200),
              'RED': (255, 0, 0),
              'GREEN': (0, 150, 0),
              'GREEN2': (15, 200, 15),
              'BLUE': (0, 0, 255)
              }

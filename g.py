import pygame as pg

# Declare some constants and variables
FPS = 45
WHITE = pg.Color("#DDDDDD")
BLACK = pg.Color("#1A1A1A")
GREY = pg.Color("#333333")
ORANGE = pg.Color("#FF6600")
RED = pg.Color("#FF1F00")
FRAME_GAP = 160
LINE_WIDTH = 10
CIRCLE_RADIUS = 50
CIRCLE_WIDTH = 10
CROSS_LENGTH = 54
CROSS_WIDTH = 14


def init():
    global WIN, WIDTH, HEIGHT
    WIN = pg.display.get_surface()
    WIDTH, HEIGHT = WIN.get_size()

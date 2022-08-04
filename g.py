import pygame as pg

# Declare some constants and variables
FPS = 45
WHITE = pg.Color("#F1F1F1")
BLACK = pg.Color("#101010")
ORANGE = pg.Color("#FF6600")
RED = pg.Color("#FF1F00")
FRAME_GAP = 160
LINE_WIDTH = 10
CIRCLE_WIDTH = 10
CROSS_WIDTH = 12
CIRCLE_RADIUS = 50
CROSS_LENGTH = 54


def init():
    global WIN, WIDTH, HEIGHT
    WIN = pg.display.get_surface()
    WIDTH, HEIGHT = WIN.get_size()

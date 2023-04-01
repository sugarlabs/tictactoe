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
# Declare variables for keeping score
player_1_score = 0
player_2_score = 0

# Initialize Pygame
pg.init()

# Create the window
WINDOW_SIZE = (800, 800)
WIN = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Tic Tac Toe")

# Define the fonts
FONT_BIG = pg.font.SysFont(None, 80)
FONT_MED = pg.font.SysFont(None, 50)

# Define the sounds
SOUND_CLICK = pg.mixer.Sound("click.wav")
SOUND_WIN = pg.mixer.Sound("win.wav")
SOUND_TIE = pg.mixer.Sound("tie.wav")

def init():
    global WIN, WIDTH, HEIGHT
    WIN = pg.display.get_surface()
    WIDTH, HEIGHT = WIN.get_size()
def draw_board():
    # Draw the board
    WIN.fill(BLACK)
    pg.draw.line(WIN, WHITE, (FRAME_GAP, 0), (FRAME_GAP, HEIGHT), LINE_WIDTH)
    pg.draw.line(WIN, WHITE, (2 * FRAME_GAP, 0), (2 * FRAME_GAP, HEIGHT), LINE_WIDTH)
    pg.draw.line(WIN, WHITE, (0, FRAME_GAP), (WIDTH, FRAME_GAP), LINE_WIDTH)
    pg.draw.line(WIN, WHITE, (0, 2 * FRAME_GAP), (WIDTH, 2 * FRAME_GAP), LINE_WIDTH)

def draw_circle(pos):
    # Draw a circle at the given position
    x, y = pos
    pg.draw.circle(WIN, ORANGE, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)
    SOUND_CLICK.play()

def draw_cross(pos):
    # Draw a cross at the given position
    x, y = pos
    pg.draw.line(WIN, RED, (x - CROSS_LENGTH // 2, y - CROSS_LENGTH // 2),
                 (x + CROSS_LENGTH // 2, y + CROSS_LENGTH // 2), CROSS_WIDTH)
    pg.draw.line(WIN, RED, (x + CROSS_LENGTH // 2, y - CROSS_LENGTH // 2),
                 (x - CROSS_LENGTH // 2, y + CROSS_LENGTH // 2), CROSS_WIDTH)
    SOUND_CLICK.play()

def get_mouse_pos():
    # Get the position of the mouse cursor
    pos = pg.mouse.get_pos()
    x, y = pos
    # Round the position to the nearest frame gap
    x = round(x / FRAME_GAP) * FRAME_GAP
    y = round(y / FRAME_GAP) * FRAME_GAP
    return x, y

def get_board_pos(pos):
    # Get the row and column of the given position on the board
    row = pos[1] // FRAME_GAP
    col = pos[0] // FRAME_GAP
    return row, col

def get_board_state(board):
    # Get the current state of the board
    state = ""
    for row in board:
        for val in row:
            state += str(val)
    return state

def check_win(board, player):
    # Check if the given player has won the game
    for i in range(3):
        # Check the rows
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True



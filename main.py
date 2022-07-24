from asyncio import constants
import pygame as pg
from constants import *
from frame import Frame
import sys

# The main controller
class Main:
    def __init__(self):
        pg.init()

        # self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.canvas = None


    def set_canvas(self, canvas):
        self.canvas = canvas
        pg.display.set_caption("Tic-Tac-Toe")

    def write_file(self, file_path):
        pass

    def read_file(self, file_path):
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
            if event.type == pg.MOUSEBUTTONUP:
                if self.canvas is None:
                    self.canvas.grab_focus()
                self.frame.detect_click(pg.mouse.get_pos())

    def draw(self):
        WIN.fill(BLACK)
        self.frame.draw()
        pg.display.update()

    def reset(self):
        self.frame = Frame(self)

    # The main loop
    def run(self):
        init()
        self.frame = Frame(self)
        self.clock = pg.time.Clock()
        while self.running:
            self.check_events()
            print(WIN)
            # if self.win is None:
            #     self.win = pg.display.get_surface()
            # else:
            #     self.draw()
            self.clock.tick(FPS)
        pg.display.quit()
        pg.quit()
        sys.exit(0)


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main()
    main.run()

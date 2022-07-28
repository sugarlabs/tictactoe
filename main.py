import pygame as pg
import g
from frame import Frame
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# The main controller
class Main:
    def __init__(self, journal=True):
        self.journal = journal
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
                if self.canvas is not None:
                    self.canvas.grab_focus()
                self.frame.detect_click(pg.mouse.get_pos())

    def draw(self):
        g.WIN.fill(g.BLACK)
        self.frame.draw()
        pg.display.update()

    def reset(self):
        self.frame = Frame(self, (g.WIDTH/2, g.HEIGHT/2))

    # The main loop
    def run(self):
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
        g.init()
        if self.canvas is not None:
            self.canvas.grab_focus()

        self.frame = Frame(self, (g.WIDTH/2, g.HEIGHT/2))
        self.clock = pg.time.Clock()
        while self.running:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()

            self.check_events()
            self.draw()
            self.clock.tick(g.FPS)
        pg.display.quit()
        pg.quit()
        sys.exit(0)


# Test if the script is directly ran
if __name__ == "__main__":
    main = Main(journal=False)
    pg.display.set_mode((1024, 768))
    main.run()

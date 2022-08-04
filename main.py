# Copyright (C) 2022 Sparsh Goenka
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pygame as pg
import g
from frame import Frame
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# The main controller
class Main:
    def __init__(self, journal=True):
        self.journal = journal
        self.running = True
        self.canvas = None
        self.heading = pg.font.Font(None, 96).render("Tic - Tac - Toe", True, g.WHITE)

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
        g.WIN.blit(
            self.heading,
            (
                (g.WIDTH - self.heading.get_width()) // 2,
                (g.HEIGHT * 0.5 - g.FRAME_GAP * 1.5 - self.heading.get_height()) // 2,
            ),
        )
        self.frame.draw()
        pg.display.update()

    def reset(self):
        self.frame = Frame(self, (g.WIDTH / 2, g.HEIGHT / 2))

    # The main loop
    def run(self):
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
        g.init()
        if self.canvas is not None:
            self.canvas.grab_focus()

        self.frame = Frame(self, (g.WIDTH / 2, g.HEIGHT / 2))
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
    pg.init()
    pg.display.set_mode((1024, 768))
    main = Main(journal=False)
    main.run()

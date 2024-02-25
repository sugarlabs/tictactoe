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
from anim import Animate
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
        self.score = [0, 0]
        self.show_help = False
        self.help_img = pg.image.load("help.jpg")

    def set_canvas(self, canvas):
        self.canvas = canvas
        pg.display.set_caption("Tic-Tac-Toe")

    def write_file(self, file_path):
        pass

    def read_file(self, file_path):
        pass

    def quit(self):
        self.running = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
            if event.type == pg.MOUSEBUTTONUP:
                if self.help_pos.collidepoint(pg.mouse.get_pos()):
                    self.show_help = not self.show_help
                if self.show_help == True: 
                    break
                if self.canvas is not None:
                    self.canvas.grab_focus()
                if self.frame.detect_click(pg.mouse.get_pos()):
                    self.set_turn()
                if self.reset_rect.collidepoint(pg.mouse.get_pos()):
                    self.frame.reset(False)
                    self.score = [0, 0]

    def draw_help(self):
        pg.draw.circle(
            g.WIN,
            g.GREY,
            self.help_pos.center,
            40,
        )
        if self.show_help:
            g.WIN.blit(
                self.close_text,
                (
                    (3 * g.WIDTH + g.FRAME_GAP * 3 - 2 * self.close_text.get_width())
                    // 4,
                    (g.HEIGHT * 0.5 - g.FRAME_GAP * 1.5 - self.close_text.get_height())
                    // 2,
                ),
            )
            pg.draw.rect(
                g.WIN,
                g.GREY,
                pg.Rect(
                    50,
                    (g.HEIGHT - g.FRAME_GAP * 3) // 2 - 10,
                    g.WIDTH - 100,
                    g.FRAME_GAP * 3 + 20,
                ),
            )
            g.WIN.blit(
                self.help_img,
                (
                    (g.WIDTH - self.help_img.get_width()) // 2,
                    (g.HEIGHT - g.FRAME_GAP * 3) // 2,
                ),
            )
            for i, text in enumerate(self.help_text):
                g.WIN.blit(
                    text,
                    (
                        (g.WIDTH - text.get_width()) // 2,
                        g.HEIGHT // 2 + 40 + 40 * i,
                    ),
                )
        else:
            g.WIN.blit(
                self.question_text,
                (
                    (3 * g.WIDTH + g.FRAME_GAP * 3 - 2 * self.question_text.get_width())
                    // 4,
                    (
                        g.HEIGHT * 0.5
                        - g.FRAME_GAP * 1.5
                        - self.question_text.get_height()
                    )
                    // 2,
                ),
            )

    def draw(self):
        g.WIN.fill(g.BLACK)
        g.WIN.blit(
            self.heading,
            (
                (g.WIDTH - self.heading.get_width()) // 2,
                (g.HEIGHT * 0.5 - g.FRAME_GAP * 1.5 - self.heading.get_height()) // 2,
            ),
        )
        g.WIN.blit(
            self.turn_text,
            (
                (g.WIDTH - g.FRAME_GAP * 3 - 2 * self.turn_text.get_width()) / 4,
                (g.HEIGHT * 0.5 - g.FRAME_GAP * 1.5 - self.turn_text.get_height()) // 2,
            ),
        )
        self.frame.draw()
        self.cross_ui.update()
        self.circle_ui.update()
        scorex = self.font.render(str(self.score[0]), True, g.WHITE)
        scoreo = self.font.render(str(self.score[1]), True, g.WHITE)
        g.WIN.blit(
            scorex,
            (
                (g.WIDTH - g.FRAME_GAP * 3 - 2 * scorex.get_width()) / 4,
                (g.HEIGHT / 2 + g.FRAME_GAP / 4),
            ),
        )
        g.WIN.blit(
            scoreo,
            (
                g.WIDTH - (g.WIDTH - g.FRAME_GAP * 3 + 2 * scorex.get_width()) / 4,
                (g.HEIGHT / 2 + g.FRAME_GAP / 4),
            ),
        )
        self.draw_help()
        pg.draw.rect(g.WIN, g.GREY, self.reset_rect)
        pg.draw.circle(
            g.WIN,
            g.GREY,
            (int(self.reset_rect.x), int(self.reset_rect.centery)),
            self.reset_rect.height // 2,
        )
        pg.draw.circle(
            g.WIN,
            g.GREY,
            (int(self.reset_rect.right), int(self.reset_rect.centery)),
            self.reset_rect.height // 2,
        )
        g.WIN.blit(
            self.reset_text,
            (
                g.WIDTH / 2 - self.reset_text.get_width() / 2,
                g.HEIGHT - self.reset_text.get_height() - 70,
            ),
        )
        pg.display.update()

    def reset(self):
        self.frame = Frame(self, (g.WIDTH / 2, g.HEIGHT / 2))

    def set_turn(self):
        self.turn_text = pg.font.Font(None, 64).render(
        ["O Turn", "", "X Turn"][self.frame.turn + 1], True, g.WHITE)
    # The main loop
    def run(self):
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
        g.init()
        pg.font.init()
        self.heading = pg.font.Font(None, 96).render("Tic - Tac - Toe", True, g.WHITE)
        self.reset_text = pg.font.Font(None, 56).render("Reset", True, g.WHITE)
        self.question_text = pg.font.Font(None, 72).render("?", True, g.WHITE)
        self.close_text = pg.font.Font(None, 64).render("X", True, g.WHITE)
        self.help_text = [
            pg.font.Font(None, 36).render(
                i,
                True,
                g.WHITE,
            )
            for i in (
                "Each player takes it in turn to place their X or O",
                "into one of the empty squares in the grid by clicking on it.",
                "To win the game get three of your symbols in a line",
                "horizontally, vertically or diagonally",
            )
        ]
        self.help_pos = pg.Rect(
            (3 * g.WIDTH + g.FRAME_GAP * 3) // 4 - 40,
            (g.HEIGHT * 0.5 - g.FRAME_GAP * 1.5) // 2 - 40,
            80,
            80,
        )
        self.reset_rect = pg.Rect(
            g.WIDTH / 2 - self.reset_text.get_width() / 2,
            g.HEIGHT - self.reset_text.get_height() - 80,
            self.reset_text.get_width(),
            self.reset_text.get_height() + 20,
        )
        self.font = pg.font.Font(None, 72)
        self.cross_ui = Animate(self, color=g.ORANGE).cross(
            ((g.WIDTH - g.FRAME_GAP * 3) / 4, g.HEIGHT / 2 - g.FRAME_GAP / 4), 43, 11
        )
        self.circle_ui = Animate(self, color=g.RED).circle(
            (g.WIDTH - (g.WIDTH - g.FRAME_GAP * 3) / 4, g.HEIGHT / 2 - g.FRAME_GAP / 4),
            40,
            8,
        )

        if self.canvas is not None:
            self.canvas.grab_focus()

        self.frame = Frame(self, (g.WIDTH / 2, g.HEIGHT / 2))
        self.set_turn()
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

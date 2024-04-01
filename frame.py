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


class Frame:
    def __init__(self, main, center, gap=g.FRAME_GAP):
        self.main = main
        self.length = 3 * gap
        self.gap = gap
        self.turn = 1
        self.remove = False
        self.center = center
        # fmt: off
        self.points = [
            [self.gap / 2, self.length / 2],
            [self.gap / 2, -self.length / 2],
            [-self.gap / 2, -self.length / 2],
            [-self.gap / 2, self.length / 2],
            [-self.length / 2, self.gap / 2],
            [self.length / 2, self.gap / 2],
            [self.length / 2, -self.gap / 2],
            [-self.length / 2, -self.gap / 2],
        ]
        for point in self.points:
            point[0] += self.center[0]
            point[1] += self.center[1]
        # fmt: on
        self.rects = []
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moves = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

        for i in range(3):
            for j in range(3):
                self.rects.append(
                    pg.Rect(
                        *self.cartesian_to_standard(
                            ((-1.5 + j) * gap, (1.5 - i) * gap)
                        ),
                        gap,
                        gap
                    )
                )

        self.animations = [
            Animate(main, 700 + i * 100).line(self.points[i],
                                              self.points[i + 1])
            for i in range(0, len(self.points), 2)
        ]

    # Convert given list cartesian coordinates to pygame coordinates
    @staticmethod
    def cartesian_to_standard(coord):
        return (coord[0] + g.WIDTH / 2, -coord[1] + g.HEIGHT / 2)

    @staticmethod
    def standard_to_cartesian(coord):
        return (coord[0] - g.WIDTH / 2, -coord[1] + g.HEIGHT / 2)

    def detect_click(self, pos):
        for rect in self.rects:
            if rect.collidepoint(pos):
                # Spawn O or X
                # Update the board
                center = self.standard_to_cartesian(rect.center)
                index = (1 - round(center[1] / self.gap),
                         round(center[0] / self.gap) + 1)
                self.board[index[0]][index[1]] = self.turn
                self.moves[index[0]][index[1]] = OX(self.main,
                                                    self.turn,
                                                    rect.center)
                self.rects.remove(rect)
                self.turn *= -1
                # Check if win
                self.check_win(index)
                return True
        return False

    def reset(self, wait=True):
        for m in self.moves:
            for n in m:
                if n is not None:
                    n.wait_and_remove = True
                    if wait:
                        ticks = pg.time.get_ticks()
                        n.remove_time = (
                            2 * n.blink_count * n.blink_dur + ticks
                        )
                    else:
                        n.remove_time = 0

    def check_win(self, index):
        def check(sum, i, j):
            if abs(sum) == 3:
                self.rects = []
                prev = i, j
                for t in range(3):
                    if i is None:
                        i = t
                    if i == -2:
                        i = 2 - t
                    if j is None:
                        j = t
                    self.moves[i][j].blink = True
                    self.moves[i][j].blink_start = pg.time.get_ticks()
                    i, j = prev
                if sum == 3:
                    self.main.score[0] += 1
                else:
                    self.main.score[1] += 1
                self.reset()

        # fmt: off
        i0 = index[0]
        i1 = index[1]
        _sum = self.board[i0][0] + self.board[i0][1] + self.board[i0][2]
        check(_sum, index[0], None)
        _sum = self.board[0][i1] + self.board[1][i1] + self.board[2][i1]
        check(_sum, None, index[1])
        _sum = self.board[0][0] + self.board[1][1] + self.board[2][2]
        check(_sum, None, None)
        _sum = self.board[2][0] + self.board[1][1] + self.board[0][2]
        check(_sum, -2, None)
        # fmt:on
        tie = 0
        for i in self.board:
            if 0 not in i:
                tie += 1
        if tie == 3:
            self.reset()

    def setup_remove(self, dur=500, animate=False):
        if not self.remove:
            self.remove = True
            self.remove_time = pg.time.get_ticks() + dur
            if animate:
                for i in self.animations:
                    i.setup_remove(dur)

    def draw(self):
        for animation in self.animations:
            animation.update()
        for i in self.moves:
            for move in i:
                if move is not None:
                    move.draw()
        if self.remove:
            if pg.time.get_ticks() > self.remove_time:
                self.main.reset()


class OX:
    def __init__(self, main, _type, center):
        self.main = main
        self.type = _type
        self.center = center
        self.blink = False
        self.blink_count = 3
        self.blink_dur = 250
        self.blink_start = None
        self.wait_and_remove = False
        self.remove_time = None

        if _type == 1:
            self.animation = Animate(main, color=g.ORANGE).cross(center)
        elif _type == -1:
            self.animation = Animate(main, color=g.RED).circle(center)

    def draw(self):
        if self.blink:
            if pg.time.get_ticks() < self.blink_start + self.blink_dur:
                self.animation.update()
            elif pg.time.get_ticks() > self.blink_start + 2 * self.blink_dur:
                self.blink_start = pg.time.get_ticks()
                self.blink_count -= 1
                if self.blink_count == 0:
                    self.blink = False
        else:
            self.animation.update()

        if self.wait_and_remove:
            if pg.time.get_ticks() > self.remove_time:
                self.animation.setup_remove()
                self.main.frame.setup_remove()
                self.wait_and_remove = False

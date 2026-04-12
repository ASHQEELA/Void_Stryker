import math
import pygame
from OpenGL.GL import *

from constants import SCREEN_W, SCREEN_H, RED, ORANGE, GREEN, YELLOW, WHITE, BLACK, PINK
from gl_utils import (
    set_color, draw_circle_filled, draw_circle_outline,
    draw_rect_filled, draw_rect_outline
)
from entities.bullet import Bullet
from entities.enemies import Enemy


class BossEnemy(Enemy):
    """Boss: phased movement and three distinct attack patterns."""

    def __init__(self):
        super().__init__(SCREEN_W // 2, -80, hp=120, speed=0.5,
                         score_val=2000, color=RED, size=55)
        self.shoot_cooldown = 0.8
        self.phase = 1
        self.entry_done = False
        self.angle = 0
        self.move_dir = 1

    def update(self, dt, px, py):
        self.t += dt
        self.shoot_timer += dt
        self.angle += dt * 60

        if not self.entry_done:
            self.y += 1.2 * dt * 60
            if self.y >= 120:
                self.y = 120
                self.entry_done = True
            return

        ratio = self.hp / self.max_hp
        if ratio < 0.35:
            self.phase = 3
        elif ratio < 0.65:
            self.phase = 2

        self.x += self.move_dir * self.speed * dt * 60 * 0.6
        if self.x > SCREEN_W - 80 or self.x < 80:
            self.move_dir *= -1

        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            self._shoot(px, py)

        self.bullets = [b for b in self.bullets if b.alive]
        for b in self.bullets:
            b.update(dt)

    def _shoot(self, px, py):
        if self.phase == 1:
            for i in range(8):
                a = 2 * math.pi * i / 8
                self.bullets.append(
                    Bullet(self.x, self.y, math.sin(a) * 3, RED,
                           damage=1, vx=math.cos(a) * 3, size=6)
                )
        elif self.phase == 2:
            dx = px - self.x
            dy = py - self.y
            dist = math.sqrt(dx * dx + dy * dy) or 1
            spd = 4.5
            self.bullets.append(
                Bullet(self.x, self.y, dy / dist * spd, ORANGE,
                       damage=2, vx=dx / dist * spd, size=7)
            )
            self.bullets.append(Bullet(self.x - 40, self.y, 4, RED, damage=1, size=6))
            self.bullets.append(Bullet(self.x + 40, self.y, 4, RED, damage=1, size=6))
        elif self.phase == 3:
            for i in range(12):
                a = 2 * math.pi * i / 12 + self.angle * 0.05
                spd = 3.5
                self.bullets.append(
                    Bullet(self.x, self.y, math.sin(a) * spd,
                           (1.0, 0.2, 0.8, 1.0), damage=1,
                           vx=math.cos(a) * spd, size=5)
                )

    def draw(self):
        s = self.size
        ratio = self.hp / self.max_hp

        # Rotating outer ring
        from OpenGL.GL import glLineWidth, glBegin, GL_LINE_LOOP, glEnd, glVertex2f
        glLineWidth(2)
        set_color((1.0, 0.2, 0.2, 0.4))
        glBegin(GL_LINE_LOOP)
        for i in range(36):
            a = 2 * math.pi * i / 36 + math.radians(self.angle)
            glVertex2f(self.x + (s + 18) * math.cos(a), self.y + (s + 18) * math.sin(a))
        glEnd()

        # Octagon body
        set_color((0.6, 0.0, 0.0, 1.0))
        glBegin(GL_POLYGON)
        for i in range(8):
            a = 2 * math.pi * i / 8 + math.radians(self.angle * 0.5)
            glVertex2f(self.x + s * math.cos(a), self.y + s * math.sin(a))
        glEnd()

        # Phase-colored inner core
        phase_colors = [
            (1.0, 0.3, 0.0, 1.0),
            (1.0, 0.1, 0.5, 1.0),
            (0.6, 0.0, 1.0, 1.0),
        ]
        draw_circle_filled(self.x, self.y, s * 0.45, phase_colors[self.phase - 1])

        # Eye
        draw_circle_filled(self.x, self.y, s * 0.18, WHITE)
        draw_circle_filled(self.x, self.y, s * 0.08, BLACK)

        # Boss HP bar at top of screen
        bw = 200
        bh = 12
        bx = SCREEN_W / 2 - 100
        by = 16
        draw_rect_filled(bx - 2, by - 2, bw + 4, bh + 4, (0.1, 0.1, 0.1, 0.9))
        bar_color = GREEN if ratio > 0.65 else (YELLOW if ratio > 0.35 else RED)
        draw_rect_filled(bx, by, bw * ratio, bh, bar_color)
        draw_rect_outline(bx, by, bw, bh, WHITE, 1)

        for b in self.bullets:
            b.draw()

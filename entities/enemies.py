import math
import pygame
from OpenGL.GL import *

from constants import (
    SCREEN_H, RED, ORANGE, PURPLE, GREEN, PINK, YELLOW, WHITE
)
from gl_utils import (
    set_color, draw_circle_filled, draw_circle_outline,
    draw_line, draw_triangle, draw_diamond,
    draw_rect_filled, draw_rect_outline
)
from entities.bullet import Bullet


class Enemy:
    def __init__(self, x, y, hp, speed, score_val, color, size=20):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.score_val = score_val
        self.color = color
        self.size = size
        self.alive = True
        self.t = 0
        self.shoot_timer = 0
        self.shoot_cooldown = 2.5
        self.bullets = []

    def update(self, dt, player_x, player_y):
        self.t += dt
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            self._shoot(player_x, player_y)
        self.bullets = [b for b in self.bullets if b.alive]
        for b in self.bullets:
            b.update(dt)

    def _shoot(self, px, py):
        pass

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

    def rect(self):
        s = self.size
        return pygame.Rect(self.x - s, self.y - s, s * 2, s * 2)

    def draw_hp_bar(self):
        ratio = self.hp / self.max_hp
        bw = self.size * 2
        bh = 4
        bx = self.x - self.size
        by = self.y - self.size - 8
        draw_rect_filled(bx, by, bw, bh, (0.2, 0.2, 0.2, 0.8))
        bar_color = GREEN if ratio > 0.5 else (YELLOW if ratio > 0.25 else RED)
        draw_rect_filled(bx, by, bw * ratio, bh, bar_color)

    def draw(self):
        pass


class ScoutEnemy(Enemy):
    """Fast, sine-wave movement. Fires single downward bullet."""

    def __init__(self, x, y):
        super().__init__(x, y, hp=2, speed=2.5, score_val=100, color=RED, size=12)
        self.shoot_cooldown = 2.0
        self.base_x = x

    def update(self, dt, px, py):
        self.y += self.speed * dt * 60 * 0.5
        self.x = self.base_x + math.sin(self.t * 2) * 40
        super().update(dt, px, py)
        if self.y > SCREEN_H + 40:
            self.alive = False

    def _shoot(self, px, py):
        self.bullets.append(Bullet(self.x, self.y, 3.5, RED, damage=1, size=5))

    def draw(self):
        s = self.size
        pulse = 0.8 + 0.2 * math.sin(self.t * 5)
        c = (self.color[0], self.color[1] * pulse, self.color[2] * pulse, 1.0)
        set_color(c)
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x,      self.y + s)
        glVertex2f(self.x - s,  self.y - s * 0.8)
        glVertex2f(self.x + s,  self.y - s * 0.8)
        glEnd()
        draw_circle_filled(self.x, self.y - s * 0.5, s * 0.35, (1.0, 0.4, 0.0, 0.7))
        self.draw_hp_bar()
        for b in self.bullets:
            b.draw()


class TankEnemy(Enemy):
    """Slow, high-HP. Fires 3-way spread."""

    def __init__(self, x, y):
        super().__init__(x, y, hp=14, speed=0.6, score_val=400, color=ORANGE, size=30)
        self.shoot_cooldown = 3.0

    def update(self, dt, px, py):
        self.y += self.speed * dt * 60 * 0.35
        super().update(dt, px, py)
        if self.y > SCREEN_H + 60:
            self.alive = False

    def _shoot(self, px, py):
        for dx in [-1.5, 0, 1.5]:
            self.bullets.append(Bullet(self.x, self.y, 2.5, ORANGE, damage=1, vx=dx, size=7))

    def draw(self):
        s = self.size
        set_color(self.color)
        glBegin(GL_POLYGON)
        for i in range(6):
            a = math.pi / 6 + 2 * math.pi * i / 6
            glVertex2f(self.x + s * math.cos(a), self.y + s * math.sin(a))
        glEnd()
        set_color((0.2, 0.2, 0.2, 1.0))
        glBegin(GL_POLYGON)
        for i in range(6):
            a = math.pi / 6 + 2 * math.pi * i / 6
            glVertex2f(self.x + (s * 0.55) * math.cos(a), self.y + (s * 0.55) * math.sin(a))
        glEnd()
        draw_circle_outline(self.x, self.y, s, (1.0, 0.7, 0.0, 0.5), 12, 2)
        self.draw_hp_bar()
        for b in self.bullets:
            b.draw()


class SniperEnemy(Enemy):
    """Fires a fast, aimed piercing shot directly at the player."""

    def __init__(self, x, y):
        super().__init__(x, y, hp=5, speed=0.8, score_val=250, color=PURPLE, size=18)
        self.shoot_cooldown = 3.5
        self.aim_x = x
        self.aim_y = y

    def update(self, dt, px, py):
        self.y += self.speed * dt * 60 * 0.2
        self.aim_x = px
        self.aim_y = py
        super().update(dt, px, py)
        if self.y > SCREEN_H + 40:
            self.alive = False

    def _shoot(self, px, py):
        dx = px - self.x
        dy = py - self.y
        dist = math.sqrt(dx * dx + dy * dy) or 1
        spd = 5.5
        self.bullets.append(
            Bullet(self.x, self.y, dy / dist * spd, PURPLE,
                   damage=2, vx=dx / dist * spd, size=6, piercing=True)
        )

    def draw(self):
        s = self.size
        draw_diamond(self.x, self.y, s * 1.5, s * 2, PURPLE)
        if self.aim_x and self.aim_y:
            draw_line(self.x, self.y, self.aim_x, self.aim_y, (0.7, 0.0, 1.0, 0.18), 1)
        draw_circle_outline(self.x, self.y, s * 0.4, PINK, 12, 1)
        self.draw_hp_bar()
        for b in self.bullets:
            b.draw()


class SwarmerEnemy(Enemy):
    """Charges directly at the player. No bullets."""

    def __init__(self, x, y):
        super().__init__(x, y, hp=1, speed=2.8, score_val=75, color=GREEN, size=10)
        self.shoot_cooldown = 999

    def update(self, dt, px, py):
        dx = px - self.x
        dy = py - self.y
        dist = math.sqrt(dx * dx + dy * dy) or 1
        self.x += dx / dist * self.speed * dt * 60 * 0.4
        self.y += dy / dist * self.speed * dt * 60 * 0.4
        self.t += dt
        if self.y > SCREEN_H + 40:
            self.alive = False

    def draw(self):
        s = self.size
        pulse = 0.85 + 0.15 * math.sin(self.t * 8)
        c = (0.1, 1.0 * pulse, 0.3, 1.0)
        draw_triangle(self.x, self.y, s, c, self.t * 3)
        draw_circle_outline(self.x, self.y, s * 1.4, (0.1, 1.0, 0.3, 0.3), 8, 1)
        self.draw_hp_bar()

    def _shoot(self, px, py):
        pass

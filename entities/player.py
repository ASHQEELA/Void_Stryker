import random
import pygame
from pygame.locals import *
from OpenGL.GL import *

from constants import SCREEN_W, SCREEN_H, CYAN, RED, PINK, GREEN
from gl_utils import set_color, draw_circle_filled, draw_circle_outline
from entities.bullet import Bullet
from entities.particle import Particle, explode


class Player:
    def __init__(self):
        self.x = SCREEN_W / 2
        self.y = SCREEN_H - 80
        self.speed = 4.5
        self.hp = 5
        self.max_hp = 5
        self.alive = True
        self.bullets = []
        self.shoot_timer = 0
        self.shoot_cooldown = 0.22
        self.size = 18
        self.invincible = 0.0
        self.t = 0

        self.shield = 0.0
        self.rapid = 0.0
        self.spread = 0.0
        self.laser = 0.0

        self.engine_particles = []

    def apply_powerup(self, kind, particles):
        if kind == "shield":
            self.shield = 8.0
        elif kind == "rapid":
            self.rapid = 7.0
        elif kind == "spread":
            self.spread = 7.0
        elif kind == "laser":
            self.laser = 7.0
        elif kind == "health":
            self.hp = min(self.hp + 2, self.max_hp)
        elif kind == "bomb":
            return "bomb"

    def update(self, dt, keys):
        self.t += dt
        self.invincible = max(0, self.invincible - dt)
        self.shield = max(0, self.shield - dt)
        self.rapid = max(0, self.rapid - dt)
        self.spread = max(0, self.spread - dt)
        self.laser = max(0, self.laser - dt)

        dx = dy = 0
        if keys[K_LEFT]  or keys[K_a]: dx -= 1
        if keys[K_RIGHT] or keys[K_d]: dx += 1
        if keys[K_UP]    or keys[K_w]: dy -= 1
        if keys[K_DOWN]  or keys[K_s]: dy += 1

        if dx and dy:
            dx *= 0.707
            dy *= 0.707

        self.x = max(self.size, min(SCREEN_W - self.size, self.x + dx * self.speed * dt * 60))
        self.y = max(self.size, min(SCREEN_H - self.size, self.y + dy * self.speed * dt * 60))

        if random.random() < 0.6:
            self.engine_particles.append(
                Particle(
                    self.x + random.uniform(-5, 5),
                    self.y + self.size,
                    random.uniform(-0.3, 0.3),
                    random.uniform(0.5, 1.5),
                    (0.3, 0.7, 1.0, 0.8),
                    random.uniform(0.2, 0.5),
                    random.uniform(2, 5),
                )
            )
        self.engine_particles = [p for p in self.engine_particles if p.alive]
        for p in self.engine_particles:
            p.update(dt)

        self.shoot_timer += dt
        cooldown = self.shoot_cooldown * (0.45 if self.rapid > 0 else 1.0)
        if keys[K_SPACE] and self.shoot_timer >= cooldown:
            self.shoot_timer = 0
            self._fire()

        self.bullets = [b for b in self.bullets if b.alive]
        for b in self.bullets:
            b.update(dt)

    def _fire(self):
        if self.laser > 0:
            self.bullets.append(Bullet(self.x, self.y, -14, PINK, damage=3, size=8, piercing=True))
        elif self.spread > 0:
            for vx in [-2.5, -1.2, 0, 1.2, 2.5]:
                self.bullets.append(Bullet(self.x, self.y, -8, CYAN, damage=1, vx=vx, size=5))
        else:
            self.bullets.append(Bullet(self.x, self.y, -10, CYAN, damage=1, size=5))

    def take_damage(self, amt, particles):
        if self.invincible > 0:
            return
        if self.shield > 0:
            self.shield = 0
            self.invincible = 1.5
            explode(particles, self.x, self.y, CYAN, 12, 3.0)
            return
        self.hp -= amt
        self.invincible = 1.2
        explode(particles, self.x, self.y, RED, 12, 3.0)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def rect(self):
        s = self.size
        return pygame.Rect(self.x - s, self.y - s, s * 2, s * 2)

    def draw(self):
        for p in self.engine_particles:
            p.draw()

        s = self.size
        if self.invincible > 0 and int(self.t * 10) % 2 == 0:
            return

        set_color(CYAN)
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x,      self.y - s)
        glVertex2f(self.x - s,  self.y + s * 0.7)
        glVertex2f(self.x + s,  self.y + s * 0.7)
        glEnd()

        set_color((0.0, 0.7, 1.0, 1.0))
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x - s,       self.y + s * 0.3)
        glVertex2f(self.x - s * 1.8, self.y + s)
        glVertex2f(self.x - s * 0.3, self.y + s * 0.7)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x + s,       self.y + s * 0.3)
        glVertex2f(self.x + s * 1.8, self.y + s)
        glVertex2f(self.x + s * 0.3, self.y + s * 0.7)
        glEnd()

        draw_circle_filled(self.x, self.y - s * 0.1, s * 0.35, (0.8, 1.0, 1.0, 1.0))

        if self.shield > 0:
            alpha = min(1.0, self.shield / 2.0)
            draw_circle_outline(self.x, self.y, s * 2.2, (0.0, 1.0, 1.0, alpha), 24, 2)
            draw_circle_filled(self.x, self.y, s * 2.2, (0.0, 0.5, 1.0, 0.1), 24)

        for b in self.bullets:
            b.draw()

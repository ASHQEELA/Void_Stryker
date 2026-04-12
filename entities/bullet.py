from constants import SCREEN_W, SCREEN_H
from gl_utils import draw_circle_filled


class Bullet:
    def __init__(self, x, y, vy, color, damage=1, vx=0, size=6, piercing=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.damage = damage
        self.size = size
        self.piercing = piercing
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        if self.y < -20 or self.y > SCREEN_H + 20 or self.x < -20 or self.x > SCREEN_W + 20:
            self.alive = False

    def draw(self):
        draw_circle_filled(self.x, self.y, self.size, self.color)
        glow = (self.color[0], self.color[1], self.color[2], 0.25)
        draw_circle_filled(self.x, self.y, self.size * 2.2, glow)
